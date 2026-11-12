"""
================================================================================
Script: scripts/generate_editorial_refined_manuscript.py
Author: Hiranyam AI Labs (https://hiranyamai.com/)
Project: SK Sutras - by Shri Shripad Kulkarni
Description: Generates the Editorial Refined Edition of Shrimad Udyog Sutras
             (10 Canonical Sutras) implementing three critical editorial rules:
             1. Rule 1: Intelligent handling of repeated source references
                (concise chapter nuance + cross-reference to earlier chapter).
             2. Rule 2: Centralise the four common foundational statements
                in Front Matter Section 3, citing only chapter-specific
                statements in individual chapters.
             3. Rule 3: Shorten repeated introductory and editorial notes
                into crisp, natural chapter-specific phrasing.
             Maintains strict 7-part chapter framework, Sanskrit accuracy,
             zero technical jargon, and complete philosophical depth.
================================================================================
"""

import os
import re
import shutil
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

# Configure Windows UTF-8 console output
if sys.platform.startswith("win"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

import docx
from docx.enum.table import WD_ALIGN_VERTICAL, WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls
from docx.shared import Inches, Pt, RGBColor

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from scripts.ten_new_sutras_canonical_data import TEN_NEW_UDYOG_SUTRAS_CANON
from scripts.generate_reader_first_manuscript import DOS_AND_DONTS, TRANSLITERATIONS

# Output Targets
OUTPUT_DOCS_DIR = BASE_DIR / "docs" / "reader_first_edition"
OUTPUT_DOCS_DIR.mkdir(parents=True, exist_ok=True)
FILE_NAME = "Shrimad_Udyog_Sutras_10_Canonical_Sutras_Editorial_Refined.docx"

TARGET_OUTPUT = OUTPUT_DOCS_DIR / FILE_NAME
DROPBOX_DIR = Path(r"C:\Users\deshp\Dropbox\Hiranyam AI Labs")
DROPBOX_OUTPUT = DROPBOX_DIR / FILE_NAME

ARTIFACT_DIR = Path(r"C:\Users\deshp\.gemini\antigravity\brain\94293167-6c7d-4773-b091-412c085b8cdc")
ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)
ARTIFACT_OUTPUT = ARTIFACT_DIR / FILE_NAME

MANDATORY_FOOTER = "Proprietory and Confidential- Hiranyam AI Labs"

# Color Palette: Classical Scholarly Publication
C_MAROON = RGBColor(139, 0, 0)       # #8B0000 Primary Sacred Accent
C_NAVY = RGBColor(18, 52, 86)        # #123456 Secondary Deep Blue
C_SLATE = RGBColor(40, 45, 55)       # #282D37 Body Text
C_CHARCOAL = RGBColor(26, 32, 44)    # #1A202C High-Legibility Devanagari Text
C_GOLD = RGBColor(180, 115, 20)      # Highlighting Accent
C_GREEN = RGBColor(24, 134, 75)      # Ethical / DOs Accent
C_RED = RGBColor(185, 28, 28)        # Pitfall / DON'Ts Accent


def set_cell_background(cell, hex_color: str) -> None:
    """Sets background shading of a docx table cell."""
    tcPr = cell._element.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{hex_color}"/>')
    tcPr.append(shd)


def set_cell_margins(cell, top: int = 80, bottom: int = 80, left: int = 120, right: int = 120) -> None:
    """Sets cell padding in dxa units (1 pt = 20 dxa)."""
    tcPr = cell._element.get_or_add_tcPr()
    tcMar = parse_xml(
        f'<w:tcMar {nsdecls("w")}>'
        f'<w:top w:w="{top}" w:type="dxa"/>'
        f'<w:bottom w:w="{bottom}" w:type="dxa"/>'
        f'<w:left w:w="{left}" w:type="dxa"/>'
        f'<w:right w:w="{right}" w:type="dxa"/>'
        f'</w:tcMar>'
    )
    tcPr.append(tcMar)


def add_hyperlink(paragraph, url: str, text: str, color: str = "123456", underline: bool = True) -> Any:
    """Appends a clickable OpenXML hyperlink to a python-docx paragraph."""
    part = paragraph.part
    r_id = part.relate_to(url, docx.opc.constants.RELATIONSHIP_TYPE.HYPERLINK, is_external=True)

    hyperlink = parse_xml(
        f'<w:hyperlink {nsdecls("w")} r:id="{r_id}" '
        f'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"/>'
    )
    new_run = parse_xml(f'<w:r {nsdecls("w")}/>')
    rPr = parse_xml(f'<w:rPr {nsdecls("w")}/>')

    if color:
        c = parse_xml(f'<w:color {nsdecls("w")} w:val="{color}"/>')
        rPr.append(c)
    if underline:
        u = parse_xml(f'<w:u {nsdecls("w")} w:val="single"/>')
        rPr.append(u)

    new_run.append(rPr)
    new_run_text = parse_xml(f'<w:t {nsdecls("w")} xml:space="preserve">{text}</w:t>')
    new_run.append(new_run_text)
    hyperlink.append(new_run)
    paragraph._element.append(hyperlink)
    return hyperlink


# ==============================================================================
# RULE 2: THE FOUR COMMON FOUNDATIONAL STATEMENTS (CENTRAL DEFINITIONS)
# ==============================================================================
FOUR_FOUNDATIONAL_STATEMENTS = {
    "doc01_mahadgrantha": {
        "title": "उद्योग महाग्रंथ विचार (Enterprise Foundation & Nation Building)",
        "sanskrit": "उद्यमेन हि सिध्यन्ति कार्याणि न मनोरथैः। कौशलं धृतिः शक्तिः सहकार्यं च राष्ट्रवर्धनम्।",
        "transliteration": "udyamena hi sidhyanti kāryāṇi na manorathaiḥ | kauśalaṁ dhṛtiḥ śaktiḥ sahakāryaṁ ca rāṣṭravardhanam ||",
        "meaning_mr": "कोणतेही कार्य केवळ मनात विचार करून वा मनोराज्य करून सिद्धीस जात नाही; ते प्रत्यक्ष अविरत परिश्रमानेच साध्य होते. उद्योजकाने आपल्या अंगी असलेले कौशल्य, संकटात न डगमगणारी धृती (धैर्य), संघशक्ती आणि परस्पर सहकार्य यांच्या बळावर राष्ट्रउभारणीला हातभार लावला पाहिजे.",
        "meaning_en": "Enterprises and works are accomplished solely through persistent diligence and concerted effort, never through idle daydreams. Craft mastery, unwavering fortitude, unified organizational strength, and collective collaboration constitute the true foundation of national advancement.",
        "enterprise_principle": "Exhorts relentless execution, mastery of craft, perseverance, and corporate nation-building as the primary engine of value creation."
    },
    "doc02_karyavritti17": {
        "title": "नीतिपूर्ण व्यापार व आचारसंहिता (Ethical Trade & Righteous Governance)",
        "sanskrit": "धर्मसंमतः अर्थलाभः। लोककल्याणार्थं वाणिज्यम्। निष्कामभावेन उद्योगपरिपालनम्।",
        "transliteration": "dharmasaṁmataḥ arthalābhaḥ | lokakalyāṇārthaṁ vāṇijyam | niṣkāmabhāvena udyogaparipālanam ||",
        "meaning_mr": "उद्योगातील आर्थिक नफा हा सदैव धर्माला, नीतीला आणि कायद्याला संमत असला पाहिजे. व्यापाराचा अंतिम हेतू केवळ स्वहित नसून व्यापक लोककल्याण असावा. फळाच्या अतिलोभाशिवाय निष्काम कर्मयोगाच्या उदात्त भावनेने उद्योग चालवणे हीच शाश्वत आचारसंहिता आहे.",
        "meaning_en": "Material wealth and commercial profit must strictly conform to righteousness and ethical law. Trade and enterprise exist fundamentally for the welfare of society. Managing an enterprise with selfless stewardship and detachment constitutes enduring corporate governance.",
        "enterprise_principle": "Emphasizes lawful righteous wealth creation, ethical trade, social responsibility, and selfless trusteeship."
    },
    "doc03_karyavritti05": {
        "title": "स्वावलंबन व संकटात संयम (Self-Reliance & Crisis Resilience)",
        "sanskrit": "स्वावलम्बनं परमं सुखम्। आत्मसंयमः संकटे धैर्यम्।",
        "transliteration": "svāvalambanaṁ paramaṁ sukham | ātmasaṁyamaḥ saṁkaṭe dhairyam ||",
        "meaning_mr": "दुसऱ्यांवर अवलंबून न राहता स्वतःच्या पायावर उभे राहणे (स्वावलंबन) हेच सर्वात मोठे सुख, स्वातंत्र्य व सामर्थ्य आहे. बाजारातील अस्थिरता, मंदी किंवा अचानक उद्भवणाऱ्या संकटांच्या काळात तीव्र आत्मसंयम आणि अविचल धैर्य बाळगणे हाच उद्योजकाचा खरा विजय आहे.",
        "meaning_en": "Self-reliance is the highest happiness and autonomy; dependency breeds vulnerability. Rigorous self-discipline, internal emotional control, and steadfast courage during crises ensure enterprise survival and ultimate triumph.",
        "enterprise_principle": "Exhorts absolute self-reliance, capital discipline, emotional equilibrium, and gritty resilience under economic volatility."
    },
    "doc04_sant_tukaram": {
        "title": "संत तुकाराम महाराज विचार (Clean Wealth & Spiritual Stewardship)",
        "sanskrit": "जोडोनियां धन उत्तम व्यवहारे । उदास विचारे वेच करी ॥",
        "transliteration": "joḍoniyāṁ dhana uttama vyavahāre | udāsa vicāre veca karī ||",
        "meaning_mr": "संपत्ती कमावताना ती १००% उत्तम, पारदर्शक, सत्य आणि नैतिक व्यवहारानेच मिळवली पाहिजे; आणि तिचा विनियोग करताना किंवा समाजासाठी खर्च करताना त्यात कोणतीही आसक्ती न ठेवता उदास (अलिप्त, निर्मम, विश्वस्त) वृत्तीने वेच केला पाहिजे.",
        "meaning_en": "Amass wealth solely through impeccable, ethical, and lawful means; dispense and deploy that wealth with a detached, noble, and altruistic mindset of a trustee.",
        "enterprise_principle": "Wealth earned through absolute commercial integrity must be administered with detached social trusteeship."
    }
}

