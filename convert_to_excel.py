#!/usr/bin/env python3
"""
Convert categorized Q&A data from markdown files to Excel format
Following the expected format: Question,Expected Answer,Source (Youtube URL),Product,Question Type,Intent_Category,Intent_SubCategory
"""

import os
import re
import pandas as pd
from pathlib import Path
from typing import List, Dict, Tuple
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class QAToExcelConverter:
    def __init__(self, categorized_dir: str = "output/categorized", output_file: str = "qa_database.xlsx"):
        self.categorized_dir = Path(categorized_dir)
        self.output_file = output_file
        self.qa_data = []
        
    def extract_qa_pairs_from_file(self, file_path: Path) -> List[Dict]:
        """Extract Q&A pairs from a markdown file."""
        qa_pairs = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Split by Q&A sections
            sections = re.split(r'\n## Q:', content)
            
            for section in sections[1:]:  # Skip the first empty section
                if not section.strip():
                    continue
                
                # Extract question and answer
                lines = section.strip().split('\n')
                if not lines:
                    continue
                
                question = lines[0].strip()
                
                # Find the answer (everything after "**A:** Answer:")
                answer_start = -1
                for i, line in enumerate(lines):
                    if '**A:** Answer:' in line:
                        answer_start = i
                        break
                
                if answer_start == -1:
                    continue
                
                # Extract answer content
                answer_lines = []
                for line in lines[answer_start:]:
                    if line.strip().startswith('---'):
                        break
                    answer_lines.append(line.strip())
                
                answer = '\n'.join(answer_lines).strip()
                
                # Clean up the answer
                answer = re.sub(r'^\*\*A:\*\* Answer:\s*', '', answer, flags=re.IGNORECASE)
                
                if question and answer and len(answer) > 10:
                    qa_pairs.append({
                        'question': question,
                        'answer': answer,
                        'file_path': str(file_path)
                    })
        
        except Exception as e:
            logger.error(f"Error processing {file_path}: {e}")
        
        return qa_pairs
    
    def determine_product_and_categories(self, file_path: Path) -> Tuple[str, str, str]:
        """Determine product, intent category, and subcategory from file path."""
        path_parts = file_path.parts
        
        # Find the product (main category)
        product = "Unknown"
        intent_category = "Unknown"
        intent_subcategory = "Unknown"
        
        for part in path_parts:
            if part in ["SketchUp_Pro_(Desktop)", "SketchUp_Web_Browser_based", "SketchUp_Go_(iPad", "SketchUp_Mobile_Viewer", "SketchUp_Shop_(Web_Premium)", "SketchUp_Studio_Professional_Suite", "LayOut_(Documentation_Tool)"]:
                product = part
                break
        
        # Find intent category and subcategory
        if "categorized" in path_parts:
            categorized_index = path_parts.index("categorized")
            if len(path_parts) > categorized_index + 1:
                intent_category = path_parts[categorized_index + 1]
            if len(path_parts) > categorized_index + 2:
                intent_subcategory = path_parts[categorized_index + 2]
        
        return product, intent_category, intent_subcategory
    
    def determine_question_type(self, question: str) -> str:
        """Determine the question type based on the question content."""
        question_lower = question.lower()
        
        if any(word in question_lower for word in ['how', 'step', 'process', 'procedure']):
            return "How-to"
        elif any(word in question_lower for word in ['what', 'define', 'meaning']):
            return "What-is"
        elif any(word in question_lower for word in ['why', 'reason', 'purpose']):
            return "Why"
        elif any(word in question_lower for word in ['troubleshoot', 'error', 'problem', 'fix', 'issue']):
            return "Troubleshooting"
        elif any(word in question_lower for word in ['practice', 'learn', 'improve', 'skill']):
            return "Practice"
        elif any(word in question_lower for word in ['where', 'find', 'location', 'menu']):
            return "Location"
        elif any(word in question_lower for word in ['when', 'time', 'duration']):
            return "When"
        else:
            return "General"
    
    def extract_source_url(self, file_path: Path) -> str:
        """Extract source URL from file path or content."""
        # Try to extract from file path first
        file_name = file_path.stem
        if file_name.startswith('video_'):
            # Extract video ID if present
            video_match = re.search(r'video_([a-zA-Z0-9_-]+)', file_name)
            if video_match:
                video_id = video_match.group(1)
                return f"https://www.youtube.com/watch?v={video_id}"
        
        # If no video ID found, return a placeholder
        return "Source URL not available"
    
    def process_all_files(self):
        """Process all categorized Q&A files and convert to Excel format."""
        logger.info("Starting conversion of categorized Q&A files to Excel format...")
        
        # Find all categorized_QnAs.md files
        qa_files = list(self.categorized_dir.rglob("categorized_QnAs.md"))
        logger.info(f"Found {len(qa_files)} Q&A files to process")
        
        total_qa_pairs = 0
        
        for file_path in qa_files:
            logger.info(f"Processing: {file_path}")
            
            # Extract Q&A pairs from file
            qa_pairs = self.extract_qa_pairs_from_file(file_path)
            
            # Determine categories
            product, intent_category, intent_subcategory = self.determine_product_and_categories(file_path)
            
            # Process each Q&A pair
            for qa_pair in qa_pairs:
                question_type = self.determine_question_type(qa_pair['question'])
                source_url = self.extract_source_url(file_path)
                
                # Create Excel row
                excel_row = {
                    'Question': qa_pair['question'],
                    'Expected Answer': qa_pair['answer'],
                    'Source (Youtube URL)': source_url,
                    'Product': product,
                    'Question Type': question_type,
                    'Intent_Category': intent_category,
                    'Intent_SubCategory': intent_subcategory
                }
                
                self.qa_data.append(excel_row)
                total_qa_pairs += 1
        
        logger.info(f"Total Q&A pairs extracted: {total_qa_pairs}")
    
    def create_excel_file(self):
        """Create Excel file with the extracted Q&A data."""
        if not self.qa_data:
            logger.warning("No Q&A data to export!")
            return
        
        # Create DataFrame
        df = pd.DataFrame(self.qa_data)
        
        # Reorder columns to match expected format
        columns_order = [
            'Question', 'Expected Answer', 'Source (Youtube URL)', 
            'Product', 'Question Type', 'Intent_Category', 'Intent_SubCategory'
        ]
        df = df[columns_order]
        
        # Create Excel file
        with pd.ExcelWriter(self.output_file, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name='Q&A Database', index=False)
            
            # Auto-adjust column widths
            worksheet = writer.sheets['Q&A Database']
            for column in worksheet.columns:
                max_length = 0
                column_letter = column[0].column_letter
                for cell in column:
                    try:
                        if len(str(cell.value)) > max_length:
                            max_length = len(str(cell.value))
                    except:
                        pass
                adjusted_width = min(max_length + 2, 50)  # Cap at 50 characters
                worksheet.column_dimensions[column_letter].width = adjusted_width
        
        logger.info(f"Excel file created successfully: {self.output_file}")
        logger.info(f"Total rows exported: {len(df)}")
        
        # Print summary statistics
        self.print_summary_statistics(df)
    
    def print_summary_statistics(self, df: pd.DataFrame):
        """Print summary statistics of the exported data."""
        print("\n" + "="*60)
        print("EXPORT SUMMARY STATISTICS")
        print("="*60)
        
        print(f"\n📊 Total Q&A pairs: {len(df)}")
        
        print(f"\n📁 Products:")
        for product, count in df['Product'].value_counts().items():
            print(f"  - {product}: {count} Q&A pairs")
        
        print(f"\n🏷️  Question Types:")
        for qtype, count in df['Question Type'].value_counts().items():
            print(f"  - {qtype}: {count} Q&A pairs")
        
        print(f"\n📂 Intent Categories:")
        for category, count in df['Intent_Category'].value_counts().items():
            print(f"  - {category}: {count} Q&A pairs")
        
        print(f"\n📂 Intent SubCategories (Top 10):")
        for subcategory, count in df['Intent_SubCategory'].value_counts().head(10).items():
            print(f"  - {subcategory}: {count} Q&A pairs")
        
        print("\n" + "="*60)

def main():
    """Main function to run the conversion."""
    converter = QAToExcelConverter()
    
    try:
        # Process all files
        converter.process_all_files()
        
        # Create Excel file
        converter.create_excel_file()
        
        print(f"\n✅ Conversion completed successfully!")
        print(f"📄 Excel file saved as: {converter.output_file}")
        
    except Exception as e:
        logger.error(f"Error during conversion: {e}")
        raise

if __name__ == "__main__":
    main() 