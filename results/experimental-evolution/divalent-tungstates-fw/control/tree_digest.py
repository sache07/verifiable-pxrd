"""Digest of a folder: relative path and content hash of every file in sorted order (as new_run.py records it).

python tree_digest.py FOLDER   prints the digest; the installer runs it on EC2 after deploying a baseline folder.
"""
import hashlib
import sys
from pathlib import Path


def tree_digest(root):
    root = Path(root)
    files = sorted(p for p in root.rglob('*') if p.is_file() and '__pycache__' not in p.parts)
    digest = hashlib.sha256()
    for p in files:
        digest.update(str(p.relative_to(root)).encode() + b'\0' + hashlib.sha256(p.read_bytes()).hexdigest().encode() + b'\0')
    return digest.hexdigest()


if __name__ == '__main__':
    print(tree_digest(sys.argv[1]))