# ==============================================================================
# RULE 2: CHAPTER-SPECIFIC ALLOTMENT OF FOUNDATIONAL STATEMENTS
# (Prevents verbatim repetition of all 4 in every chapter; cites relevant only)
# ==============================================================================
CHAPTER_FOUNDATIONS_MAPPING = {
    1: {
        "anchors": ["doc01_mahadgrantha"],
        "chapter_nuance": "या पहिल्या उद्घाटनपर प्रकरणात 'उद्योगजिज्ञासा' आणि कर्माची सक्रिय बैठक मांडताना उद्योग महाग्रंथाचा 'उद्यमेन हि सिध्यन्ति' हा विचार मूलभूत प्रेरक ठरतो."
    },
    2: {
        "anchors": ["doc04_sant_tukaram"],
        "chapter_nuance": "कर्मातील उत्कट भक्ती (परमानुरक्ती) समजून घेताना संत तुकारामांचा 'उत्तम व्यवहार व उदास विचार' हा संस्कार कर्माचे रूपांतर पवित्र उपासनेत करतो."
    },
    3: {
        "anchors": ["doc02_karyavritti17"],
        "chapter_nuance": "कर्मभक्तीतून कार्य सिद्धीस जाण्यासाठी (प्रसाद) 'धर्मसंमत अर्थलाभ व लोककल्याणार्थ वाणिज्य' ही आचारसंहिता मूळ पायाभूत आधार बनते."
    },
    4: {
        "anchors": ["doc03_karyavritti05", "doc04_sant_tukaram"],
        "chapter_nuance": "फळाची आसक्ती न ठेवता निष्काम उद्यम व परम तृप्ती साधण्यासाठी 'स्वावलंबन' आणि 'अनासक्त विनियोग (उदास विचार)' यांचा सुंदर मिलाफ अनिवार्य आहे."
    },
    5: {
        "anchors": ["doc02_karyavritti17"],
        "chapter_nuance": "अहंकाराचा लोप करून विनीत ग्राहकसेवा करताना 'निष्कामभावेन उद्योगपरिपालनम्' ही वृत्ती नम्र उद्यमाचा पाया रचते."
    },
    6: {
        "anchors": ["doc01_mahadgrantha"],
        "chapter_nuance": "उद्योगनिष्ठेची परिपूर्णता कौशल्य, संकटातील धृती आणि सहकार्यातूनच साध्य होते, ज्यातून सर्व प्रयत्न सफल होतात."
    },
    7: {
        "anchors": ["doc03_karyavritti05"],
        "chapter_nuance": "उद्योग कोणत्याही बाह्य प्रलोभनाशिवाय स्वतःमध्येच परिपूर्ण व स्वायत्त होण्यासाठी 'स्वावलम्बनं परमं सुखम्' हे अधिष्ठान आधारभूत आहे."
    },
    8: {
        "anchors": ["doc02_karyavritti17", "doc04_sant_tukaram"],
        "chapter_nuance": "सर्व कर्मांचे अर्पण करणे म्हणजे व्यवसायाची साधने समाजाच्या कल्याणासाठी विश्वस्त भावनेने उपयोगात आणणे."
    },
    9: {
        "anchors": ["doc02_karyavritti17"],
        "chapter_nuance": "संस्थेतील उणिवा, गैरव्यवहार व दोषांचे क्षालन करण्यासाठी केवळ आणि केवळ 'धर्मसंमत अर्थलाभ' व नैतिकतेची कास धरणे आवश्यक आहे."
    },
    10: {
        "anchors": ["doc03_karyavritti05", "doc04_sant_tukaram"],
        "chapter_nuance": "अनैतिक प्रलोभने व तात्पुरते शॉर्टकट्स नाकारून एकाच धर्माचा आश्रय घेण्यासाठी आत्मसंयम आणि उत्तम व्यवहाराची निष्ठा अपरिहार्य आहे."
    }
}

# ==============================================================================
# RULE 3: CRISP, NATURAL CHAPTER-SPECIFIC INTRODUCTIONS & NOTES
# ==============================================================================
CHAPTER_INTRODUCTIONS = {
    1: "प्रकरणाचे मूळ अधिष्ठान: नारद भक्ती सूत्र १ ('अथातो भक्तिं व्याख्यास्यामः') व शांडिल्य भक्ती सूत्र १ ('अथातो भक्तिजिज्ञासा') या दोन प्राचीन सूत्रांवर हे प्रकरण आधारित आहे.",
    2: "प्रकरणाचे मूळ अधिष्ठान: नारद भक्ती सूत्र २ ('सा त्वस्मिन् परमप्रेमरूपा') व शांडिल्य भक्ती सूत्र २ ('सा परानुरक्तिरीश्वरे') या दोन प्रेमलक्षणांवर हे प्रकरण आधारित आहे.",
    3: "प्रकरणाचे मूळ अधिष्ठान: नारद भक्ती सूत्र ३ ('अमृतस्वरूपा च') व शांडिल्य भक्ती सूत्र ३ ('स च भक्तिप्रसादात्') या कृपा व अमरत्वाच्या तत्त्वांवर हे प्रकरण आधारित आहे.",
    4: "प्रकरणाचे मूळ अधिष्ठान: नारद भक्ती सूत्र ४ ('यल्लब्ध्वा पुमान् सिद्धो भवति...') व शांडिल्य भक्ती सूत्र ४ ('प्रारब्धक्षये परमं पदम्') या परम तृप्तीच्या वचनांवर हे प्रकरण आधारित आहे.",
    5: "प्रकरणाचे मूळ अधिष्ठान: नारद भक्ती सूत्र ५ ('यत्प्राप्य न किञ्चिद् वाञ्छति...') व शांडिल्य भक्ती सूत्र ५ ('नमस्कारश्च भक्त्या') या विनीत व निष्काम वचनांवर हे प्रकरण आधारित आहे.",
    6: "प्रकरणाचे मूळ अधिष्ठान: नारद भक्ती सूत्र ६ ('यज्ज्ञात्वा मत्तो भवति...') व शांडिल्य भक्ती सूत्र ६ ('भक्तिमतः सर्वं सफलं भवति') या परिपूर्ण सफलतेच्या वचनांवर हे प्रकरण आधारित आहे.",
    7: "प्रकरणाचे मूळ अधिष्ठान: नारद भक्ती सूत्र ७ ('सा न कामयमाना निरोधरूपत्वात्') व शांडिल्य भक्ती सूत्र ७ ('न क्रिया परप्रयोजनाभावात्') या स्वायत्त व निरोधरूप वचनांवर हे प्रकरण आधारित आहे.",
    8: "प्रकरणाचे मूळ अधिष्ठान: नारद भक्ती सूत्र ८ ('निरोधस्तु लोकवेदव्यापारन्यासः') व शांडिल्य भक्ती सूत्र ८ ('तन्न्यासश्च भक्तौ') या सर्वस्व अर्पण व संन्यास वचनांवर हे प्रकरण आधारित आहे.",
    9: "प्रकरणाचे मूळ अधिष्ठान: नारद भक्ती सूत्र ९ ('तस्मिन्ननन्यता तद्विरोधिषूदासीनता च') व शांडिल्य भक्ती सूत्र ९ ('पातकनाशनं च') या अनन्यता व दोषनिवारक वचनांवर हे प्रकरण आधारित आहे.",
    10: "प्रकरणाचे मूळ अधिष्ठान: नारद भक्ती सूत्र १० ('अन्याश्रयाणां त्यागोऽनन्यता') व शांडिल्य भक्ती सूत्र १० ('दैन्यं च शरणागतिः') या अनन्य आश्रय व शरणागतीच्या वचनांवर हे प्रकरण आधारित आहे."
}

