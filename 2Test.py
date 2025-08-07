import re
import unicodedata

def normalize_text(text: str) -> str:
    # Unicode normalization to fix weird characters
    text = unicodedata.normalize("NFKC", text)
    
    # Replace non-breaking spaces and tabs with regular space
    text = text.replace('\xa0', ' ')
    text = text.replace('\t', ' ')
    
    # Normalize smart quotes and dashes
    text = text.replace('“', '"').replace('”', '"')
    text = text.replace('’', "'")
    text = text.replace('–', '-')  # en dash
    text = text.replace('—', '-')  # em dash
    
    # Remove trailing spaces on each line (but keep line breaks)
    text = re.sub(r'[ \t]+$', '', text, flags=re.MULTILINE)
    
    # Normalize multiple spaces (but preserve single line breaks)
    text = re.sub(r'[ \t]{2,}', ' ', text)
    
    # Remove redundant empty lines (keep single blank line for paragraphs)
    text = re.sub(r'\n{3,}', '\n\n', text)
    
    # Strip leading/trailing whitespace
    text = text.strip()
    
    return text

# === File Paths ===
input_file_path = "raw_input.txt"          # Replace with your input file name
output_file_path = "normalized_output.txt" # Replace with your desired output name

# === Read, Normalize, Write ===
with open(input_file_path, 'r', encoding='utf-8') as infile:
    raw_text = infile.read()

cleaned_text = normalize_text(raw_text)

with open(output_file_path, 'w', encoding='utf-8') as outfile:
    outfile.write(cleaned_text)

print(f"✅ Normalized text saved to: {output_file_path}")
