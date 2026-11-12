import sys
import re
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, r"C:\Users\deshp\.gemini\antigravity\scratch\sk-sutras-by-shri-shripad-kulkarni")
from scripts.ten_new_sutras_canonical_data import TEN_NEW_UDYOG_SUTRAS_CANON

print("=== REPETITION ANALYSIS ACROSS 10 SUTRAS ===\n")

# 1. Check the 4 common foundational statements
for key in ["doc01_mahadgrantha", "doc02_karyavritti17", "doc03_karyavritti05", "doc04_sant_tukaram"]:
    vals = [s["bharatiya_jnana_foundation"].get(key) for s in TEN_NEW_UDYOG_SUTRAS_CANON]
    is_identical = len(set(vals)) == 1
    print(f"Key: {key} -> All identical across 10 sutras? {is_identical}")
    print(f"  Sample value: {vals[0]}\n")

# 2. Check iks_scriptural_references across chapters
print("=== IKS SCRIPTURAL REFERENCES ===")
verse_occurrences = {}
for s in TEN_NEW_UDYOG_SUTRAS_CANON:
    s_idx = s["sutra_no"]
    raw_iks = s["bharatiya_jnana_foundation"]["iks_scriptural_references"]
    # Find traditions and verses
    traditions = re.findall(r"Tradition:\s*([^\n\r]+)", raw_iks)
    sanskrit_verses = re.findall(r"Sanskrit Verse:\s*([^\n\r]+)", raw_iks)
    print(f"Sutra {s_idx:02d} has {len(sanskrit_verses)} verses:")
    for t, v in zip(traditions, sanskrit_verses):
        t_clean = t.strip()
        v_clean = v.strip()
        print(f"  - [{t_clean}]: {v_clean[:60]}...")
        if v_clean not in verse_occurrences:
            verse_occurrences[v_clean] = {"tradition": t_clean, "chapters": []}
        verse_occurrences[v_clean]["chapters"].append(s_idx)
    print()

print("=== REPEATED VERSES SUMMARY ===")
for v, data in verse_occurrences.items():
    print(f"Verse ({data['tradition']}) appears in Chapters: {data['chapters']}")
    print(f"  Text: {v[:80]}...\n")
