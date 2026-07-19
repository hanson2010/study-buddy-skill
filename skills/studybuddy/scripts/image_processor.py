import os
import sys
import shutil

try:
    from PIL import Image
except ImportError:
    print('Error: Pillow is not installed. Please install it with "pip install Pillow".', file=sys.stderr)
    sys.exit(1)

from common import get_data_dir, get_raw_dir, get_unique_filename, update_markdown_references

MAX_SIZE_MB = 2
MAX_SIZE_BYTES = MAX_SIZE_MB * 1024 * 1024
SUPPORTED_EXTENSIONS = ('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp')


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


def process_image(filepath):
    if not os.path.exists(filepath):
        print(f'Error: File not found - {filepath}', file=sys.stderr)
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
        shutil.copy2(filepath, target_path)
    
    rel_path = os.path.relpath(target_path, get_data_dir())
    print(f'Result: {rel_path}')
    return rel_path


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
