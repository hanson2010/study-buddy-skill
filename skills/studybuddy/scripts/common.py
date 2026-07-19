import os
import sys
import shutil
from datetime import datetime


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
                    print(f'Error updating {md_path}: {e}', file=sys.stderr)
