import os
import sys

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

from common import get_data_dir, get_raw_dir, get_unique_filename, update_markdown_references

MAX_SIZE_MB = 50
MAX_SIZE_BYTES = MAX_SIZE_MB * 1024 * 1024
SUPPORTED_EXTENSIONS = ('.pdf',)


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
        print(f'Error: File not found - {filepath}', file=sys.stderr)
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
    
    print(f'Copying PDF {filepath} ({filesize/1024/1024:.2f}MB) -> {target_path}')
    import shutil
    shutil.copy2(filepath, target_path)
    
    text, num_pages = extract_pdf_text(filepath)
    if text:
        text_filename = os.path.splitext(new_filename)[0] + '_text.md'
        text_path = os.path.join(raw_dir, text_filename)
        with open(text_path, 'w', encoding='utf-8') as f:
            f.write('---\n')
            f.write(f'pdf_file: {new_filename}\n')
            f.write(f'pages: {num_pages}\n')
            f.write('---\n\n')
            f.write(text)
        print(f'Extracted text saved to: {text_filename}')
    
    rel_path = os.path.relpath(target_path, get_data_dir())
    print(f'Result: {rel_path}')
    return rel_path


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