import csv
import re

def clean_text(text):
    """Clean text for Excel compatibility"""
    if not text:
        return ""
    
    # Remove markdown formatting
    text = re.sub(r'\*\*(.*?)\*\*', r'\1', text)  # Remove **bold**
    text = re.sub(r'###\s*', '', text)  # Remove ### headers
    text = re.sub(r'✅\s*', '', text)  # Remove ✅ emoji
    text = re.sub(r'⚠️\s*', '', text)  # Remove ⚠️ emoji
    text = re.sub(r'##\s*', '', text)  # Remove ## headers
    
    # Replace line breaks with spaces
    text = text.replace('\n', ' ')
    text = text.replace('\r', ' ')
    
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text)
    text = text.strip()
    
    # Truncate if too long
    if len(text) > 30000:
        text = text[:30000] + "... [truncated]"
    
    return text

def fix_csv():
    """Fix the CSV file for Excel using proper CSV handling with multi-line support"""
    try:
        # Read the original CSV file with proper handling of multi-line fields
        rows = []
        with open('qa_pairs_expected_format.csv', 'r', encoding='utf-8') as f:
            # Use csv.reader with proper quoting to handle multi-line fields
            csv_reader = csv.reader(f, quoting=csv.QUOTE_MINIMAL)
            for row in csv_reader:
                if len(row) >= 2:  # Ensure we have at least question and answer
                    # Clean the answer field (second column)
                    row[1] = clean_text(row[1])
                rows.append(row)
        
        # Write the fixed CSV file using proper CSV writer
        with open('qa_pairs_excel_ready.csv', 'w', encoding='utf-8', newline='') as f:
            csv_writer = csv.writer(f, quoting=csv.QUOTE_ALL)
            csv_writer.writerows(rows)
        
        print("Fixed CSV created: qa_pairs_excel_ready.csv")
        print("This file should import properly into Excel with correct column separation.")
        print("All answers are now contained in a single column.")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    fix_csv() 