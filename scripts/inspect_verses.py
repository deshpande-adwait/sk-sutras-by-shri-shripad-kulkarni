"""Inspection script for canonical data
"""
import json
import re
import sys

def main():
    sys.stdout.reconfigure(encoding='utf-8')
    with open('scripts/ten_new_sutras_canonical_data.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract all verses
    verses = re.findall(r'\"sanskrit_verse\":\s*\"([^\"]+)\"', content)
    print("Found verses:")
    for i, v in enumerate(verses, 1):
        print(f"  {i}: {v}")

if __name__ == '__main__':
    main()
