import os
import sys
from datetime import datetime

try:
    import pymupdf4llm
except ImportError:
    print('Error: pymupdf4llm is not installed. Please install it with "pip install pymupdf4llm".', file=sys.stderr)
    sys.exit(1)

try:
    import pymupdf
except ImportError:
    print('Error: pymupdf is not installed. Please install it with "pip install pymupdf".', file=sys.stderr)
    sys.exit(1)

MAX_SIZE_MB = 50
MAX_SIZE_BYTES = MAX_SIZE_MB * 1024 * 1024
SUPPORTED_EXTENSIONS = ('.pdf',)

def get_data_dir():
    data_dir = os.environ.get('STUDYBUDDY_DATA_DIR')
    if not data_dir:
        print('Error: STUDYBUDDY_DATA_DIR environment variable is not set. Please set it before using StudyBuddy.', file=sys.stderr)
        sys.exit(1)
    return data_dir

def get_raw_dir(year=None, month=None):
    if year is None or month is None:
        now = datetime.now()
        year = now.year
        month = now.month
    data_dir = get_data_dir()
    raw_dir = os.path.join(data_dir, 'raw', str(year), f'{month:02d}')
    os.makedirs(raw_dir, exist_ok=True)
    return raw_dir

def get_unique_filename(raw_dir, original_filename):
    base_name, file_ext = os.path.splitext(original_filename)
    target_path = os.path.join(raw_dir, original_filename)
    
    if not os.path.exists(target_path):
        return original_filename
    
    counter = 1
    while True:
        new_filename = f'{base_name}_{counter}{file_ext}'
        target_path = os.path.join(raw_dir, new_filename)
        if not os.path.exists(target_path):
            return new_filename
        counter += 1

def extract_pdf_text(filepath):
    try:
        md_text = pymupdf4llm.to_markdown(filepath, header=False, footer=False)
        doc = pymupdf.open(filepath)
        num_pages = len(doc)
        doc.close()
        return md_text.strip(), num_pages
    except Exception as e:
        print(f'Error extracting text from PDF: {e}', file=sys.stderr)
        return None, 0

def process_pdf(filepath):
    if not os.path.exists(filepath):
        print(f'Error: File not found - {filepath}')
        return None
    
    file_ext = os.path.splitext(filepath)[1].lower()
    if file_ext not in SUPPORTED_EXTENSIONS:
        print(f'Skipping unsupported format - {filepath}')
        return None
    
    filesize = os.path.getsize(filepath)
    if filesize > MAX_SIZE_BYTES:
        print(f'Warning: PDF file size ({filesize/1024/1024:.2f}MB) exceeds recommended limit of {MAX_SIZE_MB}MB')
    
    original_filename = os.path.basename(filepath)
    
    raw_dir = get_raw_dir()
    new_filename = get_unique_filename(raw_dir, original_filename)
    target_path = os.path.join(raw_dir, new_filename)
    
    import shutil
    print(f'Copying PDF {filepath} ({filesize/1024/1024:.2f}MB) -> {target_path}')
    shutil.copy2(filepath, target_path)
    
    text, num_pages = extract_pdf_text(filepath)
    if text:
        text_filename = os.path.splitext(new_filename)[0] + '_text.md'
        text_path = os.path.join(raw_dir, text_filename)
        with open(text_path, 'w', encoding='utf-8') as f:
            f.write(f'---\n')
            f.write(f'pdf_file: {new_filename}\n')
            f.write(f'pages: {num_pages}\n')
            f.write(f'---\n\n')
            f.write(text)
        print(f'Extracted text saved to: {text_filename}')
    
    rel_path = os.path.relpath(target_path, get_data_dir())
    print(f'Result: {rel_path}')
    return rel_path

def update_markdown_references(data_dir, old_path, new_rel_path):
    for root, dirs, files in os.walk(data_dir):
        for filename in files:
            if filename.endswith('.md'):
                md_path = os.path.join(root, filename)
                try:
                    with open(md_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    old_rel = os.path.relpath(old_path, os.path.dirname(md_path))
                    if old_rel in content or old_path in content:
                        content = content.replace(old_rel, new_rel_path)
                        content = content.replace(old_path, new_rel_path)
                        with open(md_path, 'w', encoding='utf-8') as f:
                            f.write(content)
                        print(f'Updated reference in: {md_path}')
                except Exception as e:
                    print(f'Error updating {md_path}: {e}')

def main():
    if len(sys.argv) < 2:
        print('Usage: python pdf_processor.py <pdf_file> [<pdf_file> ...]')
        sys.exit(1)
    
    data_dir = get_data_dir()
    os.makedirs(data_dir, exist_ok=True)
    
    for filepath in sys.argv[1:]:
        result = process_pdf(filepath)
        if result:
            update_markdown_references(data_dir, filepath, result)

if __name__ == '__main__':
    main()