# ==============================================================================
# RULE 1: CHAPTER-SPECIFIC NUANCE FOR SUBSEQUENT APPEARANCES OF IKS VERSES
# ==============================================================================
IKS_SUBSEQUENT_NUANCES = {
    # Bhartrihari Niti Shataka 68 (Nindantu nitinipuna...)
    ("Bhartrihari Niti Shataka", 2): (
        "प्रकरणाशी संबंधित विशेष पैलू: कर्मावर उत्कट प्रेम (परमानुरक्ती) असणारा उद्योजक लोकांच्या स्तुती-निंदेने विचलित न होता आपल्या ध्येयाशी एकनिष्ठ राहतो.",
        1
    ),
    ("Bhartrihari Niti Shataka", 4): (
        "प्रकरणाशी संबंधित विशेष पैलू: फळाच्या तात्कालिक परिणामांची (लक्ष्मी येवो वा जावो) चिंता न करता शांत चित्ताने कर्म करत राहणे हेच निष्काम कर्माचे खरे सामर्थ्य आहे.",
        1
    ),
    ("Bhartrihari Niti Shataka", 5): (
        "प्रकरणाशी संबंधित विशेष पैलू: स्तुतीने अहंकार न वाढू देता आणि निंदेने खचून न जाता शांतपणे ग्राहकसेवेत लीन राहणे म्हणजेच नम्र उद्यम.",
        1
    ),
    ("Bhartrihari Niti Shataka", 6): (
        "प्रकरणाशी संबंधित विशेष पैलू: बाजारातील तात्पुरते चढउतार किंवा लोकांची मते बदलली तरी आपल्या कार्यगुणवत्तेच्या व नीतीच्या मार्गावर अविचल राहणे हीच उद्योगनिष्ठा.",
        1
    ),
    ("Bhartrihari Niti Shataka", 7): (
        "प्रकरणाशी संबंधित विशेष पैलू: बाह्य फलप्राप्तीच्या प्रलोभनाशिवाय केवळ कार्याची स्वायत्त पूर्णता साधण्यासाठी नैतिक धैर्याने उभे राहणे.",
        1
    ),
    ("Bhartrihari Niti Shataka", 8): (
        "प्रकरणाशी संबंधित विशेष पैलू: नफा-तोट्याच्या द्वंद्वापलीकडे जाऊन सर्व कर्म व्यापक लोककल्याणासाठी अर्पण करण्याचे नैतिक धैर्य.",
        1
    ),
    ("Bhartrihari Niti Shataka", 9): (
        "प्रकरणाशी संबंधित विशेष पैलू: स्तुती-निंदेची पर्वा न करता संस्थेतील उणिवा व दोष दूर करण्यासाठी धर्माधिष्ठित कठोर निर्णय घेण्याचे सामर्थ्य.",
        1
    ),

    # Patanjali Yoga Sutras 1.33 (Maitri-karuna...)
    ("Patanjali Yoga Sutras", 2): (
        "प्रकरणाशी संबंधित विशेष पैलू: सहकाऱ्यांविषयी मैत्री व ग्राहकांविषयी करुणा बाळगल्याने कर्मातील उत्कटता निकोप राहते आणि व्यावसायिक संबंध समृद्ध होतात.",
        1
    ),
    ("Patanjali Yoga Sutras", 3): (
        "प्रकरणाशी संबंधित विशेष पैलू: चित्तप्रसन्नता लाभल्याशिवाय कर्माचे रूपांतर भक्तीत आणि ईश्वरी प्रसादात (सफलतेत) होऊ शकत नाही.",
        1
    ),
    ("Patanjali Yoga Sutras", 5): (
        "प्रकरणाशी संबंधित विशेष पैलू: नम्रतेचा पाया मैत्री व करुणेत आहे; अहंकार नष्ट झाल्यास आपोआप सर्वांशी सौहार्दाचे संबंध प्रस्थापित होतात.",
        1
    ),
    ("Patanjali Yoga Sutras", 6): (
        "प्रकरणाशी संबंधित विशेष पैलू: दीर्घकालीन गुणवत्तेची साधना करताना सहकाऱ्यांच्या यशाबद्दल मुदिता (आनंद) आणि अडथळ्यांविषयी उपेक्षा वृत्ती मनाला स्थिर ठेवते.",
        1
    ),
    ("Patanjali Yoga Sutras", 9): (
        "प्रकरणाशी संबंधित विशेष पैलू: न्यायनिवाडा करताना वैयक्तिक पूर्वग्रह न ठेवता मैत्री व करुणेच्या भावनेने दोषांचे परिमार्जन करणे.",
        1
    ),
    ("Patanjali Yoga Sutras", 10): (
        "प्रकरणाशी संबंधित विशेष पैलू: चित्त शांत ठेवून संपूर्ण नम्रतेने केवळ धर्माचा आश्रय घेणे, ज्यामुळे सर्व अनैतिक प्रलोभने निष्प्रभ ठरतात.",
        1
    ),

    # Isha Upanishad 1 (Isha vasyam...)
    ("Isha Upanishad", 3): (
        "प्रकरणाशी संबंधित विशेष पैलू: सृष्टीतील प्रत्येक साधन ईश्वराचे मानून त्याचा विनियोग केल्यास व्यवसायातील यश हा केवळ वैयक्तिक नफा न राहता 'ईश्वरी प्रसाद' बनतो.",
        2
    ),
    ("Isha Upanishad", 8): (
        "प्रकरणाशी संबंधित विशेष पैलू: ईश्वराच्या विश्वात कर्मार्पण करणे म्हणजेच उद्योगातील साधनसंपत्ती विश्वस्त (Trustee) म्हणून समाजासाठी वापरणे.",
        2
    ),
    ("Isha Upanishad", 9): (
        "प्रकरणाशी संबंधित विशेष पैलू: लोभाचा त्याग (मा गृधः) केल्याशिवाय संस्थेत पारदर्शक कारभार आणि नैतिक दोषनिवारण शक्य नाही.",
        2
    ),
    ("Isha Upanishad", 10): (
        "प्रकरणाशी संबंधित विशेष पैलू: सर्व काही ईश्वराचे आहे या विनम्र जाणिवेतून इतर सर्व गैरमार्गांचा आश्रय सोडून केवळ धर्मतत्त्वावर निष्ठा ठेवणे.",
        2
    ),

    # Kautilya Arthashastra 1.19.34 (Anutthane dhruvo nasah...)
    ("Kautilya Arthashastra", 4): (
        "प्रकरणाशी संबंधित विशेष पैलू: फळाची आसक्ती न ठेवताही उत्थान (सक्रियता) व दक्षतेमध्ये किंचितही ढिलाई न येऊ देणे म्हणजेच परिपूर्ण कर्म.",
        3
    ),
    ("Kautilya Arthashastra", 5): (
        "प्रकरणाशी संबंधित विशेष पैलू: नम्रतेचा अर्थ निष्क्रियता नव्हे; उत्थानाची पराकाष्ठा आणि वर्तनात विनम्रता यांचा सुंदर संगम म्हणजे नम्र उद्यम.",
        3
    ),
    ("Kautilya Arthashastra", 6): (
        "प्रकरणाशी संबंधित विशेष पैलू: सातत्यपूर्ण उत्थान आणि रोजची जागरूकता हीच उद्योगनिष्ठेची प्रत्यक्ष कसोटी आहे, ज्यातून शाश्वत यश प्राप्त होते.",
        3
    ),
    ("Kautilya Arthashastra", 7): (
        "प्रकरणाशी संबंधित विशेष पैलू: बाह्य प्रेरणेशिवाय स्वतःच्या आंतरिक प्रेरणेतून सतत कार्यरत राहणे (उत्थान) हीच स्वायत्त उद्योजकाची ओळख आहे.",
        3
    ),
    ("Kautilya Arthashastra", 10): (
        "प्रकरणाशी संबंधित विशेष पैलू: केवळ नशिबावर विसंबून न राहता सक्रिय उद्यम करणे आणि त्याच वेळी अंतिम आश्रय नीतीधर्माचा घेणे.",
        3
    ),
}


def parse_iks_block(raw_text: str) -> List[Dict[str, str]]:
    """Parses raw iks_scriptural_references text into individual structured records."""
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


def get_tradition_key(tradition_str: str) -> str:
    """Extracts base canonical tradition key from detailed tradition string."""
    t = tradition_str.lower()
    if "bhartrihari" in t and "68" in t:
        return "Bhartrihari Niti Shataka"
    if "patanjali" in t:
        return "Patanjali Yoga Sutras"
    if "isha upanishad" in t:
        return "Isha Upanishad"
    if "kautilya" in t:
        return "Kautilya Arthashastra"
    if "bhagavad gita" in t and ("3.20" in t or "chapter 3" in t):
        return "Bhagavad Gita 3.20"
    if "bhagavad gita" in t and ("2.47" in t or "chapter 2" in t):
        return "Bhagavad Gita 2.47"
    if "bhartrihari" in t and "27" in t:
        return "Bhartrihari Niti Shataka 27"
    if "vidura" in t:
        return "Vidura Niti"
    return tradition_str.split('(')[0].strip()


