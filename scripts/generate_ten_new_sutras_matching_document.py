"""
================================================================================
Script: scripts/generate_ten_new_sutras_matching_document.py
Author: Hiranyam AI Labs (https://hiranyamai.com/)
Project: SK Sutras - by Shri Shripad Kulkarni
Description: Generates the clean, authoritative Word document (.docx)
             containing EXCLUSIVELY the core requested components for the
             10 NEW Udyog Sutras in simple layman terms with ZERO technical jargon.
             Enforces continuous confidentiality footer on every page:
             "Proprietory and Confidential- Hiranyam AI Labs"
================================================================================
"""

import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from scripts.generate_clean_layman_manuscript import build_clean_layman_document

if __name__ == "__main__":
    build_clean_layman_document()
