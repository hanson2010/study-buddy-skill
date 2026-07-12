import os
import sys
from datetime import datetime
from PIL import Image

MAX_SIZE_MB = 2
MAX_SIZE_BYTES = MAX_SIZE_MB * 1024 * 1024
SUPPORTED_EXTENSIONS = ('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp')

def get_data_dir():
    return os.environ.get('STUDYBUDDY_DATA_DIR', os.path.expanduser('~/.studybuddy'))

def get_raw_dir(year=None, month=None):
    if year is None or month is None:
        now = datetime.now()
        year = now.year
        month = now.month
    data_dir = get_data_dir()
    raw_dir = os.path.join(data_dir, 'raw', str(year), f'{month:02d}')
    os.makedirs(raw_dir, exist_ok=True)
    return raw_dir

def compress_image(src_path, target_path, max_bytes=MAX_SIZE_BYTES):
    with Image.open(src_path) as img:
        img_format = img.format or 'JPEG'
        if img_format == 'PNG' and img.mode == 'RGBA':
            img_format = 'PNG'
        else:
            img_format = 'JPEG'
            if img.mode != 'RGB':
                img = img.convert('RGB')
        
        width, height = img.size
        quality = 95
        
        while True:
            temp_path = target_path + '.tmp'
            img.save(temp_path, format=img_format, quality=quality, optimize=True)
            
            if os.path.getsize(temp_path) <= max_bytes or quality <= 10:
                os.replace(temp_path, target_path)
                break
            
            quality -= 5
            if width > 2048 or height > 2048:
                width = int(width * 0.9)
                height = int(height * 0.9)
                img = img.resize((width, height), Image.Resampling.LANCZOS)
    
    return target_path

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

def process_image(filepath):
    if not os.path.exists(filepath):
        print(f'Error: File not found - {filepath}')
        return None
    
    file_ext = os.path.splitext(filepath)[1].lower()
    if file_ext not in SUPPORTED_EXTENSIONS:
        print(f'Skipping unsupported format - {filepath}')
        return None
    
    filesize = os.path.getsize(filepath)
    original_filename = os.path.basename(filepath)
    
    raw_dir = get_raw_dir()
    new_filename = get_unique_filename(raw_dir, original_filename)
    target_path = os.path.join(raw_dir, new_filename)
    
    if filesize > MAX_SIZE_BYTES:
        print(f'Compressing {filepath} ({filesize/1024/1024:.2f}MB) -> {target_path}')
        compress_image(filepath, target_path)
    else:
        print(f'Copying {filepath} ({filesize/1024/1024:.2f}MB) -> {target_path}')
        import shutil
        shutil.copy2(filepath, target_path)
    
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
        print('Usage: python image_processor.py <image_file> [<image_file> ...]')
        sys.exit(1)
    
    data_dir = get_data_dir()
    os.makedirs(data_dir, exist_ok=True)
    
    for filepath in sys.argv[1:]:
        result = process_image(filepath)
        if result:
            update_markdown_references(data_dir, filepath, result)

if __name__ == '__main__':
    main()