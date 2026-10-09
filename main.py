"""File deduplication utility: lists duplicate files by content."""

import argparse, hashlib, sys
from pathlib import Path

def file_hash(p: Path) -> str:
    h = hashlib.sha256()
    with p.open('rb') as f:
        for chunk in iter(lambda: f.read(8192), b''):
            h.update(chunk)
    return h.hexdigest()

def find_duplicates(dir_path: Path):
    hashes = {}
    for p in dir_path.rglob('*'):
        if p.is_file():
            h = file_hash(p)
            hashes.setdefault(h, []).append(p)
    return {h: lst for h, lst in hashes.items() if len(lst) > 1}

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('directory', nargs='?', default='.', help='Directory to scan')
    args = parser.parse_args()
    dir_path = Path(args.directory).resolve()
    if not dir_path.is_dir():
        sys.exit(f'Not a directory: {dir_path}')
    duplicates = find_duplicates(dir_path)
    if not duplicates:
        print('No duplicates found.')
        return
    for h, files in duplicates.items():
        print(f'Duplicate group ({len(files)} files):')
        for f in files:
            print(f'  {f}')
        print()

if __name__ == '__main__':
    main()