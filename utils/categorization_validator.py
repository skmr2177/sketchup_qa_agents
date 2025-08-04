#!/usr/bin/env python3
"""
Categorization Validation Script
Validates the current Q&A categorization and identifies issues
"""

import os
import re
from pathlib import Path
from typing import List, Dict, Tuple, Set
from collections import defaultdict

class CategorizationValidator:
    def __init__(self, base_output_dir="output"):
        self.base_output_dir = Path(base_output_dir)
        self.categorized_dir = self.base_output_dir / "categorized"
        
        # Define expected content patterns for each category
        self.category_patterns = {
            "Extensions_Plugins": {
                "required_keywords": ["extension", "plugin", "warehouse", "install"],
                "excluded_keywords": ["extension of", "extend", "extending"],
                "min_matches": 2
            },
            "Materials_Textures": {
                "required_keywords": ["material", "texture", "pbr", "ambient occlusion", "realistic"],
                "excluded_keywords": [],
                "min_matches": 2
            },
            "LayOut_Integration": {
                "required_keywords": ["layout", "viewport", "documentation", "modification tools"],
                "excluded_keywords": [],
                "min_matches": 2
            },
            "Drawing_Modeling_Tools": {
                "required_keywords": ["tool", "modeling", "drawing", "geometry", "shape"],
                "excluded_keywords": [],
                "min_matches": 1
            },
            "Import_Export": {
                "required_keywords": ["import", "export", "cad", "file", "reference image"],
                "excluded_keywords": [],
                "min_matches": 2
            }
        }
    
    def extract_file_content(self, file_path: Path) -> str:
        """Extract content from Q&A file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            return content.lower()
        except Exception as e:
            print(f"Error reading {file_path}: {e}")
            return ""
    
    def validate_category_content(self, content: str, category: str) -> Tuple[bool, List[str]]:
        """Validate if content matches the assigned category"""
        if category not in self.category_patterns:
            return True, []  # Skip validation for undefined categories
        
        pattern = self.category_patterns[category]
        issues = []
        
        # Check for excluded keywords
        for excluded in pattern["excluded_keywords"]:
            if excluded in content:
                issues.append(f"Contains excluded keyword: '{excluded}'")
        
        # Count required keyword matches
        matches = 0
        matched_keywords = []
        for keyword in pattern["required_keywords"]:
            if keyword in content:
                matches += 1
                matched_keywords.append(keyword)
        
        if matches < pattern["min_matches"]:
            issues.append(f"Insufficient keyword matches: {matches}/{pattern['min_matches']} required")
            issues.append(f"Found keywords: {matched_keywords}")
        
        is_valid = len(issues) == 0
        return is_valid, issues
    
    def analyze_file_categorization(self, file_path: Path) -> Dict:
        """Analyze a single file's categorization"""
        # Extract path components
        parts = file_path.parts
        if len(parts) < 4:
            return {"error": "Invalid file path structure"}
        
        platform = parts[-4]
        category = parts[-3]
        subcategory = parts[-2]
        filename = parts[-1]
        
        # Extract content
        content = self.extract_file_content(file_path)
        if not content:
            return {"error": "Could not read file content"}
        
        # Validate categorization
        is_valid, issues = self.validate_category_content(content, category)
        
        # Analyze content for other potential categories
        potential_categories = []
        for cat, pattern in self.category_patterns.items():
            if cat != category:
                matches = sum(1 for keyword in pattern["required_keywords"] if keyword in content)
                if matches >= pattern["min_matches"]:
                    potential_categories.append((cat, matches))
        
        # Sort potential categories by match count
        potential_categories.sort(key=lambda x: x[1], reverse=True)
        
        return {
            "file_path": str(file_path),
            "platform": platform,
            "current_category": category,
            "current_subcategory": subcategory,
            "is_valid": is_valid,
            "issues": issues,
            "potential_categories": potential_categories,
            "content_preview": content[:200] + "..." if len(content) > 200 else content
        }
    
    def validate_all_categorizations(self) -> Dict:
        """Validate all categorizations and generate report"""
        print("🔍 Starting categorization validation...")
        
        all_files = list(self.categorized_dir.rglob("categorized_QnAs.md"))
        print(f"📁 Found {len(all_files)} categorized files to validate")
        
        validation_results = {
            "total_files": len(all_files),
            "valid_files": 0,
            "invalid_files": 0,
            "files_by_category": defaultdict(list),
            "issues_by_category": defaultdict(list),
            "misclassifications": [],
            "detailed_results": []
        }
        
        for file_path in all_files:
            result = self.analyze_file_categorization(file_path)
            
            if "error" in result:
                print(f"❌ Error processing {file_path.name}: {result['error']}")
                continue
            
            validation_results["detailed_results"].append(result)
            validation_results["files_by_category"][result["current_category"]].append(result)
            
            if result["is_valid"]:
                validation_results["valid_files"] += 1
            else:
                validation_results["invalid_files"] += 1
                validation_results["issues_by_category"][result["current_category"]].append(result)
                
                # Check for potential misclassifications
                if result["potential_categories"]:
                    best_alternative = result["potential_categories"][0]
                    if best_alternative[1] > 2:  # More than 2 keyword matches
                        validation_results["misclassifications"].append({
                            "file": result["file_path"],
                            "current_category": result["current_category"],
                            "suggested_category": best_alternative[0],
                            "confidence": best_alternative[1],
                            "issues": result["issues"]
                        })
        
        return validation_results
    
    def generate_validation_report(self, results: Dict) -> str:
        """Generate detailed validation report"""
        report = f"""# Categorization Validation Report

Generated on: {Path(__file__).stat().st_mtime}

## Summary

- **Total files analyzed**: {results['total_files']}
- **Valid categorizations**: {results['valid_files']}
- **Invalid categorizations**: {results['invalid_files']}
- **Success rate**: {(results['valid_files'] / max(results['total_files'], 1) * 100):.1f}%

## Issues by Category

"""
        
        for category, files in results["issues_by_category"].items():
            report += f"### {category}\n"
            report += f"**Files with issues**: {len(files)}\n\n"
            
            for file_result in files:
                report += f"**File**: {Path(file_result['file_path']).name}\n"
                report += f"**Issues**:\n"
                for issue in file_result["issues"]:
                    report += f"- {issue}\n"
                
                if file_result["potential_categories"]:
                    report += f"**Potential better categories**:\n"
                    for cat, matches in file_result["potential_categories"][:3]:
                        report += f"- {cat} ({matches} keyword matches)\n"
                
                report += f"**Content preview**: {file_result['content_preview']}\n\n"
        
        # Misclassifications section
        if results["misclassifications"]:
            report += "## Potential Misclassifications\n\n"
            report += "| File | Current Category | Suggested Category | Confidence | Issues |\n"
            report += "|------|------------------|-------------------|------------|--------|\n"
            
            for mis in results["misclassifications"]:
                filename = Path(mis["file"]).name
                report += f"| {filename} | {mis['current_category']} | {mis['suggested_category']} | {mis['confidence']} | {', '.join(mis['issues'])} |\n"
        
        # Category distribution
        report += "\n## Category Distribution\n\n"
        report += "| Category | Total Files | Valid Files | Invalid Files | Success Rate |\n"
        report += "|----------|-------------|-------------|---------------|--------------|\n"
        
        for category, files in results["files_by_category"].items():
            total = len(files)
            valid = sum(1 for f in files if f["is_valid"])
            invalid = total - valid
            success_rate = (valid / total * 100) if total > 0 else 0
            
            report += f"| {category} | {total} | {valid} | {invalid} | {success_rate:.1f}% |\n"
        
        return report
    
    def save_validation_report(self, results: Dict, output_path: str = None):
        """Save validation report to file"""
        if output_path is None:
            output_path = self.base_output_dir / "categorization_validation_report.md"
        
        report_content = self.generate_validation_report(results)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(report_content)
        
        print(f"📄 Validation report saved to: {output_path}")
        return output_path
    
    def print_summary(self, results: Dict):
        """Print validation summary"""
        print(f"\n📊 Validation Summary:")
        print(f"   Total files: {results['total_files']}")
        print(f"   Valid: {results['valid_files']}")
        print(f"   Invalid: {results['invalid_files']}")
        print(f"   Success rate: {(results['valid_files'] / max(results['total_files'], 1) * 100):.1f}%")
        
        if results["misclassifications"]:
            print(f"\n⚠️  Potential misclassifications found: {len(results['misclassifications'])}")
            for mis in results["misclassifications"][:5]:  # Show first 5
                filename = Path(mis["file"]).name
                print(f"   - {filename}: {mis['current_category']} → {mis['suggested_category']} (confidence: {mis['confidence']})")
        
        print(f"\n📁 Detailed report saved to: {self.base_output_dir / 'categorization_validation_report.md'}")

def main():
    """Main function to run validation"""
    validator = CategorizationValidator()
    results = validator.validate_all_categorizations()
    validator.save_validation_report(results)
    validator.print_summary(results)

if __name__ == "__main__":
    main() 