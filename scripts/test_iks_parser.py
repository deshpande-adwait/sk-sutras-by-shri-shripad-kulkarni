import sys
import re

sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, r"C:\Users\deshp\.gemini\antigravity\scratch\sk-sutras-by-shri-shripad-kulkarni")
from scripts.ten_new_sutras_canonical_data import TEN_NEW_UDYOG_SUTRAS_CANON

def parse_iks_block(raw_text):
    items = []
    blocks = re.split(r'•\s*(?:\[\]:)?\s*Tradition:\s*', raw_text)
    for b in blocks:
        if not b.strip():
            continue
        lines = b.strip().split('\n')
        tradition = lines[0].strip()
        data = {'tradition': tradition}
        current_key = None
        current_val = []
        for line in lines[1:]:
            m = re.match(r'^(Sanskrit Verse|Enterprise Principle|English Meaning|Marathi Meaning|Themes):\s*(.*)', line.strip())
            if m:
                if current_key:
                    data[current_key] = ' '.join(current_val).strip()
                current_key = m.group(1).lower().replace(' ', '_')
                current_val = [m.group(2).strip()]
            else:
                if current_key:
                    current_val.append(line.strip())
        if current_key:
            data[current_key] = ' '.join(current_val).strip()
        items.append(data)
    return items

seen_verses = {}
for i, s in enumerate(TEN_NEW_UDYOG_SUTRAS_CANON, 1):
    raw = s['bharatiya_jnana_foundation']['iks_scriptural_references']
    parsed = parse_iks_block(raw)
    print(f"=== Chapter {i:02d} ({s['theme']}) ===")
    for p in parsed:
        v = p.get('sanskrit_verse', '').strip()
        trad = p.get('tradition', '')
        is_first = v not in seen_verses
        if is_first:
            seen_verses[v] = i
            print(f"  [FIRST-EXPEDITION - Ch {i:02d}] {trad} | Verse: {v[:40]}...")
        else:
            first_ch = seen_verses[v]
            print(f"  [SUBSEQUENT-NUANCE - Refer Ch {first_ch:02d}] {trad} | Verse: {v[:40]}...")