def build_editorial_refined_manuscript() -> Path:
    """
    Constructs the complete 10-chapter publication manuscript with:
    - Centralized foundational matrix in front matter (Rule 2)
    - Chapter-specific foundational citations (Rule 2)
    - Intelligent handling of repeated source references (Rule 1)
    - Shortened introductory and editorial notes (Rule 3)
    - Prominent translation box under every Udyoga Sutra
    - Strict 7-part pedagogical framework across all 10 chapters
    - Mandatory confidentiality footer on every page
    - Clickable link to https://hiranyamai.com/
    """
    print("=" * 80)
    print("GENERATING EDITORIAL REFINED MANUSCRIPT (SHRIMAD UDYOG SUTRAS)")
    print("=" * 80)

    doc = docx.Document()

    # Set Margins (0.8 inch all around)
    for section in doc.sections:
        section.top_margin = Inches(0.8)
        section.bottom_margin = Inches(0.8)
        section.left_margin = Inches(0.8)
        section.right_margin = Inches(0.8)

        # Mandatory Confidentiality Footer on every page
        footer = section.footer
        f_p = footer.paragraphs[0]
        f_p.text = MANDATORY_FOOTER
        f_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        for r in f_p.runs:
            r.font.name = "Georgia"
            r.font.size = Pt(8.5)
            r.font.color.rgb = RGBColor(120, 120, 120)

    # ==================== GRAND TITLE PAGE ====================
    t_p = doc.add_paragraph()
    t_p.paragraph_format.space_before = Pt(36)
    t_p.paragraph_format.space_after = Pt(4)
    t_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    t_run1 = t_p.add_run("॥ श्रीमद् उद्योग सूत्राणि ॥\n")
    t_run1.font.name = "Georgia"
    t_run1.font.size = Pt(26)
    t_run1.font.bold = True
    t_run1.font.color.rgb = C_MAROON

    sub_p = doc.add_paragraph()
    sub_p.paragraph_format.space_before = Pt(0)
    sub_p.paragraph_format.space_after = Pt(4)
    sub_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    sub_run1 = sub_p.add_run("SHRIMAD UDYOG SUTRAS\n")
    sub_run1.font.name = "Georgia"
    sub_run1.font.size = Pt(17)
    sub_run1.font.bold = True
    sub_run1.font.color.rgb = C_NAVY

    sub_run2 = sub_p.add_run("भारतीय ज्ञानपरंपरेवर अधिष्ठित आधुनिक उद्योग व व्यवस्थापन तत्त्वे — १० मूलभूत प्रकरणे\n")
    sub_run2.font.name = "Georgia"
    sub_run2.font.size = Pt(11)
    sub_run2.font.color.rgb = C_CHARCOAL

    sub_run3 = sub_p.add_run("(संपादकीय परिष्कृत आवृत्ती — Editorial Refined Edition)\n")
    sub_run3.font.name = "Georgia"
    sub_run3.font.size = Pt(10)
    sub_run3.font.italic = True
    sub_run3.font.bold = True
    sub_run3.font.color.rgb = C_GOLD

    # Metadata Box
    m_tbl = doc.add_table(rows=1, cols=1)
    m_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    m_cell = m_tbl.cell(0, 0)
    set_cell_background(m_cell, "F5F2EB")
    set_cell_margins(m_cell, top=100, bottom=100, left=140, right=140)
    m_p = m_cell.paragraphs[0]
    m_p.paragraph_format.line_spacing = 1.3
    m_p.paragraph_format.space_after = Pt(0)

    m_p.add_run("ग्रंथकार (Author): श्री श्रीपाद कुलकर्णी (Shri Shripad Kulkarni)\n")
    m_p.add_run("मार्गदर्शक तत्त्व: 'सूत्र लहान, विचार महान, निरूपण सुटसुटीत, संक्षिप्त आणि आचरण व्यावहारिक'\n")
    m_p.add_run(
        "सद्ग्रंथ प्रेरणा: नारद भक्ती सूत्रे, शांडिल्य भक्ती सूत्रे, श्रीमद्भगवद्गीता, कौटिलीय अर्थशास्त्र, "
        "संत तुकाराम महाराज अभंगगाथा, समर्थ रामदास दासबोध, ईशावास्योपनिषद, पतंजली योगसूत्रे, भर्तृहरी नीतिशतक व विदुरनीती\n"
    )
    m_p.add_run("प्रकाशन आवृत्ती: २०२६ | संपादकीय परिष्कृत संस्करण (Editorial Refined Edition)\n")
    m_p.add_run("संशोधन व संपादन सहाय्य: ")
    add_hyperlink(m_p, "https://hiranyamai.com/", "Powered by Hiranyam AI Labs", color="123456", underline=True)

    doc.add_page_break()

    # ==================== TABLE OF CONTENTS (अनुक्रमणिका) ====================
    toc_p = doc.add_paragraph()
    toc_p.paragraph_format.space_before = Pt(10)
    toc_p.paragraph_format.space_after = Pt(8)
    toc_run = toc_p.add_run("अनुक्रमणिका (Table of Contents)")
    toc_run.font.name = "Georgia"
    toc_run.font.size = Pt(16)
    toc_run.font.bold = True
    toc_run.font.color.rgb = C_MAROON

    toc_tbl = doc.add_table(rows=15, cols=2)
    toc_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    for r in toc_tbl.rows:
        r.cells[0].width = Inches(5.2)
        r.cells[1].width = Inches(1.8)

    front_items = [
        ("१. प्रस्तावना : हे पुस्तक का लिहिले? (Introduction — Why this book?)", "प्रवेश व पूर्वपीठिका"),
        ("२. 'उद्योग सूत्र' म्हणजे काय? (What is an Udyoga Sutra?)", "प्रवेश व पूर्वपीठिका"),
        ("३. ज्ञानस्रोत व सद्ग्रंथ परंपरा (Sources & Knowledge Foundations)", "प्रवेश व पूर्वपीठिका"),
        ("४. उद्योग सूत्रांची निर्मिती कशी झाली? (How Udyoga Sutras are Derived)", "प्रवेश व पूर्वपीठिका"),
        ("५. प्रत्येक प्रकरणाचे वाचन कसे करावे? (How to Read Each Chapter)", "प्रवेश व पूर्वपीठिका"),
    ]

    for idx, (title, section_name) in enumerate(front_items):
        c0 = toc_tbl.cell(idx, 0)
        c1 = toc_tbl.cell(idx, 1)
        set_cell_background(c0, "FBF9F5" if idx % 2 == 0 else "FFFFFF")
        set_cell_background(c1, "FBF9F5" if idx % 2 == 0 else "FFFFFF")
        set_cell_margins(c0, top=40, bottom=40, left=80, right=80)
        set_cell_margins(c1, top=40, bottom=40, left=80, right=80)
        p0 = c0.paragraphs[0]
        p1 = c1.paragraphs[0]
        p1.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        r0 = p0.add_run(title)
        r0.font.name = "Arial"
        r0.font.size = Pt(9.5)
        r0.font.bold = True
        r0.font.color.rgb = C_NAVY
        r1 = p1.add_run(section_name)
        r1.font.name = "Georgia"
        r1.font.size = Pt(8.5)
        r1.font.italic = True
        r1.font.color.rgb = C_SLATE

    target_sutras = TEN_NEW_UDYOG_SUTRAS_CANON[:10]
    for s_i, s_data in enumerate(target_sutras):
        row_idx = 5 + s_i
        c0 = toc_tbl.cell(row_idx, 0)
        c1 = toc_tbl.cell(row_idx, 1)
        set_cell_background(c0, "FBF9F5" if row_idx % 2 == 0 else "FFFFFF")
        set_cell_background(c1, "FBF9F5" if row_idx % 2 == 0 else "FFFFFF")
        set_cell_margins(c0, top=40, bottom=40, left=80, right=80)
        set_cell_margins(c1, top=40, bottom=40, left=80, right=80)
        p0 = c0.paragraphs[0]
        p1 = c1.paragraphs[0]
        p1.alignment = WD_ALIGN_PARAGRAPH.RIGHT

        s_no = s_data["sutra_no"]
        s_verse = s_data["new_udyog_sutra"]["sanskrit_verse"]
        r0 = p0.add_run(f"प्रकरण {s_no:02d} : {s_verse}")
        r0.font.name = "Georgia"
        r0.font.size = Pt(9.5)
        r0.font.bold = True
        r0.font.color.rgb = C_MAROON

        r1 = p1.add_run(f"उद्योग सूत्र {s_no}")
        r1.font.name = "Arial"
        r1.font.size = Pt(8.5)
        r1.font.color.rgb = C_NAVY

    doc.add_page_break()

    # ==================== FRONT MATTER SECTIONS ====================
    # Section 1: Introduction
    hp1 = doc.add_paragraph()
    hp1.paragraph_format.space_before = Pt(12)
    hp1.paragraph_format.space_after = Pt(4)
    hr1 = hp1.add_run("१. प्रस्तावना : हे पुस्तक का लिहिले? (Introduction — Why this book?)")
    hr1.font.name = "Georgia"
    hr1.font.size = Pt(13)
    hr1.font.bold = True
    hr1.font.color.rgb = C_MAROON

    p_intro1 = doc.add_paragraph(
        "भारतीय संस्कृतीमध्ये ज्ञानाची, चिंतनाची आणि आचरणाची एक अखंड, समृद्ध परंपरा चालत आलेली आहे. सहस्रो वर्षांपूर्वी आपल्या ऋषी-मुनींनी जीवनाच्या अंतिम सत्याचा शोध घेताना जे सिद्धांत मांडले, ते केवळ अध्यात्मापुरते मर्यादित नव्हते. मानवी मनाचे नियम, कार्यकुशलता, सचोटी, समर्पण आणि सामाजिक कल्याण या सर्व अंगांना त्यामध्ये स्पर्श करण्यात आला होता.\n\n"
        "आज एकविसाव्या शतकात जेव्हा आपण जागतिक व्यापार, स्टार्टअप्स, कॉर्पोरेट व्यवस्थापन आणि उद्योजकतेच्या युगात वावरत आहोत, तेव्हा बाह्य तंत्रज्ञान बदलले असले तरी मूलभूत मानवी प्रश्न तेच आहेत: संकटात मन स्थिर कसे ठेवावे? यशाच्या शिखरावर असताना नैतिक तोल कसा सांभाळावा? नफा मिळवताना समाजाचे कल्याण कसे साधावे? आणि आपल्या सहकाऱ्यांमध्ये कार्याविषयी उत्कट भक्ती कशी निर्माण करावी?\n\n"
        "हे पुस्तक या सर्व प्रश्नांची उत्तरे शोधण्यासाठी भारतीय ज्ञानपरंपरेतील दोन दीपस्तंभांकडे वळते: नारद भक्ती सूत्रे आणि शांडिल्य भक्ती सूत्रे. भक्तीच्या या प्रामाणिक सूत्रांचे मंथन करून आधुनिक उद्योजक, व्यवस्थापक आणि व्यावसायिकांसाठी आचरणात आणण्याजोगी '१० उद्योग सूत्रे' येथे सादर केली आहेत."
    )
    p_intro1.paragraph_format.space_after = Pt(6)
    p_intro1.paragraph_format.line_spacing = 1.15

    # Section 2: What is an Udyoga Sutra
    hp2 = doc.add_paragraph()
    hp2.paragraph_format.space_before = Pt(10)
    hp2.paragraph_format.space_after = Pt(4)
    hr2 = hp2.add_run("२. 'उद्योग सूत्र' म्हणजे काय? (What is an Udyoga Sutra?)")
    hr2.font.name = "Georgia"
    hr2.font.size = Pt(13)
    hr2.font.bold = True
    hr2.font.color.rgb = C_MAROON

    p_intro2 = doc.add_paragraph(
        "आपल्या परंपरेत 'सूत्र' या वाङ्मयप्रकाराला अनन्यसाधारण महत्त्व आहे. व्याकरणाच्या भाषेत सूत्राची व्याख्या करताना म्हटले आहे:\n"
        "'अल्पाक्षरमसंदिग्धं सारवद्विश्वतोमुखम् । अस्तोभमनवद्यं च सूत्रं सूत्रविदो विदुः ॥'\n"
        "म्हणजेच, कमीत कमी अक्षरे, संशयशून्य स्पष्टता, अथांग तत्त्वसार, सर्वतोमुखी उपयुक्तता आणि कोणताही निरर्थक शब्द नसलेली रचना म्हणजे सूत्र.\n\n"
        "या ग्रंथातील 'उद्योग सूत्र' म्हणजे आधुनिक व्यवसाय, नेतृत्व आणि उद्यमशीलतेचे मार्गदर्शक तत्त्व दर्शवणारे एक संक्षिप्त, लयबद्ध आणि स्मरणीय संस्कृत वचन आहे. 'सूत्र लहान, विचार महान' या सूत्रीय शिस्तीचे येथे काटेकोर पालन करण्यात आले आहे.\n\n"
        "सूत्र स्वतः आकाराने लहान असले तरी त्याचे 'निरूपण' (Exposition / Bhashya), त्याची 'सत्यकथा' (Real-life Case Studies) आणि दैनंदिन जीवनातील 'आचरण' (Actionable Steps) हे विस्तृत व सखोल आहेत. वाचक केवळ सूत्र वाचून थांबणार नाही, तर त्यामागील खोल विचार समजून घेऊन तो आपल्या उद्योगात प्रत्यक्ष अमलात आणू शकेल."
    )
    p_intro2.paragraph_format.space_after = Pt(6)
    p_intro2.paragraph_format.line_spacing = 1.15

    # Section 3: Sources & Knowledge Foundations (WITH RULE 2 CENTRAL SECTION)
    hp3 = doc.add_paragraph()
    hp3.paragraph_format.space_before = Pt(10)
    hp3.paragraph_format.space_after = Pt(4)
    hr3 = hp3.add_run("३. ज्ञानस्रोत व सद्ग्रंथ परंपरा (Sources & Knowledge Foundations)")
    hr3.font.name = "Georgia"
    hr3.font.size = Pt(13)
    hr3.font.bold = True
    hr3.font.color.rgb = C_MAROON

    p_intro3 = doc.add_paragraph(
        "हा ग्रंथ कोणत्याही कल्पनेवर किंवा हवेतील विचारांवर आधारलेला नाही. यातील प्रत्येक उद्योग सूत्र भारतीय ज्ञानपरंपरेतील मान्यताप्राप्त, प्रामाणिक सद्ग्रंथांवर आधारलेले आहे:\n"
        "• नारद भक्ती सूत्रे (Narada Bhakti Sutras): प्रेमाची, समर्पणाची आणि निःस्वार्थ सेवेची सर्वोच्च मानके देणारा आदिग्रंथ. यातील 'समर्पण' हे उद्योगात 'कामावरील अढळ निष्ठा' म्हणून अवतरते.\n"
        "• शांडिल्य भक्ती सूत्रे (Shandilya Bhakti Sutras): भक्तीला एक तार्किक, शिस्तबद्ध आणि बुद्धिमान शास्त्र म्हणून प्रस्थापित करणारा ग्रंथ. यातील 'जिज्ञासा' आणि 'परानुराग' हे उद्योजकीय संशोधनाचा पाया बनतात.\n"
        "• श्रीमद्भगवद्गीता (Bhagavad Gita): निष्काम कर्मयोग आणि 'लोकसंग्रह' (समाजाचे धारण-पोषण) यांची विश्वमान्य शिकवण.\n"
        "• कौटिलीय अर्थशास्त्र (Kautilya Arthashastra): सक्रिय उद्यमशीलता, अखंड दक्षता (उत्थान) आणि संपत्तीचे न्याय्य रक्षण.\n"
        "• संत तुकाराम महाराज अभंगगाथा: 'जोडोनियां धन उत्तम व्यवहारे । उदास विचारे वेच करी ॥' या वचनातून मिळणारा नैतिक व्यवहाराचा आदर्श.\n"
        "• समर्थ रामदास दासबोध: 'आधीं प्रचिती मग अनुमती' व 'सामर्थ्य आहे चळवळीचे' ही व्यावहारिक कार्यप्रणाली.\n"
        "• ईशावास्योपनिषद: 'तेन त्यक्तेन भुञ्जीथा' — त्यागपूर्वक उपभोग आणि विश्वस्त व्यवस्थापन (Trusteeship).\n"
        "• पतंजली योगसूत्रे: चार प्रकारची चित्तप्रसादन वृत्ती (मैत्री, करुणा, मुदिता, उपेक्षा), ताणमुक्ती आणि संकटातील चित्तस्थैर्य.\n"
        "• भर्तृहरी नीतिशतक व विदुरनीती: कोणत्याही दबावाखाली सत्याचा आणि न्यायाचा मार्ग न सोडणारा धीरोदात्त नैतिक कणखरपणा."
    )
    p_intro3.paragraph_format.space_after = Pt(6)
    p_intro3.paragraph_format.line_spacing = 1.15

    # ---------------- CENTRAL FOUNDATIONAL STATEMENTS BOX (RULE 2) ----------------
    cf_title = doc.add_paragraph()
    cf_title.paragraph_format.space_before = Pt(8)
    cf_title.paragraph_format.space_after = Pt(3)
    cfr = cf_title.add_run("॥ चार मूलभूत ग्रंथीय अधिष्ठाने (The Four Common Foundational Scriptural Anchors) ॥")
    cfr.font.name = "Georgia"
    cfr.font.size = Pt(11)
    cfr.font.bold = True
    cfr.font.color.rgb = C_GOLD

    cf_tbl = doc.add_table(rows=1, cols=1)
    cf_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    cf_cell = cf_tbl.cell(0, 0)
    set_cell_background(cf_cell, "FBF9F5")
    set_cell_margins(cf_cell, top=80, bottom=80, left=120, right=120)
    cfp = cf_cell.paragraphs[0]
    cfp.paragraph_format.space_after = Pt(0)
    cfp.paragraph_format.line_spacing = 1.2

    cf_lead = cfp.add_run(
        "खालील चार मूलभूत विधाने या ग्रंथातील सर्व दहा प्रकरणांचे सामायिक वैचारिक अधिष्ठान आहेत. पुस्तकातील पुनरावृत्ती टाळण्यासाठी "
        "ही चारही अधिष्ठाने येथे एकत्रितपणे सविस्तर स्पष्ट करण्यात आली आहेत. वैयक्तिक प्रकरणांमध्ये केवळ त्या प्रकरणाशी थेट संबंधित "
        "असलेल्या अधिष्ठानाचा संदर्भ देऊन वाचकाला या मध्यवर्ती ज्ञानस्रोताकडे निर्देशित केले आहे:\n\n"
    )
    cf_lead.font.name = "Georgia"
    cf_lead.font.size = Pt(8.5)
    cf_lead.font.italic = True
    cf_lead.font.color.rgb = C_SLATE

    for f_key in ["doc01_mahadgrantha", "doc02_karyavritti17", "doc03_karyavritti05", "doc04_sant_tukaram"]:
        f_info = FOUR_FOUNDATIONAL_STATEMENTS[f_key]
        r_ft = cfp.add_run(f"★ {f_info['title']}\n")
        r_ft.font.name = "Arial"
        r_ft.font.size = Pt(9.5)
        r_ft.font.bold = True
        r_ft.font.color.rgb = C_MAROON

        r_fsk = cfp.add_run(f"   मूळ वचन: {f_info['sanskrit']}\n")
        r_fsk.font.name = "Georgia"
        r_fsk.font.size = Pt(10)
        r_fsk.font.bold = True
        r_fsk.font.color.rgb = C_CHARCOAL

        r_ftr = cfp.add_run(f"   ({f_info['transliteration']})\n")
        r_ftr.font.name = "Arial"
        r_ftr.font.size = Pt(8)
        r_ftr.font.italic = True
        r_ftr.font.color.rgb = C_GOLD

        r_fmr = cfp.add_run(f"   मराठी अर्थ व उद्योगातील महत्त्व: {f_info['meaning_mr']}\n")
        r_fmr.font.name = "Georgia"
        r_fmr.font.size = Pt(8.5)
        r_fmr.font.color.rgb = C_SLATE

        r_fen = cfp.add_run(f"   English: {f_info['meaning_en']}\n\n")
        r_fen.font.name = "Arial"
        r_fen.font.size = Pt(8)
        r_fen.font.italic = True
        r_fen.font.color.rgb = C_SLATE

    cf_concl = cfp.add_run(
        "संपादकीय समन्वय: हा चतुःसूत्री पाया संपूर्ण ग्रंथात व्यापून राहिला आहे. प्रत्येक प्रकरणात या चारपैकी ज्या सूत्राचा संबंध "
        "त्या प्रकरणाच्या गाभ्याशी आहे, तेवढाच एक संदर्भ त्या प्रकरणात स्पष्ट करून उर्वरित सर्व विधानांसाठी या मध्यवर्ती अधिष्ठानाचा संदर्भ देण्यात आला आहे."
    )
    cf_concl.font.name = "Georgia"
    cf_concl.font.size = Pt(8.5)
    cf_concl.font.italic = True
    cf_concl.font.color.rgb = C_NAVY

    # Section 4: How Udyoga Sutras are Derived (WITH EDITORIAL CONVENTIONS)
    hp4 = doc.add_paragraph()
    hp4.paragraph_format.space_before = Pt(12)
    hp4.paragraph_format.space_after = Pt(4)
    hr4 = hp4.add_run("४. उद्योग सूत्रांची निर्मिती कशी झाली? (How Udyoga Sutras are Derived)")
    hr4.font.name = "Georgia"
    hr4.font.size = Pt(13)
    hr4.font.bold = True
    hr4.font.color.rgb = C_MAROON

    p_intro4 = doc.add_paragraph(
        "या ग्रंथातील नवीन उद्योग सूत्रांची रचना एका अत्यंत जबाबदार, पाच-टप्प्यांच्या अभ्यासपूर्ण पद्धतीतून झाली आहे:\n\n"
        "१. मूळ तत्त्वाचा शोध (Source Identification): नारद व शांडिल्य भक्ती सूत्रांमधील किंवा इतर सद्ग्रंथांमधील मूळ संस्कृत श्लोक व त्याचा मूळ संदर्भातील अर्थ समजून घेणे.\n"
        "२. समकालीन उद्योगाशी संवाद (Enterprise Dialogue): त्या तत्त्वाचा आजच्या व्यवसाय, नेतृत्व, कर्मचारी-संबंध आणि ग्राहकसेवेमधील खरा अन्वयार्थ काय होतो, याचा सखोल विचार करणे.\n"
        "३. सूत्रीय संक्षेपण (Sutra Formulation): त्या विचाराला अत्यंत संक्षिप्त, पाणिनीय व्याकरणाला धरून आणि स्मरणीय अशा नव्या संस्कृत उद्योग सूत्रात गुंफणे.\n"
        "४. बहुआयामी निरूपण (Comprehensive Exposition): सूत्राचे सुलभ मराठी विवेचन, ऐतिहासिक सत्यकथा आणि मानसिक संतुलनासाठी योगविचार मांडणे.\n"
        "५. प्रत्यक्ष आचारसंहिता (Actionable DOs & DON'Ts): आधुनिक संस्थापकांसाठी, व्यवस्थापकांसाठी आणि नेत्यांसाठी काय करावे व काय टाळावे, याचे स्पष्ट मार्गदर्शक नियम तयार करणे.\n\n"
        "महत्त्वाची संपादकीय नोंद: या ग्रंथातील 'मूळ आधार श्लोक' हे प्राचीन सद्ग्रंथांतील (नारद, शांडिल्य, गीता, उपनिषद इ.) जसेच्या तसे अधिकृत श्लोक आहेत. "
        "तर प्रत्येक प्रकरणातील 'नवीन उद्योग सूत्र' हे त्या प्राचीन तत्त्वांचे मंथन करून आधुनिक उद्योगासाठी नव्याने सूत्रबद्ध केलेले समकालीन संस्कृत सूत्र आहे. "
        "वाचकाने प्राचीन मूळ श्लोक आणि हे नवीन उद्योग सूत्र यांमधील हा महत्त्वाचा भेद ध्यानात घ्यावा."
    )
    p_intro4.paragraph_format.space_after = Pt(6)
    p_intro4.paragraph_format.line_spacing = 1.15

    # Section 5: How to Read Each Chapter
    hp5 = doc.add_paragraph()
    hp5.paragraph_format.space_before = Pt(10)
    hp5.paragraph_format.space_after = Pt(4)
    hr5 = hp5.add_run("५. प्रत्येक प्रकरणाचे वाचन कसे करावे? (How to Read Each Chapter)")
    hr5.font.name = "Georgia"
    hr5.font.size = Pt(13)
    hr5.font.bold = True
    hr5.font.color.rgb = C_MAROON

    p_intro5 = doc.add_paragraph(
        "वाचकाला प्रत्येक प्रकरणात एका अत्यंत नैसर्गिक, शिस्तबद्ध आणि सुसंगत वाचन-प्रवासाचा अनुभव यावा, यासाठी संपूर्ण पुस्तकात सात-भागांचा एकच प्रमाणबद्ध क्रम ठेवण्यात आला आहे:\n\n"
        "पायरी १ — मूळ आधार आणि संदर्भ श्लोक (Source Foundation): प्रथम मूळ सद्ग्रंथातील श्लोक, त्यांचा सरळ अर्थ आणि त्यांचा मूळ संदर्भ.\n"
        "पायरी २ — मूळ तत्त्वाकडून उद्योग सूत्राकडे (Derivation Bridge): त्या मूळ विचारातून आधुनिक उद्योग सूत्राची प्रेरणा कशी मिळाली, याचा वैचारिक सेतू.\n"
        "पायरी ३ — नवीन उद्योग सूत्र व सरळ अर्थ (New Udyoga Sutra & Translation): नव्याने रचलेले संस्कृत उद्योग सूत्र, त्याचे ठळक मराठी व इंग्रजी भाषांतर आणि व्याकरण.\n"
        "पायरी ४ — सविस्तर विवेचन व निरूपण (Detailed Exposition & Bhashya): सूत्राचा सखोल, सुटसुटीत तात्विक व व्यावहारिक अर्थ.\n"
        "पायरी ५ — व्यावहारिक उपयोजन व सत्यकथा (Practical Case Studies & Yoga): जागतिक व भारतीय उद्योगजगतातील सत्यकथा आणि पतंजली योगविचारातून मानसिक ताणमुक्ती.\n"
        "पायरी ६ — काय करावे आणि काय टाळावे (DOs & DON'Ts): आधुनिक उद्योगासाठी नेमकी, आचरणात आणण्याजोगी आचारसंहिता.\n"
        "पायरी ७ — चिंतन व अंतिम सूत्रसार (Reflection & Key Takeaway): अंतर्मुख करणारा प्रश्न आणि एका ओळीचा आचरण मंत्र."
    )
    p_intro5.paragraph_format.space_after = Pt(6)
    p_intro5.paragraph_format.line_spacing = 1.15

    doc.add_page_break()

    # ==================== TEN CANONICAL SUTRA CHAPTERS ====================
    seen_iks_verses: Dict[str, int] = {}

    for item in target_sutras:
        s_idx = item["sutra_no"]
        theme = item["theme"]
        mp = item["matching_pair"]
        bjf = item["bharatiya_jnana_foundation"]
        nus = item["new_udyog_sutra"]
        dnd = DOS_AND_DONTS.get(s_idx, DOS_AND_DONTS[1])

        # ---------------- CHAPTER BANNER ----------------
        ch_tbl = doc.add_table(rows=1, cols=1)
        ch_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        ch_cell = ch_tbl.cell(0, 0)
        set_cell_background(ch_cell, "123456")
        set_cell_margins(ch_cell, top=90, bottom=90, left=140, right=140)
        ch_p = ch_cell.paragraphs[0]
        ch_p.paragraph_format.space_after = Pt(0)
        ch_run1 = ch_p.add_run(f"॥ प्रकरण {s_idx:02d} ॥\n")
        ch_run1.font.name = "Georgia"
        ch_run1.font.size = Pt(11)
        ch_run1.font.bold = True
        ch_run1.font.color.rgb = C_GOLD
        ch_run2 = ch_p.add_run(f"उद्योग सूत्र {s_idx:02d} : {nus['sanskrit_verse']}\n")
        ch_run2.font.name = "Georgia"
        ch_run2.font.size = Pt(13)
        ch_run2.font.bold = True
        ch_run2.font.color.rgb = RGBColor(255, 255, 255)
        ch_run3 = ch_p.add_run(f"विषयसूत्र: {theme}")
        ch_run3.font.name = "Arial"
        ch_run3.font.size = Pt(8.5)
        ch_run3.font.italic = True
        ch_run3.font.color.rgb = RGBColor(220, 230, 242)

        # ---------------- SECTION 1: SOURCE FOUNDATION (SOURCE FIRST) ----------------
        s1_title = doc.add_paragraph()
        s1_title.paragraph_format.space_before = Pt(10)
        s1_title.paragraph_format.space_after = Pt(2)
        r_s1 = s1_title.add_run("१. मूळ आधार आणि संदर्भ श्लोक (Foundational Source Verses)")
        r_s1.font.name = "Arial"
        r_s1.font.size = Pt(10.5)
        r_s1.font.bold = True
        r_s1.font.color.rgb = C_MAROON

        # RULE 3: Crisp Chapter-Specific Lead-in
        s1_intro = doc.add_paragraph()
        s1_intro.paragraph_format.space_before = Pt(2)
        s1_intro.paragraph_format.space_after = Pt(4)
        ch_intro_text = CHAPTER_INTRODUCTIONS.get(s_idx, "या प्रकरणातील तत्त्वाचा मूळ आधार खालील प्राचीन सूत्रांवर अधिष्ठित आहे:")
        r_s1_intro = s1_intro.add_run(ch_intro_text)
        r_s1_intro.font.name = "Georgia"
        r_s1_intro.font.size = Pt(9)
        r_s1_intro.font.italic = True
        r_s1_intro.font.color.rgb = C_SLATE

        # Two-Column Matching Pair Table
        p_tbl = doc.add_table(rows=2, cols=2)
        p_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        for row in p_tbl.rows:
            row.cells[0].width = Inches(3.5)
            row.cells[1].width = Inches(3.5)

        # Narada Source Column
        c_n_hdr = p_tbl.cell(0, 0)
        set_cell_background(c_n_hdr, "8B0000")
        set_cell_margins(c_n_hdr, top=50, bottom=50, left=90, right=90)
        p1 = c_n_hdr.paragraphs[0]
        p1.paragraph_format.space_after = Pt(0)
        r1 = p1.add_run(f"नारद भक्ती सूत्र {mp['narada']['sutra_no']} (Narada Bhakti Sutra #{mp['narada']['sutra_no']})")
        r1.font.name = "Arial"
        r1.font.size = Pt(9)
        r1.font.bold = True
        r1.font.color.rgb = RGBColor(255, 255, 255)

        c_n_body = p_tbl.cell(1, 0)
        set_cell_background(c_n_body, "FBF9F5")
        set_cell_margins(c_n_body, top=60, bottom=60, left=90, right=90)
        p_nb = c_n_body.paragraphs[0]
        p_nb.paragraph_format.space_after = Pt(0)
        r_ns = p_nb.add_run(f"{mp['narada']['sanskrit']}\n")
        r_ns.font.name = "Georgia"
        r_ns.font.size = Pt(11)
        r_ns.font.bold = True
        r_ns.font.color.rgb = C_MAROON

        r_ntr = p_nb.add_run(f"({TRANSLITERATIONS['narada'].get(s_idx, '')})\n\n")
        r_ntr.font.name = "Arial"
        r_ntr.font.size = Pt(8)
        r_ntr.font.italic = True
        r_ntr.font.color.rgb = C_GOLD

        r_nm_lbl = p_nb.add_run("मराठी अर्थ: ")
        r_nm_lbl.font.name = "Georgia"
        r_nm_lbl.font.size = Pt(9)
        r_nm_lbl.font.bold = True
        r_nm_lbl.font.color.rgb = C_MAROON
        r_nm_val = p_nb.add_run(f"{mp['narada']['meaning_mr']}\n\n")
        r_nm_val.font.name = "Georgia"
        r_nm_val.font.size = Pt(9)
        r_nm_val.font.color.rgb = C_CHARCOAL

        r_ne_lbl = p_nb.add_run("English: ")
        r_ne_lbl.font.name = "Arial"
        r_ne_lbl.font.size = Pt(8.5)
        r_ne_lbl.font.bold = True
        r_ne_lbl.font.color.rgb = C_NAVY
        r_ne_val = p_nb.add_run(f"{mp['narada']['meaning_en']}")
        r_ne_val.font.name = "Arial"
        r_ne_val.font.size = Pt(8.5)
        r_ne_val.font.italic = True
        r_ne_val.font.color.rgb = C_SLATE

        # Shandilya Source Column
        c_s_hdr = p_tbl.cell(0, 1)
        set_cell_background(c_s_hdr, "123456")
        set_cell_margins(c_s_hdr, top=50, bottom=50, left=90, right=90)
        p2 = c_s_hdr.paragraphs[0]
        p2.paragraph_format.space_after = Pt(0)
        r2 = p2.add_run(f"शांडिल्य भक्ती सूत्र {mp['shandilya']['sutra_no']} (Shandilya Bhakti Sutra #{mp['shandilya']['sutra_no']})")
        r2.font.name = "Arial"
        r2.font.size = Pt(9)
        r2.font.bold = True
        r2.font.color.rgb = RGBColor(255, 255, 255)

        c_s_body = p_tbl.cell(1, 1)
        set_cell_background(c_s_body, "FBF9F5")
        set_cell_margins(c_s_body, top=60, bottom=60, left=90, right=90)
        p_sb = c_s_body.paragraphs[0]
        p_sb.paragraph_format.space_after = Pt(0)
        r_ss = p_sb.add_run(f"{mp['shandilya']['sanskrit']}\n")
        r_ss.font.name = "Georgia"
        r_ss.font.size = Pt(11)
        r_ss.font.bold = True
        r_ss.font.color.rgb = C_NAVY

        r_str = p_sb.add_run(f"({TRANSLITERATIONS['shandilya'].get(s_idx, '')})\n\n")
        r_str.font.name = "Arial"
        r_str.font.size = Pt(8)
        r_str.font.italic = True
        r_str.font.color.rgb = C_GOLD

        r_sm_lbl = p_sb.add_run("मराठी अर्थ: ")
        r_sm_lbl.font.name = "Georgia"
        r_sm_lbl.font.size = Pt(9)
        r_sm_lbl.font.bold = True
        r_sm_lbl.font.color.rgb = C_MAROON
        r_sm_val = p_sb.add_run(f"{mp['shandilya']['meaning_mr']}\n\n")
        r_sm_val.font.name = "Georgia"
        r_sm_val.font.size = Pt(9)
        r_sm_val.font.color.rgb = C_CHARCOAL

        r_se_lbl = p_sb.add_run("English: ")
        r_se_lbl.font.name = "Arial"
        r_se_lbl.font.size = Pt(8.5)
        r_se_lbl.font.bold = True
        r_se_lbl.font.color.rgb = C_NAVY
        r_se_val = p_sb.add_run(f"{mp['shandilya']['meaning_en']}")
        r_se_val.font.name = "Arial"
        r_se_val.font.size = Pt(8.5)
        r_se_val.font.italic = True
        r_se_val.font.color.rgb = C_SLATE

        # Thematic Harmony Note
        p_harm = doc.add_paragraph()
        p_harm.paragraph_format.space_before = Pt(4)
        p_harm.paragraph_format.space_after = Pt(4)
        r_hl = p_harm.add_run("दोन्ही संदर्भांमधील समान वैचारिक सूत्र (Harmonious Source Insight): ")
        r_hl.font.name = "Arial"
        r_hl.font.size = Pt(8.5)
        r_hl.font.bold = True
        r_hl.font.color.rgb = C_GOLD
        r_ht = p_harm.add_run(mp["thematic_harmony"])
        r_ht.font.name = "Georgia"
        r_ht.font.size = Pt(8.5)
        r_ht.font.color.rgb = C_SLATE

        # ---------------- BHARATIYA KNOWLEDGE BASE FOUNDATIONS (RULE 1 & RULE 2) ----------------
        f_tbl = doc.add_table(rows=1, cols=1)
        f_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        f_cell = f_tbl.cell(0, 0)
        set_cell_background(f_cell, "F5F2EB")
        set_cell_margins(f_cell, top=60, bottom=60, left=100, right=100)
        fp = f_cell.paragraphs[0]
        fp.paragraph_format.space_after = Pt(0)
        fr1 = fp.add_run("भारतीय ज्ञान परंपरा व सद्ग्रंथ विचार (Bharatiya Wisdom Foundations):\n")
        fr1.font.name = "Arial"
        fr1.font.size = Pt(9)
        fr1.font.bold = True
        fr1.font.color.rgb = C_NAVY

        # RULE 2 IMPLEMENTATION: Retain only chapter-specific foundational anchor
        f_map = CHAPTER_FOUNDATIONS_MAPPING.get(s_idx, {"anchors": ["doc01_mahadgrantha"], "chapter_nuance": ""})
        r_ch_anchor_hdr = fp.add_run("• या प्रकरणाशी संबंधित मूलभूत ग्रंथीय अधिष्ठान:\n")
        r_ch_anchor_hdr.font.name = "Georgia"
        r_ch_anchor_hdr.font.size = Pt(8.5)
        r_ch_anchor_hdr.font.bold = True
        r_ch_anchor_hdr.font.color.rgb = C_MAROON

        for a_key in f_map["anchors"]:
            a_data = FOUR_FOUNDATIONAL_STATEMENTS[a_key]
            r_av = fp.add_run(f"  ★ {a_data['title']}: {a_data['sanskrit']}\n")
            r_av.font.name = "Georgia"
            r_av.font.size = Pt(8.5)
            r_av.font.bold = True
            r_av.font.color.rgb = C_CHARCOAL

        r_anuance = fp.add_run(f"  प्रकरणाशी विशेष संदर्भ: {f_map['chapter_nuance']}\n")
        r_anuance.font.name = "Georgia"
        r_anuance.font.size = Pt(8)
        r_anuance.font.color.rgb = C_SLATE

        r_across = fp.add_run("  (चारही मूलभूत ग्रंथीय अधिष्ठानांच्या सविस्तर निरूपणासाठी पहा: ग्रंथारंभीचे 'ज्ञानस्रोत व सद्ग्रंथ परंपरा' पृष्ठ)\n\n")
        r_across.font.name = "Georgia"
        r_across.font.size = Pt(8)
        r_across.font.italic = True
        r_across.font.color.rgb = C_GOLD

        # RULE 1 IMPLEMENTATION: Intelligent handling of repeated IKS references
        raw_iks = bjf.get('iks_scriptural_references', '')
        parsed_iks = parse_iks_block(raw_iks)

        r_iks_hdr = fp.add_run("• प्राचीन सद्ग्रंथ संदर्भ (Ancient Scriptural Verses):\n")
        r_iks_hdr.font.name = "Georgia"
        r_iks_hdr.font.size = Pt(8.5)
        r_iks_hdr.font.bold = True
        r_iks_hdr.font.color.rgb = C_NAVY

        for iks_item in parsed_iks:
            v_text = iks_item.get('sanskrit_verse', '').strip()
            trad = iks_item.get('tradition', '').strip()
            trad_key = get_tradition_key(trad)

            is_first_occurrence = v_text not in seen_iks_verses

            if is_first_occurrence:
                # FIRST OCCURRENCE: Full presentation
                seen_iks_verses[v_text] = s_idx

                r_iv = fp.add_run(f"  [१] {trad}\n")
                r_iv.font.name = "Arial"
                r_iv.font.size = Pt(8.5)
                r_iv.font.bold = True
                r_iv.font.color.rgb = C_MAROON

                r_isk = fp.add_run(f"      श्लोक: {v_text}\n")
                r_isk.font.name = "Georgia"
                r_isk.font.size = Pt(9)
                r_isk.font.bold = True
                r_isk.font.color.rgb = C_CHARCOAL

                if iks_item.get('marathi_meaning'):
                    r_imm = fp.add_run(f"      मराठी अर्थ: {iks_item['marathi_meaning']}\n")
                    r_imm.font.name = "Georgia"
                    r_imm.font.size = Pt(8)
                    r_imm.font.color.rgb = C_SLATE

                if iks_item.get('english_meaning'):
                    r_ien = fp.add_run(f"      English: {iks_item['english_meaning']}\n")
                    r_ien.font.name = "Arial"
                    r_ien.font.size = Pt(8)
                    r_ien.font.italic = True
                    r_ien.font.color.rgb = C_SLATE

                if iks_item.get('enterprise_principle'):
                    r_iep = fp.add_run(f"      उद्यम तत्त्व (Enterprise Principle): {iks_item['enterprise_principle']}\n\n")
                    r_iep.font.name = "Georgia"
                    r_iep.font.size = Pt(8)
                    r_iep.font.color.rgb = C_NAVY
            else:
                # SUBSEQUENT OCCURRENCE: Retain shloka & citation, provide chapter-specific focus + cross-reference
                first_ch = seen_iks_verses[v_text]
                nuance_info = IKS_SUBSEQUENT_NUANCES.get(
                    (trad_key, s_idx),
                    (f"प्रकरणाशी संबंधित विशेष पैलू: या सूत्रातील तत्त्व या प्रकरणाच्या उद्योग सूत्राला पूरक अधिष्ठान देते.", first_ch)
                )
                nuance_text, ref_ch = nuance_info

                r_iv = fp.add_run(f"  [२] {trad}\n")
                r_iv.font.name = "Arial"
                r_iv.font.size = Pt(8.5)
                r_iv.font.bold = True
                r_iv.font.color.rgb = C_NAVY

                r_isk = fp.add_run(f"      श्लोक: {v_text}\n")
                r_isk.font.name = "Georgia"
                r_isk.font.size = Pt(9)
                r_isk.font.bold = True
                r_isk.font.color.rgb = C_CHARCOAL

                r_inuance = fp.add_run(f"      {nuance_text}\n")
                r_inuance.font.name = "Georgia"
                r_inuance.font.size = Pt(8)
                r_inuance.font.color.rgb = C_SLATE

                r_iref = fp.add_run(f"      (सविस्तर मूळ अर्थ व विश्लेषणासाठी पहा: प्रकरण {ref_ch:02d})\n\n")
                r_iref.font.name = "Georgia"
                r_iref.font.size = Pt(8)
                r_iref.font.italic = True
                r_iref.font.color.rgb = C_GOLD

        # ---------------- SECTION 2: DERIVATION / CONNECTION ----------------
        d_title = doc.add_paragraph()
        d_title.paragraph_format.space_before = Pt(8)
        d_title.paragraph_format.space_after = Pt(2)
        r_dt = d_title.add_run("२. मूळ तत्त्वाकडून उद्योग सूत्राकडे (From the Source Principle to an Udyoga Sutra)")
        r_dt.font.name = "Arial"
        r_dt.font.size = Pt(10.5)
        r_dt.font.bold = True
        r_dt.font.color.rgb = C_MAROON

        d_box = doc.add_table(rows=1, cols=1)
        d_box.alignment = WD_TABLE_ALIGNMENT.CENTER
        d_cell = d_box.cell(0, 0)
        set_cell_background(d_cell, "FBF9F5")
        set_cell_margins(d_cell, top=60, bottom=60, left=100, right=100)
        dp = d_cell.paragraphs[0]
        dp.paragraph_format.space_after = Pt(0)
        
        dr1 = dp.add_run("वैचारिक सेतू व आधुनिक उद्यम निष्पत्ती (Philosophical Bridge & Modern Synthesis):\n")
        dr1.font.name = "Arial"
        dr1.font.size = Pt(9)
        dr1.font.bold = True
        dr1.font.color.rgb = C_NAVY

        phil_text = nus.get("philosophical_foundation_mr", "")
        # RULE 3: Shortened, natural editorial bridge note
        dr2 = dp.add_run(
            f"{phil_text}\n\n"
            f"टीप: वरील प्राचीन सूत्रांच्या मंथनातून आधुनिक उद्योजकतेसाठी हे समकालीन 'उद्योग सूत्र' नव्याने सूत्रबद्ध केले आहे."
        )
        dr2.font.name = "Georgia"
        dr2.font.size = Pt(8.5)
        dr2.font.color.rgb = C_SLATE

        # ---------------- SECTION 3: NEWLY FORMULATED UDYOGA SUTRA ----------------
        s_title = doc.add_paragraph()
        s_title.paragraph_format.space_before = Pt(8)
        s_title.paragraph_format.space_after = Pt(2)
        r_st = s_title.add_run("३. नवीन उद्योग सूत्र व सरळ अर्थ (The Newly Formulated Udyoga Sutra & Translation)")
        r_st.font.name = "Arial"
        r_st.font.size = Pt(10.5)
        r_st.font.bold = True
        r_st.font.color.rgb = C_MAROON

        # Shloka Box
        sh_tbl = doc.add_table(rows=1, cols=1)
        sh_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        sh_cell = sh_tbl.cell(0, 0)
        set_cell_background(sh_cell, "FFFBF0")
        set_cell_margins(sh_cell, top=80, bottom=80, left=120, right=120)
        shp = sh_cell.paragraphs[0]
        shp.alignment = WD_ALIGN_PARAGRAPH.CENTER
        shp.paragraph_format.space_after = Pt(0)
        sutra_verse_clean = nus['sanskrit_verse'].strip()
        shr1 = shp.add_run(f"॥ उद्योगसूत्रम् {s_idx:02d} ॥\n")
        shr1.font.name = "Georgia"
        shr1.font.size = Pt(11)
        shr1.font.bold = True
        shr1.font.color.rgb = C_GOLD

        shr2 = shp.add_run(f"{sutra_verse_clean}\n")
        shr2.font.name = "Georgia"
        shr2.font.size = Pt(15)
        shr2.font.bold = True
        shr2.font.color.rgb = C_MAROON

        shr3 = shp.add_run(f"({TRANSLITERATIONS['new_sutra'].get(s_idx, '')})")
        shr3.font.name = "Arial"
        shr3.font.size = Pt(8.5)
        shr3.font.italic = True
        shr3.font.color.rgb = C_NAVY

        # DEDICATED PROMINENT TRANSLATION BOX (DIRECTLY UNDER SHLOKA)
        tr_tbl = doc.add_table(rows=1, cols=1)
        tr_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        tr_cell = tr_tbl.cell(0, 0)
        set_cell_background(tr_cell, "FBF9F5")
        set_cell_margins(tr_cell, top=70, bottom=70, left=110, right=110)
        trp = tr_cell.paragraphs[0]
        trp.paragraph_format.space_after = Pt(0)

        tr_mr_hdr = trp.add_run("मराठी भाषांतर व सरळ अर्थ (Marathi Translation & Direct Meaning):\n")
        tr_mr_hdr.font.name = "Georgia"
        tr_mr_hdr.font.size = Pt(10)
        tr_mr_hdr.font.bold = True
        tr_mr_hdr.font.color.rgb = C_MAROON

        tr_mr_val = trp.add_run(f"{nus.get('translation_mr')}\n\n")
        tr_mr_val.font.name = "Georgia"
        tr_mr_val.font.size = Pt(11.5)
        tr_mr_val.font.bold = True
        tr_mr_val.font.color.rgb = C_CHARCOAL

        tr_en_hdr = trp.add_run("English Translation:\n")
        tr_en_hdr.font.name = "Arial"
        tr_en_hdr.font.size = Pt(9)
        tr_en_hdr.font.bold = True
        tr_en_hdr.font.color.rgb = C_NAVY

        tr_en_val = trp.add_run(f"{nus.get('translation_en')}")
        tr_en_val.font.name = "Arial"
        tr_en_val.font.size = Pt(10)
        tr_en_val.font.italic = True
        tr_en_val.font.color.rgb = C_SLATE

        # Padaccheda, Anvaya & Nirukta
        pa_p = doc.add_paragraph()
        pa_p.paragraph_format.space_before = Pt(4)
        pa_p.paragraph_format.space_after = Pt(2)
        r_pl = pa_p.add_run("शब्द फोड (Word Breakdown / Padaccheda): ")
        r_pl.font.name = "Arial"
        r_pl.font.size = Pt(8.5)
        r_pl.font.bold = True
        r_pl.font.color.rgb = C_NAVY
        r_pv = pa_p.add_run(f"{nus['padaccheda']}\n")
        r_pv.font.name = "Georgia"
        r_pv.font.size = Pt(9)
        r_pv.font.color.rgb = C_SLATE

        r_al = pa_p.add_run("सोपा सरळ क्रम (Simple Prose Order / Anvaya): ")
        r_al.font.name = "Arial"
        r_al.font.size = Pt(8.5)
        r_al.font.bold = True
        r_al.font.color.rgb = C_NAVY
        r_av = pa_p.add_run(f"{nus['anvaya']}\n")
        r_av.font.name = "Georgia"
        r_av.font.size = Pt(9)
        r_av.font.color.rgb = C_SLATE

        r_nl = pa_p.add_run("शब्दांचे अर्थ (Word Meanings / Nirukta): ")
        r_nl.font.name = "Arial"
        r_nl.font.size = Pt(8.5)
        r_nl.font.bold = True
        r_nl.font.color.rgb = C_NAVY
        r_nv = pa_p.add_run(str(nus.get("nirukta", "")))
        r_nv.font.name = "Georgia"
        r_nv.font.size = Pt(8.5)
        r_nv.font.color.rgb = C_SLATE

        # ---------------- SECTION 4: DETAILED EXPLANATION / BHASHYA ----------------
        e_title = doc.add_paragraph()
        e_title.paragraph_format.space_before = Pt(8)
        e_title.paragraph_format.space_after = Pt(2)
        r_et = e_title.add_run("४. सविस्तर विवेचन व निरूपण (Detailed Exposition & Commentary)")
        r_et.font.name = "Arial"
        r_et.font.size = Pt(10.5)
        r_et.font.bold = True
        r_et.font.color.rgb = C_MAROON

        b_tbl = doc.add_table(rows=1, cols=1)
        b_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        b_cell = b_tbl.cell(0, 0)
        set_cell_background(b_cell, "FFFFFF")
        set_cell_margins(b_cell, top=60, bottom=60, left=100, right=100)
        bp = b_cell.paragraphs[0]
        bp.paragraph_format.space_after = Pt(0)
        b_hdr = bp.add_run("सुटसुटीत निरूपण (Crisp & Clear Explanation — सूत्र लहान, विचार महान):\n")
        b_hdr.font.name = "Georgia"
        b_hdr.font.size = Pt(9.5)
        b_hdr.font.bold = True
        b_hdr.font.color.rgb = C_MAROON

        bhashya_text = nus.get("comprehensive_bhashya_mr") or nus.get("translation_mr", "")
        b_val = bp.add_run(bhashya_text)
        b_val.font.name = "Georgia"
        b_val.font.size = Pt(9.5)
        b_val.font.color.rgb = C_SLATE

        # ---------------- SECTION 5: PRACTICAL APPLICATION AND EXAMPLES ----------------
        ex_title = doc.add_paragraph()
        ex_title.paragraph_format.space_before = Pt(8)
        ex_title.paragraph_format.space_after = Pt(2)
        r_ext = ex_title.add_run("५. व्यावहारिक उपयोजन व सत्यकथा (Practical Applications & Real-Life Case Studies)")
        r_ext.font.name = "Arial"
        r_ext.font.size = Pt(10.5)
        r_ext.font.bold = True
        r_ext.font.color.rgb = C_MAROON

        ex_tbl = doc.add_table(rows=2, cols=1)
        ex_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER

        # Row 0: Real-Life Case Studies
        c_cs = ex_tbl.cell(0, 0)
        set_cell_background(c_cs, "F5F7FA")
        set_cell_margins(c_cs, top=50, bottom=50, left=90, right=90)
        p_cs = c_cs.paragraphs[0]
        p_cs.paragraph_format.space_after = Pt(0)
        r_csh = p_cs.add_run("सत्यकथा व ऐतिहासिक उदाहरणे (Inspiring Real-Life Case Studies — Eastern & Western):\n")
        r_csh.font.name = "Arial"
        r_csh.font.size = Pt(8.5)
        r_csh.font.bold = True
        r_csh.font.color.rgb = C_NAVY

        case_studies = nus.get("biographical_case_studies", [])
        if isinstance(case_studies, list) and case_studies:
            for cs in case_studies:
                if isinstance(cs, dict):
                    p_cs.add_run(f"• {cs.get('name')} [{cs.get('category')}]: {cs.get('case_summary')}\n")
                else:
                    p_cs.add_run(f"• {cs}\n")
        else:
            p_cs.add_run("• जमशेदजी टाटा (स्वदेशी राष्ट्रउभारणी) व थॉमस एडिसन (तर्कशुद्ध प्रयोगशीलता व समर्पण)\n")

        # Row 1: Patanjali Yoga Psychological Resilience Framework
        c_yg = ex_tbl.cell(1, 0)
        set_cell_background(c_yg, "FBF9F5")
        set_cell_margins(c_yg, top=50, bottom=50, left=90, right=90)
        p_yg = c_yg.paragraphs[0]
        p_yg.paragraph_format.space_after = Pt(0)
        r_ygh = p_yg.add_run("मानसिक समतोल व ताणमुक्ती — पतंजली योगविचार (Mental Peace & Stress Relief):\n")
        r_ygh.font.name = "Georgia"
        r_ygh.font.size = Pt(8.5)
        r_ygh.font.bold = True
        r_ygh.font.color.rgb = C_GOLD

        yg_data = nus.get("mental_resilience_yoga_sutras", {})
        if isinstance(yg_data, dict) and yg_data:
            ref = yg_data.get("sutra_reference", "पतंजली योगसूत्र १.१२")
            v_sk = yg_data.get("sanskrit", "अभ्यासवैराग्याभ्यां तन्निरोधः")
            fw = yg_data.get("psychological_framework", "")
            p_yg.add_run(f"• सूत्र संदर्भ: {ref} — {v_sk}\n• मनाची शांतता व ताणमुक्ती: {fw}")
        else:
            p_yg.add_run("• अभ्यास व वैराग्याच्या द्वारे उद्योजकाने संकटातही मानसिक संतुलन राखावे.")

        # ---------------- SECTION 6: DOs AND DON'Ts ----------------
        dd_title = doc.add_paragraph()
        dd_title.paragraph_format.space_before = Pt(8)
        dd_title.paragraph_format.space_after = Pt(2)
        r_ddt = dd_title.add_run("६. काय करावे आणि काय टाळावे — आचारसंहिता (DOs and DON'Ts for Modern Enterprise)")
        r_ddt.font.name = "Arial"
        r_ddt.font.size = Pt(10.5)
        r_ddt.font.bold = True
        r_ddt.font.color.rgb = C_MAROON

        dd_tbl = doc.add_table(rows=2, cols=1)
        dd_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER

        # DOs Cell
        c_do = dd_tbl.cell(0, 0)
        set_cell_background(c_do, "F0FDF4")  # Light green tint
        set_cell_margins(c_do, top=50, bottom=50, left=90, right=90)
        p_do = c_do.paragraphs[0]
        p_do.paragraph_format.space_after = Pt(0)
        r_doh = p_do.add_run("✓ काय करावे (DOs — रचनात्मक आणि आवश्यक कृती):\n")
        r_doh.font.name = "Arial"
        r_doh.font.size = Pt(8.5)
        r_doh.font.bold = True
        r_doh.font.color.rgb = C_GREEN

        for do_item in dnd["dos"]:
            p_do.add_run(f"• {do_item}\n")

        # Practical Guidance for Roles
        pe_items = nus.get("practical_enterprise_guidance", [])
        if isinstance(pe_items, list) and pe_items:
            for item in pe_items:
                if isinstance(item, dict):
                    p_do.add_run(f"• [{item.get('role')}]: {item.get('guidance')}\n")

        # DON'Ts Cell
        c_dont = dd_tbl.cell(1, 0)
        set_cell_background(c_dont, "FEF2F2")  # Light red tint
        set_cell_margins(c_dont, top=50, bottom=50, left=90, right=90)
        p_dont = c_dont.paragraphs[0]
        p_dont.paragraph_format.space_after = Pt(0)
        r_donth = p_dont.add_run("✗ काय टाळावे (DON'Ts — संभाव्य धोके, प्रलोभने व चुका):\n")
        r_donth.font.name = "Arial"
        r_donth.font.size = Pt(8.5)
        r_donth.font.bold = True
        r_donth.font.color.rgb = C_RED

        for dont_item in dnd["donts"]:
            p_dont.add_run(f"• {dont_item}\n")

        # ---------------- SECTION 7: REFLECTION / KEY TAKEAWAY ----------------
        ref_title = doc.add_paragraph()
        ref_title.paragraph_format.space_before = Pt(8)
        ref_title.paragraph_format.space_after = Pt(2)
        r_reft = ref_title.add_run("७. चिंतन व अंतिम सूत्रसार (Reflection & Key Takeaway)")
        r_reft.font.name = "Arial"
        r_reft.font.size = Pt(10.5)
        r_reft.font.bold = True
        r_reft.font.color.rgb = C_MAROON

        ref_tbl = doc.add_table(rows=1, cols=1)
        ref_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        ref_cell = ref_tbl.cell(0, 0)
        set_cell_background(ref_cell, "FFFBF0")
        set_cell_margins(ref_cell, top=60, bottom=60, left=100, right=100)
        ref_p = ref_cell.paragraphs[0]
        ref_p.paragraph_format.space_after = Pt(0)

        rq_h = ref_p.add_run("अंतर्मुख करणारा प्रश्न (Practical Reflection for Leaders):\n")
        rq_h.font.name = "Georgia"
        rq_h.font.size = Pt(9)
        rq_h.font.bold = True
        rq_h.font.color.rgb = C_NAVY

        rq_v = ref_p.add_run(f"\"{dnd['reflection_question']}\"\n\n")
        rq_v.font.name = "Georgia"
        rq_v.font.size = Pt(9.5)
        rq_v.font.italic = True
        rq_v.font.color.rgb = C_CHARCOAL

        ta_h = ref_p.add_run("अंतिम सूत्रसार व आचरण मंत्र (Core Takeaway):\n")
        ta_h.font.name = "Arial"
        ta_h.font.size = Pt(9)
        ta_h.font.bold = True
        ta_h.font.color.rgb = C_MAROON

        ta_v = ref_p.add_run(f"★ {dnd['takeaway']}")
        ta_v.font.name = "Georgia"
        ta_v.font.size = Pt(10)
        ta_v.font.bold = True
        ta_v.font.color.rgb = C_MAROON

        # Auspicious Separator
        q_p = doc.add_paragraph()
        q_p.paragraph_format.space_before = Pt(8)
        q_p.paragraph_format.space_after = Pt(16)
        q_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        qr = q_p.add_run("॥ शुभं भवतु — उद्योगेनैव सिध्यन्ति कार्याणि ॥")
        qr.font.name = "Georgia"
        qr.font.size = Pt(9)
        qr.font.italic = True
        qr.font.color.rgb = C_GOLD

        if s_idx < 10:
            doc.add_page_break()

    # Save to Target Paths
    TARGET_OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    doc.save(str(TARGET_OUTPUT))
    print(f"Saved workspace file: {TARGET_OUTPUT}")

    # Copy to Dropbox
    try:
        DROPBOX_OUTPUT.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(TARGET_OUTPUT, DROPBOX_OUTPUT)
        print(f"Copied to Dropbox: {DROPBOX_OUTPUT}")
    except Exception as e:
        print(f"Warning: Could not copy to Dropbox: {e}")

    # Copy to Brain Artifact
    try:
        shutil.copy2(TARGET_OUTPUT, ARTIFACT_OUTPUT)
        print(f"Copied to Brain Artifact: {ARTIFACT_OUTPUT}")
    except Exception as e:
        print(f"Warning: Could not copy to Brain Artifact: {e}")

    print("\nManuscript generation completed successfully.")
    return TARGET_OUTPUT


if __name__ == "__main__":
    build_editorial_refined_manuscript()
