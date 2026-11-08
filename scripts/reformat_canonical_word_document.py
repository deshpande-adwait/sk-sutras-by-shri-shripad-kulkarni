"""
================================================================================
Script: scripts/reformat_canonical_word_document.py
Author: Hiranyam AI Labs (https://hiranyamai.com/)
Project: SK Sutras - by Shri Shripad Kulkarni
Description: Exact Canonical Word Document Generator for the First Ten Approved
             Udyam Sutras, matching the client's exact required format:
             - Header Banner & Metadata Table
             - Per-Sutra Unit:
               * UDYAM SUTRA {N}: {Sanskrit/Marathi Title} ({English Subtitle})
               * Sanskrit Shloka + IAST Transliteration in container box
               * Source References (Foundational Texts) table:
                 - Narad Bhakti Sutra
                 - Shandilya Bhakti Sutra
                 - Bharatiya Jnana Tradition
               * English Translation
               * मराठी विवेचन व भावार्थ
               * Philosophical Foundation (तत्त्वज्ञानात्मक अधिष्ठान)
               * Practical Application in Business & Management (Structured Bullets)
             - Continuous Mandatory Footer on EVERY page:
               "Proprietory and Confidential- Hiranyam AI Labs"
================================================================================
"""

import os
import shutil
import sys
from pathlib import Path

# Ensure UTF-8 output encoding across Windows consoles
if sys.platform.startswith("win"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

import docx
from docx import Document
from docx.enum.table import WD_ALIGN_VERTICAL, WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Inches, Pt, RGBColor

BASE_DIR = Path(__file__).resolve().parent.parent
DOCS_DIR = BASE_DIR / "docs"
DOCS_DIR.mkdir(parents=True, exist_ok=True)
ARTIFACT_DIR = Path(r"C:\Users\deshp\.gemini\antigravity\brain\94293167-6c7d-4773-b091-412c085b8cdc")
OUTPUT_DOCX = DOCS_DIR / "UDYOG_SUTRAS_TEN_NEW_CANONICAL_MATCHING_AND_SHLOKAS.docx"

MANDATORY_FOOTER = "Proprietory and Confidential- Hiranyam AI Labs"

# Color Palette
C_MAROON = RGBColor(139, 0, 0)       # #8B0000 Primary Sacred Accent
C_NAVY = RGBColor(26, 54, 93)        # #1A365D Primary Corporate Header
C_GOLD = RGBColor(184, 134, 11)      # #B8860B Secondary Accent
C_SLATE = RGBColor(44, 62, 80)       # #2C3E50 Body Text Slate
C_DARK_TEXT = RGBColor(30, 41, 59)   # #1E293B Dark Charcoal
C_MUTED = RGBColor(100, 116, 139)    # #64748B Secondary Muted

# XML Helper Functions for Document Styling
def set_cell_background(cell, hex_color: str):
    """Sets background shading of a table cell."""
    tcPr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), hex_color)
    tcPr.append(shd)

def set_cell_margins(cell, top=100, bottom=100, left=140, right=140):
    """Sets cell internal padding in dxa (1 pt = 20 dxa)."""
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement("w:tcMar")
    for m, val in [("top", top), ("bottom", bottom), ("left", left), ("right", right)]:
        node = OxmlElement(f"w:{m}")
        node.set(qn("w:w"), str(val))
        node.set(qn("w:type"), "dxa")
        tcMar.append(node)
    tcPr.append(tcMar)

def set_cell_borders(cell, top="none", bottom="none", left="none", right="none", 
                     color="CCCCCC", sz="4"):
    """Sets cell borders with specified styles and colors."""
    tcPr = cell._tc.get_or_add_tcPr()
    tcBorders = OxmlElement("w:tcBorders")
    borders = {"top": top, "bottom": bottom, "left": left, "right": right}
    for border_name, border_style in borders.items():
        b_el = OxmlElement(f"w:{border_name}")
        b_el.set(qn("w:val"), border_style)
        if border_style != "none":
            b_el.set(qn("w:sz"), sz)
            b_el.set(qn("w:space"), "0")
            b_el.set(qn("w:color"), color)
        tcBorders.append(b_el)
    tcPr.append(tcBorders)

# Canonical 10 Sutras Data exactly as provided by the user
TEN_SUTRAS_DATA = [
    {
        "sutra_no": 1,
        "title": "उद्यम-संकल्प व रणनीतिक जिज्ञासा (Inception & Diligent Inquiry)",
        "shloka_devanagari": "अथातो व्यवहारेऽस्मिन् धर्म्यमुद्योगमारभेत् ।\nजिज्ञासा कार्यदक्षाणां सर्वसिद्धेः प्रसाधिका ॥",
        "shloka_iast": "athāto vyavahāre'smin dharmyam udyogam ārabhet |\njijñāsā kāryadakṣāṇāṁ sarvasiddheḥ prasādhikā ||",
        "sources": {
            "narada": "Narada Bhakti Sutra 1 — अथातो भक्तिं व्याख्यास्यामः ॥",
            "shandilya": "Shandilya Bhakti Sutra 1 — अथातो भक्तिजिज्ञासा ॥",
            "bharatiya_jnana": "Kautilya's Arthashastra (Adhikarana 1, Adhyaya 19, Shloka 34) — अनुत्थाने ध्रुवो नाशः प्राप्तस्यानागतस्य च । प्राप्यते फलमुत्थानाल्लभते चार्थसम्पदम् ॥",
        },
        "english_translation": "Now, in this arena of worldly commerce, one must initiate righteous enterprise; the rigorous, strategic inquiry of skilled professionals accomplishes all success.",
        "marathi_purport": "कोणताही व्यवसाय केवळ उत्साहाच्या भरात सुरू करू नये. व्यवहारात उतरताना पहिली पायरी म्हणजे आपला उद्योग नीती आणि न्यायावर आधारलेला असावा. त्याचबरोबर कार्यकुशल उद्योजकाने बाजारातील गरज, ग्राहकांची समस्या आणि तंत्रज्ञान याविषयी सातत्याने सखोल चौकशी (जिज्ञासा) केली पाहिजे. अभ्यासपूर्ण विचार आणि नैतिक संकल्प यांच्या संयोगातूनच सर्व उद्दिष्टे यशस्वी होतात.",
        "philosophical_foundation": "नारदभक्तिसूत्राचा पहिला शब्द 'अथातो' संकल्पाची आणि आंतरिक समर्पणाची घोषणा करतो; शांडिल्यभक्तिसूत्रातील 'जिज्ञासा' हा शब्द अंधश्रद्धेला नाकारून बुद्धिनिष्ठ संशोधनाचा आग्रह धरतो. कौटिलीय अर्थशास्त्र स्पष्ट करते की 'उत्थान' म्हणजे सक्रिय उद्यम नसेल, तर मिळालेली आणि मिळणारी संपत्ती नष्ट होते. मूळ शास्त्रात हे अध्यात्म आणि राज्यव्यवस्थेसाठी आले आहे; उद्योगात त्याचा अर्थ असा की व्यवसाय सुरू करण्यापूर्वी कल्पनेची बाजारपेठेत कसून चाचणी (Feasibility Validation) करणे अनिवार्य आहे.",
        "practical_applications": [
            ("नवउद्योजकांसाठी", "व्यवसाय सुरू करताना केवळ भावनेच्या भरात भांडवल गुंतवू नका; ग्राहकांशी प्रत्यक्ष बोलून समस्येची सत्यता तपासा."),
            ("व्यवस्थापकांसाठी", "नवीन प्रकल्प हाती घेताना खर्च, जोखीम आणि तंत्रज्ञानाचा प्राथमिक अभ्यास (Due Diligence) कागदावर नव्हे तर प्रत्यक्षात करा."),
            ("नेतृत्वासाठी", "संस्थेचा पाया सुरुवातीपासूनच पारदर्शक आणि कायदेशीर नियमांवर उभा करा.")
        ]
    },
    {
        "sutra_no": 2,
        "title": "व्यावसायिक निष्ठा व उत्कृष्टतेचा ध्यास (Craftsmanship & Passion)",
        "shloka_devanagari": "स्वाधिकारे परा प्रीतिरुद्योगे सिद्धिदायिनी ।\nअनुरागवतां यत्नः सुदृढो नैव सीदति ॥",
        "shloka_iast": "svādhikāre parā prītir udyoge siddhidāyinī |\nanurāgavatāṁ yatnaḥ sudṛḍho naiva sīdati ||",
        "sources": {
            "narada": "Narada Bhakti Sutra 2 — सा त्वस्मिन् परमप्रेमरूपा ॥",
            "shandilya": "Shandilya Bhakti Sutra 2 — सा परानुरक्तिरीश्वरे ॥",
            "bharatiya_jnana": "Bhagavad Gita (Chapter 18, Verse 45) — स्वे स्वे कर्मण्यभिरतः संसिद्धिं लभते नरः । स्वकर्मनिरतः सिद्धिं यथा विन्दति तच्छृणु ॥",
        },
        "english_translation": "Supreme love toward one’s rightful work yields accomplishment in enterprise; the disciplined effort of passionate creators never falters.",
        "marathi_purport": "आपल्या वाट्याला आलेल्या कामावर आणि जबाबदारीवर मनापासून प्रेम असणे हेच उद्योगातील यशाचे खरे गमक आहे. केवळ पैशासाठी केलेले काम थकवा आणते; पण ज्या कामात आत्मीयता आणि उत्कृष्टतेचा ध्यास असतो, त्या कामात कितीही अडचणी आल्या तरी माणसाचा प्रयत्न खचत नाही. अशी निष्ठाच उत्पादनाला जागतिक दर्जा मिळवून देते.",
        "philosophical_foundation": "नारदांचे 'परमप्रेम' हे भावनिक समर्पणाचे शिखर आहे, तर शांडिल्यांची 'परानुरक्ती' ही सर्वोच्च तत्त्वाशी असलेली अढळ बौद्धिक बांधिलकी आहे. गीतेतील १८.४५ श्लोक सांगतो की स्वतःच्या स्वाभाविक कर्तव्यात जो पूर्णपणे गढून जातो, तोच सिद्धी पावतो. मूळ शास्त्रातील ईश्वरभक्तीचा हा भाव उद्योगात 'कामावरील पूजाभाव' (Craftsmanship) म्हणून रूपांतरित होतो.",
        "practical_applications": [
            ("उत्पादन गुणवत्तेसाठी", "'शून्य-त्रुटी' (Zero Defect) ही केवळ घोषणा न ठेवता कामात अभिमान बाळगणारी संस्कृती तयार करा."),
            ("कर्मचारी व्यवस्थापनासाठी", "कर्मचाऱ्यांना केवळ वेतनाचे मजूर न मानता त्यांच्या कौशल्याचा आदर करा; कामात स्वायत्तता द्या."),
            ("व्यावसायिक जीवनासाठी", "तात्पुरत्या ट्रेंडच्या मागे धावण्याऐवजी स्वतःच्या मूळ कौशल्यात निपुणता मिळवा.")
        ]
    },
    {
        "sutra_no": 3,
        "title": "शाश्वत मूल्यनिर्मिती व संस्थागत अमरत्व (Institutional Longevity & Governance)",
        "shloka_devanagari": "अमृतत्वाय धर्म्या स्याद् वाणिज्ये शुभसन्ततिः ।\nन्यायोपार्जितवित्तेन चिरं जीवति संस्था ॥",
        "shloka_iast": "amṛtatvāya dharmyā syād vāṇijye śubhasantatiḥ |\nnyāyopārjitavittena ciraṁ jīvati saṁsthā ||",
        "sources": {
            "narada": "Narada Bhakti Sutra 3 — अमृतस्वरूपा च ॥",
            "shandilya": "Shandilya Bhakti Sutra 3 — तत्संस्थस्यामृतत्वोपदेशात् ॥",
            "bharatiya_jnana": "Bhartrihari's Niti Shataka (Verse 68) — निन्दन्तु नीतिनिपुणा यदि वा स्तुवन्तु लक्ष्मीः समाविशतु गच्छतु वा यथेष्टम् । अद्यैव वा मरणमस्तु युगान्तरे वा न्यायात्पथः प्रविचलन्ति पदं न धीराः ॥",
        },
        "english_translation": "For an enterprise to attain enduring legacy, its conduct must be righteous; an institution founded on ethically acquired wealth endures long.",
        "marathi_purport": "व्यापाराला दीर्घायुष्य लाभावे असे वाटत असेल, तर व्यवसायातील प्रत्येक व्यवहार आणि निर्णय नैतिकतेच्या परंपरेला धरून असला पाहिजे. अन्यायाने, कर चुकवून किंवा ग्राहकाला फसवून मिळवलेला नफा फुग्यासारखा फुटतो. याउलट, न्यायाने आणि सचोटीने मिळवलेल्या पैशावरच एखादी संस्था पिढ्यानपिढ्या ताठ मानेने जिवंत राहते.",
        "philosophical_foundation": "नारद आणि शांडिल्य दोघेही भक्तीला 'अमृतस्वरूप' मानतात—जी व्यक्तीला मृत्यूच्या पलीकडे नेते. भर्तृहरीच्या नीतिशतकात स्पष्ट केले आहे की संपत्ती येवो वा जावो, धीर पुरुष न्यायाचा मार्ग सोडत नाहीत. मूळ शास्त्रातील मोक्षाचे अमरत्व येथे संस्थात्मक अमरत्वात (Corporate Longevity) रूपांतरित होते.",
        "practical_applications": [
            ("लेखांकनासाठी", "आर्थिक व्यवहारात १००% पारदर्शकता ठेवा; ताळेबंदात फेरफार करून तात्पुरते मूल्यांकन फुगवू नका."),
            ("ब्रँड विश्वासासाठी", "ग्राहकांशी केलेले करार आणि आश्वासने तोट्यात गेलात तरी पाळा."),
            ("संस्था बांधणीसाठी", "एका पिढीपुरता व्यवसाय न पाहता पुढील १०० वर्षे टिकेल अशी नियमाधिष्ठित व्यवस्था उभारा.")
        ]
    },
    {
        "sutra_no": 4,
        "title": "लोभमुक्ती व आंतरिक समाधान (Contentment Over Greed)",
        "shloka_devanagari": "तृप्तो भवति धर्मेण न लुब्धो विनशिष्यति ।\nअन्यायेनार्जितं वित्तं क्षिप्रं नश्यति मूलतः ॥",
        "shloka_iast": "tṛpto bhavati dharmeṇa na lubdho vinaśiṣyati |\nanyāyenārjitaṁ vittaṁ kṣipraṁ naśyati mūlataḥ ||",
        "sources": {
            "narada": "Narada Bhakti Sutra 4 — यल्लव्ध्वा पुमान् सिद्धो भवति अमृतो भवति तृप्तो भवति ॥",
            "shandilya": "Shandilya Bhakti Sutra 7 — हेतावप्रतिष्ठानात् ॥",
            "bharatiya_jnana": "Isha Upanishad (Mantra 1) — ईशा वास्यमिदं सर्वं यत्किञ्च जगत्यां जगत् । तेन त्यक्तेन भुञ्जीथा मा गृधः कस्यस्विद्धनम् ॥",
        },
        "english_translation": "One contented through integrity prospers, while the greedy faces ruin; wealth amassed through injustice rapidly perishes at its root.",
        "marathi_purport": "धर्माने आणि प्रामाणिक कष्टाने काम करणारा व्यावसायिक आंतरिक समाधानाने समृद्ध होतो. याउलट, अमर्याद लोभाच्या आहारी जाऊन नफा मिळवणारा स्वतःचाच विनाश ओढवून घेतो. कामगारांचे शोषण करून किंवा ग्राहकांची फसवणूक करून मिळवलेले धन कितीही मोठे दिसले, तरी ते मुळासकट लवकरच नष्ट होते.",
        "philosophical_foundation": "नारद सूत्रातील 'तृप्तो भवति' हा आत्मिक समाधानाचा निकष आहे; शांडिल्यांचे 'हेतावप्रतिष्ठानात्' सांगते की केवळ स्वार्थी हेतूंना जगात स्थिर अधिष्ठान नसते. ईशावास्योपनिषदातील 'मा गृधः कस्यस्विद्धनम्' कोणाच्याही धनाचा लोभ धरू नका हा आदेश देतो. हा विचार व्यवसायात शोषणात्मक नफ्याऐवजी 'वाजवी नफा आणि नैतिक मर्यादा' (Fair Pricing & Value Restraint) शिकवतो.",
        "practical_applications": [
            ("मूल्य निर्धारण", "ग्राहकांवर अव्वाच्या सव्वा नफा लादण्याऐवजी सेवा आणि खर्चाशी सुसंगत किंमत ठेवा."),
            ("कामगार संबंध", "कामगारांच्या श्रमाचा योग्य मोबदला वेळेवर द्या; त्यांचे शोषण करून नफा वाढवू नका."),
            ("गुंतवणूक धोरण", "रातोरात श्रीमंत करणाऱ्या संशयास्पद आणि अनैतिक योजनांपासून सावध राहा.")
        ]
    },
    {
        "sutra_no": 5,
        "title": "सर्वहितचिंतन व अखंड समर्पण (Stakeholder Welfare & Trusteeship)",
        "shloka_devanagari": "हितं सर्वजनस्यापि चिन्तयेत् सततं बुधः ।\nयज्ञार्थं वर्तते कर्म तन्न बन्धाय कल्पते ॥",
        "shloka_iast": "hitaṁ sarvajanasyāpi cintayet satataṁ budhaḥ |\nyajñārthaṁ vartate karma tanna bandhāya kalpate ||",
        "sources": {
            "narada": "Narada Bhakti Sutra 19 — नारदस्तु तदर्पिताखिलाचारता तद्विस्मरणे परमव्याकुलतेति ॥",
            "shandilya": "Shandilya Bhakti Sutra 87 — सर्वथा वर्तमानोऽपि न स संसारी भवति ॥",
            "bharatiya_jnana": "Bhagavad Gita (Chapter 3, Verse 9) — यज्ञार्थात्कर्मणोऽन्यत्र लोकोऽयं कर्मबन्धनः । तदर्थं कर्म कौन्तेय मुक्तसङ्गः समाचर ॥",
        },
        "english_translation": "A wise leader constantly safeguards the welfare of all stakeholders; when professional work is conducted as a dedicated sacrifice, it causes no bondage.",
        "marathi_purport": "सुजाण उद्योजकाने केवळ स्वतःच्या खिशाचा विचार न करता ग्राहक, कामगार, पुरवठादार आणि समाज या सर्वांच्या हिताचा सतत विचार करावा. जेव्हा आपला व्यवसाय हा समाजाच्या सेवेसाठी चालवलेला एक पवित्र यज्ञ बनतो, तेव्हा त्यातील नफा-तोटा किंवा चढउतार माणसाला मानसिक बंधनात किंवा तणावात अडकवत नाहीत.",
        "philosophical_foundation": "नारदांचे 'तदर्पिताखिलाचारता' आपले सर्व आचरण ईश्वराला अर्पण करण्याचे सांगते; शांडिल्यांचे 'सर्वथा वर्तमानोऽपि' सांगते की जगात सक्रिय राहूनही माणूस बंधनामुक्त राहू शकतो. गीतेतील ३.९ श्लोक 'यज्ञार्थ कर्म' बंधनकारक ठरत नसल्याचे स्पष्ट करतो. आधुनिक भाषेत यालाच 'Stakeholder Capitalism' किंवा विश्वस्त व्यवस्था (Trusteeship) म्हणतात.",
        "practical_applications": [
            ("कंपनी धोरण", "कंपनीच्या वार्षिक उद्दिष्टांमध्ये केवळ EBITDA न ठेवता पर्यावरण आणि कर्मचारी समाधानाचे निकष ठेवा."),
            ("पुरवठा साखळी", "लहान पुरवठादारांची देयके अडकवून न ठेवता त्यांना वेळेवर पैसे देऊन सक्षम करा."),
            ("संकट व्यवस्थापन", "मंदीच्या काळात कामगारांना कामावरून काढण्याऐवजी व्यवस्थापकीय खर्चात कपात करा.")
        ]
    },
    {
        "sutra_no": 6,
        "title": "आघातजन्य-सामर्थ्य व विपत्ति-रूपांतरण (Antifragility & Adversarial Transformation)",
        "shloka_devanagari": "आघातोत्पीडितः प्राज्ञो दीप्यते न तु सीदति ।\nविपद्भवति सामर्थ्यं यस्योद्योगः स्वभावजः ॥",
        "shloka_iast": "āghātotpīḍitaḥ prājño dīpyate na tu sīdati |\nvipad bhavati sāmarthyaṁ yasyodyogaḥ svabhāvajaḥ ||",
        "sources": {
            "narada": "Narada Bhakti Sutra 78 — अहिंसासत्यशौचदयास्तिक्यादिचारित्र्याणि परिपालनीयानि ॥",
            "shandilya": "Shandilya Bhakti Sutra 61 — तदैक्यान्नानात्वम् ॥",
            "bharatiya_jnana": "Mahabharata, Udyoga Parva (Chapter 134, Verse 14 - Vidula-Putra Samvada) — उत्तिष्ठ हे कापुरुष मा शेष्वैवं पराजितः । मुहूर्तं ज्वलितं श्रेयो न च धूमायितं चिरम् ॥",
        },
        "english_translation": "Buffeted by external shocks and hostility, the wise leader blazes forth and never collapses; adversity itself transforms into enduring capability for one whose enterprise is born of innate purpose.",
        "marathi_purport": "जेव्हा उद्योगावर अचानक संकटे, आर्थिक मंदी किंवा स्पर्धकांचे आक्रमक हल्ले होतात, तेव्हा खरा सुजाण उद्योजक खचून जात नाही. तो उलट नव्या जोमाने उजळून निघतो. ज्याचा व्यवसाय केवळ नफ्यासाठी नसून स्वतःच्या आंतरिक ध्येयातून उभा राहिला आहे, त्याच्यासाठी बाह्य संकटेच नव्या क्षमतेची आणि यशाची कारणे बनतात.",
        "philosophical_foundation": "नारदांचे ७८वे सूत्र संकटातही आंतरिक मूल्यांचे रक्षण करण्यास सांगते; शांडिल्यांचे ६१वे सूत्र सांगते की विविधतेचा समेट एकात्मिक तत्त्वात होतो. महाभारतातील विदुला-संवाद पराभवातून उठून पराक्रम गाजवण्याची प्रेरणा देतो. हा विचार केवळ संकटात टिकून राहणे (Resilience) नव्हे, तर संकटातून अधिक बळकट होणे (Antifragility) शिकवतो.",
        "practical_applications": [
            ("मंदीच्या काळात", "व्यवसाय थंडावला असल्यास कर्मचाऱ्यांना काढून टाकण्याऐवजी नवीन उत्पादनांच्या संशोधनावर (R&D) भर द्या."),
            ("स्पर्धेला सामोरे जाताना", "मोठ्या स्पर्धकाने किंमत युद्ध सुरू केले तर स्वतःच्या सेवेत विशिष्ट गुणवत्ता (Niche Specialization) निर्माण करा."),
            ("तंत्रज्ञान बदलात", "जुने तंत्रज्ञान बंद पडत असताना लगेच नव्या तंत्रज्ञानाचा स्वीकार करून स्वतःला आघाडीवर न्या.")
        ]
    },
    {
        "sutra_no": 7,
        "title": "प्रज्ञा-स्वायत्तता व स्वदेशी नवोन्मेष (Epistemic Sovereignty & Foundational IP)",
        "shloka_devanagari": "परप्रज्ञोपजीवेन न स्वराज्यं प्रसिद्ध्यति ।\nस्वात्ममूल्यान्वेषणेन विश्वं जयति बुद्धिमान् ॥",
        "shloka_iast": "paraprajñopajīvena na svarājyaṁ prasiddhyati |\nsvātmamūlyānveṣaṇena viśvaṁ jayati buddhimān ||",
        "sources": {
            "narada": "Narada Bhakti Sutra 10 — अन्याश्रयाणां त्यागोऽनन्यता ॥",
            "shandilya": "Shandilya Bhakti Sutra 8 — तद्वतः प्रपत्तिरन्यथा पातित्यात् ॥",
            "bharatiya_jnana": "Bhagavad Gita (Chapter 3, Verse 35) — श्रेयान्स्वधर्मो विगुणः परधर्मात्स्वनुष्ठितात् । स्वधर्मे निधनं श्रेयः परधर्मो भयावहः ॥",
        },
        "english_translation": "True sovereignty is never achieved by living on borrowed intellect and derivative frameworks; by originating foundational value from one's own core genius, the wise creator commands the world.",
        "marathi_purport": "परकीय तंत्रज्ञानाची केवळ नक्कल करून किंवा दुसऱ्यांच्या उसन्या विचारांवर अवलंबून राहून कोणताही देश किंवा उद्योग स्वावलंबी होऊ शकत नाही. जेव्हा बुद्धिमान उद्योजक आपल्या स्वतःच्या मूळ प्रतिभेचा आणि कौशल्याचा शोध घेऊन मूलभूत संशोधन करतो, तेव्हाच तो जागतिक बाजारपेठेत स्वतःचे स्वतंत्र आणि सन्माननीय स्थान निर्माण करतो.",
        "philosophical_foundation": "नारदांचे 'अन्याश्रयाणां त्यागो' इतर बाह्य आधारांचा त्याग करण्यास सांगते; शांडिल्यांचे 'तद्वतः प्रपत्तिरन्यथा पातित्यात्' स्वतःच्या सत्याला सोडून दुसऱ्यावर विसंबल्यास पतन निश्चित असल्याचे सांगते. गीतेतील 'स्वधर्मे निधनं श्रेयः' दुसऱ्याचे अनुकरण धोकादायक ठरवते. हे तत्त्व तंत्रज्ञान क्षेत्रात 'पेटंट्स आणि स्वदेशी आर्किटेक्चर' (Foundational IP) चे महत्त्व अधोरेखित करते.",
        "practical_applications": [
            ("सॉफ्टवेअर व आयटी", "पाश्चात्त्य साधनांचे केवळ व्हेंडर न बनता स्वतःचे मूळ सॉफ्टवेअर प्लॅटफॉर्म्स आणि अल्गोरिदम्स विकसित करा."),
            ("उत्पादन क्षेत्र", "आयात मालावर अवलंबून न राहता स्थानिक पातळीवर घटक निर्मितीची क्षमता उभी करा."),
            ("बौद्धिक संपदा", "आपल्या संशोधनाचे पेटंट घेऊन जागतिक स्तरावर रॉयल्टी मिळवणारी संस्था बना.")
        ]
    },
    {
        "sutra_no": 8,
        "title": "ज्ञानसंक्रमण व संस्थागत सातत्य (Inter-generational Lineage & Succession)",
        "shloka_devanagari": "न केवलं धनं स्थाप्यं स्थापनीया परम्परा ।\nयोग्यशिष्ये समर्पितं कार्यं तिष्ठति शाश्वतम् ॥",
        "shloka_iast": "na kevalaṁ dhanaṁ sthāpyaṁ sthāpanīyā paramparā |\nyogyaśiṣye samarpitaṁ kāryaṁ tiṣṭhati śāśvatam ||",
        "sources": {
            "narada": "Narada Bhakti Sutra 38 — महत्सङ्गस्तु दुर्लभोऽगम्योऽमोघश्च ॥",
            "shandilya": "Shandilya Bhakti Sutra 91 — परम्परातो ज्ञानसंसिद्धिः ॥",
            "bharatiya_jnana": "Taittiriya Upanishad, Shikshavalli (Anuvaka 11, Verse 1) — स्वाध्यायान्मा प्रमदः । आचार्याय प्रियं धनमाहृत्य प्रजातन्तुं मा व्यवच्छेत्सीः ॥",
        },
        "english_translation": "A leader must not merely leave behind monetary wealth; one must establish an enduring lineage of wisdom and values. An enterprise entrusted to a worthy successor endures eternally.",
        "marathi_purport": "संस्थापकाने केवळ बँक बॅलन्स किंवा मालमत्ता मागे सोडून जाणे पुरेसे नाही; त्याने आपल्या मूल्यांची आणि कार्यसंस्कृतीची एक जिवंत परंपरा निर्माण केली पाहिजे. जेव्हा एखादा उद्योग स्वतःच्या रक्ताच्या नात्यापेक्षा योग्य, कुशल आणि चारित्र्यवान शिष्याकडे विश्वासाने सोपवला जातो, तेव्हाच तो व्यवसाय काळाच्या ओघात अमर होतो.",
        "philosophical_foundation": "नारदांचे 'महत्सङ्गस्तु' महान विभूतींचा सहवास दुर्लभ असल्याचे सांगते; शांडिल्यांचे 'परम्परातो' ज्ञान केवळ अखंड गुरु-शिष्य परंपरेतून टिकत असल्याचे स्पष्ट करते. तैत्तिरीय उपनिषदातील 'प्रजातन्तुं मा व्यवच्छेत्सीः' ज्ञानाची अखंड साखळी कधीही तोडू नये असा आदेश देते. हे तत्त्व आधुनिक कॉर्पोरेट जगतात 'Succession Planning' आणि नेतृत्व निर्मितीचे मूळ आहे.",
        "practical_applications": [
            ("कौटुंबिक व्यवसाय", "केवळ मुलाला मालकी न देता योग्य गुणवत्ता आणि क्षमता असेल तरच सर्वोच्च पदाची जबाबदारी द्या."),
            ("कॉर्पोरेट नेतृत्व", "आपल्या कार्यकाळातच पुढील पिढीचे ३ ते ५ सक्षम नेते तयार करा (Talent Pipeline)."),
            ("कार्यसंस्कृती", "व्यवसायाचे अलिखित नियम आणि ग्राहकांशी असलेले नाते नवीन पिढीपर्यंत पोहचवा.")
        ]
    },
    {
        "sutra_no": 9,
        "title": "प्राकृतिक दोहन व चक्रीय परिसंस्था (Regenerative Ecological Symbiosis)",
        "shloka_devanagari": "दोहनेन यथा धेनुः पालिता न तु हिंसिता ।\nतथैव प्रकृतेर्भोगाद् उद्योगः फलवान् भवेत् ॥",
        "shloka_iast": "dohanena yathā dhenuḥ pālitā na tu hiṁsitā |\ntathaiva prakṛter bhogād udyogaḥ phalavān bhavet ||",
        "sources": {
            "narada": "Narada Bhakti Sutra 67 — तन्मया हि ते ॥",
            "shandilya": "Shandilya Bhakti Sutra 96 — प्राणेषु सर्वभूतानां समत्वम् ॥",
            "bharatiya_jnana": "Atharvaveda, Prithvi Sukta (Kanda 12, Sukta 1, Verse 35) — यत्ते भूमे विखनामि क्षिप्रं तदपि रोहतु । मा ते मर्म विमृग्वरि मा ते हृदयमर्पिपम् ॥",
        },
        "english_translation": "Just as a cow is lovingly nurtured and gently milked—never harmed or destroyed—so must an enterprise utilize nature’s resources through regeneration, thereby yielding enduring fruit.",
        "marathi_purport": "ज्याप्रमाणे सुजाण शेतकरी गाईचे आधी उत्तम पोषण करतो, तिच्या वासराला पुरेसे दूध पाजतो आणि मगच उरलेले दूध प्रेमाने काढतो—तिला कधीही इजा पोहोचवत नाही; अगदी त्याचप्रमाणे उद्योजकाने निसर्गातील संसाधनांचा वापर करताना तिचे संवर्धन केले पाहिजे. निसर्गाचे शोषण न करता तिचे पुनरुज्जीवन करणारा उद्योगच दीर्घकाळ भरभराटीस येतो.",
        "philosophical_foundation": "नारदांचे 'तन्मया हि ते' चराचराशी एकरूप होणे शिकवते; शांडिल्यांचे 'प्राणेषु समत्वम्' सर्व प्राणिमात्रांविषयी समभावाची मागणी करते. अथर्ववेदातील पृथ्वी सूक्त स्पष्ट सांगते: 'हे माते, तुझ्याकडून जेवढे घेईन तेवढे तातडीने पुन्हा निर्माण होवो; तुझ्या मर्मावर कधीही आघात होणार नाही.' हे तत्त्व 'चक्रीय अर्थव्यवस्था' (Circular Economy & Net-Zero) चे सर्वोच्च भारतीय रूप आहे.",
        "practical_applications": [
            ("कारखान्यांसाठी", "सांडपाणी प्रक्रिया (Zero Liquid Discharge) करून पाणी पुन्हा वापरा; नद्या प्रदूषित करू नका."),
            ("पॅकेजिंग", "प्लास्टिकचा वापर बंद करून १००% विघटनशील (Biodegradable) साहित्याचा वापर करा."),
            ("ऊर्जा व्यवस्थापन", "छतावर सौर ऊर्जा प्रकल्प बसवून स्वतःची वीज स्वतः निर्माण करा.")
        ]
    },
    {
        "sutra_no": 10,
        "title": "वास्तविक मूल्यनिर्मिती व आभासी अर्थत्याग (Tangible Utility Over Speculation)",
        "shloka_devanagari": "आभासिकं त्यजेल्लोभं वस्तुसत्यं विचिन्तयेत् ।\nलोकस्य दुःखहारित्वाद् उद्योगो महते श्रिये ॥",
        "shloka_iast": "ābhāsikaṁ tyajel lobhaṁ vastusatyaṁ vicintayet |\nlokasya duḥkhahāritvād udyogo mahate śriye ||",
        "sources": {
            "narada": "Narada Bhakti Sutra 7 — सा न कामयमाना निरोधरूपत्वात् ॥",
            "shandilya": "Shandilya Bhakti Sutra 6 — न क्रिया परप्रयोजनाभावात् ॥",
            "bharatiya_jnana": "Kautilya's Arthashastra (Adhikarana 1, Adhyaya 4, Sutra 1) — कृषि-पशुपाल्ये वणिज्या च वार्ता । धान्य-पशु-हिरण्य-कुप्य-विष्टि-प्रदानाद् औपकारिकी ॥",
        },
        "english_translation": "Let an entrepreneur renounce the illusory greed of paper speculation and concentrate upon real, tangible utility; an enterprise that alleviates the genuine suffering of the people attains monumental glory.",
        "marathi_purport": "केवळ कागदी मूल्यांकन फुगवण्याच्या किंवा सट्टेबाजीच्या आभासी लोभाचा उद्योजकाने त्याग करावा. आपल्या उत्पादनाची समाजात खरी गरज काय आहे आणि ते लोकांचे नेमके कोणते दुःख किंवा अडचण दूर करते, यावरच आपले लक्ष केंद्रित असावे. जो व्यवसाय लोकांच्या दैनंदिन जीवनातील अडचणी सोडवतो, त्याला कधीही ग्राहक कमी पडत नाहीत आणि तोच चिरंतन संपत्ती निर्माण करतो.",
        "philosophical_foundation": "नारदांचे ७वे सूत्र फसव्या कामनेचा निरोध करते; शांडिल्यांचे ६वे सूत्र सांगते की ज्या कर्माला ठोस प्रयोजन नाही, ती केवळ पोकळ हालचाल असते. कौटिलीय अर्थशास्त्रातील 'वार्ता' तत्त्वज्ञान शेती, पशुपालन आणि व्यापार यांनाच खरी संपत्ती मानणारे आहे, कारण ते प्रत्यक्ष धान्य व जीवनोपयोगी वस्तू देते. हा विचार हायपर-फायनान्स आणि स्टार्टअप मूल्यांकनाच्या फुग्यांवर कडक प्रहार करतो.",
        "practical_applications": [
            ("स्टार्टअप संस्थापकांसाठी", "पुढील फंडिंग राउंडच्या व्हॅल्युएशनवर नव्हे, तर तुमच्या उत्पादनाने ग्राहकांची कोणती खरी समस्या सुटली यावर लक्ष द्या."),
            ("व्यवसाय निवड", "केवळ ट्रेडिंग करण्याऐवजी प्रत्यक्ष उपयुक्त वस्तूंचे उत्पादन किंवा आवश्यक सेवा देणारा उद्योग निवडा."),
            ("शाश्वत नफा", "ज्या दिवशी उत्पादन ग्राहकाचे दुःख दूर करते, त्या दिवशी कंपनीचा महसूल नैसर्गिकरीत्या वाढतो.")
        ]
    }
]

def build_reformatted_canonical_document():
    """Compiles the complete Word document matching the client's exact format."""
    doc = Document()

    # Configure Margins & Continuous Mandatory Footer on EVERY section
    for section in doc.sections:
        section.top_margin = Inches(0.75)
        section.bottom_margin = Inches(0.75)
        section.left_margin = Inches(0.75)
        section.right_margin = Inches(0.75)
        section.different_first_page_header_footer = False

        footer = section.footer
        f_p = footer.paragraphs[0]
        f_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        f_run = f_p.add_run(MANDATORY_FOOTER)
        f_run.font.name = "Arial"
        f_run.font.size = Pt(8.5)
        f_run.font.bold = True
        f_run.font.color.rgb = C_MAROON

    # ==================== COVER / INITIATIVE HEADER ====================
    # Top Pre-Title
    p_pre = doc.add_paragraph()
    p_pre.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_pre.paragraph_format.space_before = Pt(12)
    p_pre.paragraph_format.space_after = Pt(2)
    r_pre = p_pre.add_run("SRI SHRIPAD KULKARNI'S CANONICAL INITIATIVE\n")
    r_pre.font.name = "Arial"
    r_pre.font.size = Pt(10)
    r_pre.font.bold = True
    r_pre.font.color.rgb = C_GOLD

    # Main Title
    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_before = Pt(0)
    p_title.paragraph_format.space_after = Pt(4)
    r_title = p_title.add_run("UDYAM SUTRAS: THE FIRST TEN APPROVED CANONICAL SUTRAS\n")
    r_title.font.name = "Georgia"
    r_title.font.size = Pt(18)
    r_title.font.bold = True
    r_title.font.color.rgb = C_MAROON

    # Subtitle
    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_sub.paragraph_format.space_before = Pt(0)
    p_sub.paragraph_format.space_after = Pt(10)
    r_sub = p_sub.add_run("Synthesized by the Five-Agent AI Council (Narada × Shandilya × Bharatiya Jnana → Sutrakar → Independent Validator)")
    r_sub.font.name = "Arial"
    r_sub.font.size = Pt(9.5)
    r_sub.font.italic = True
    r_sub.font.color.rgb = C_SLATE

    # Metadata Table (2x2 Grid)
    meta_tbl = doc.add_table(rows=2, cols=4)
    meta_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    meta_data = [
        [("Primary Author / Idea:", True), ("Shri Shripad Kulkarni", False), 
         ("Date of Approval:", True), ("November 07, 2026", False)],
        [("Technology Partner:", True), ("Hiranyam AI Labs (https://hiranyamai.com/)", False), 
         ("Council Approval:", True), ("10/10 Approved by Agent 5", False)]
    ]

    for row_idx, row in enumerate(meta_data):
        for col_idx, (text, is_label) in enumerate(row):
            cell = meta_tbl.cell(row_idx, col_idx)
            set_cell_background(cell, "FBF9F5" if is_label else "FFFFFF")
            set_cell_margins(cell, top=60, bottom=60, left=100, right=100)
            set_cell_borders(cell, top="single", bottom="single", left="single", right="single", color="E2E8F0", sz="4")
            cp = cell.paragraphs[0]
            cp.paragraph_format.space_after = Pt(0)
            crun = cp.add_run(text)
            crun.font.name = "Arial"
            crun.font.size = Pt(8.5)
            if is_label:
                crun.font.bold = True
                crun.font.color.rgb = C_NAVY
            else:
                crun.font.color.rgb = C_DARK_TEXT

    # Divider paragraph
    div_p = doc.add_paragraph()
    div_p.paragraph_format.space_before = Pt(12)
    div_p.paragraph_format.space_after = Pt(8)

    # ==================== TEN CANONICAL SUTRAS ====================
    for idx, s in enumerate(TEN_SUTRAS_DATA):
        if idx > 0:
            doc.add_page_break()

        s_num = s["sutra_no"]
        s_title = s["title"]

        # 1. Header Banner
        h_tbl = doc.add_table(rows=1, cols=1)
        h_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        h_cell = h_tbl.cell(0, 0)
        set_cell_background(h_cell, "1A365D")  # Deep Navy Banner
        set_cell_margins(h_cell, top=90, bottom=90, left=140, right=140)
        set_cell_borders(h_cell, top="none", bottom="none", left="none", right="none")
        h_p = h_cell.paragraphs[0]
        h_p.paragraph_format.space_after = Pt(0)
        hrun = h_p.add_run(f"UDYAM SUTRA {s_num}: {s_title}")
        hrun.font.name = "Arial"
        hrun.font.size = Pt(10.5)
        hrun.font.bold = True
        hrun.font.color.rgb = RGBColor(255, 255, 255)

        # Spacing
        sp1 = doc.add_paragraph()
        sp1.paragraph_format.space_before = Pt(6)
        sp1.paragraph_format.space_after = Pt(0)

        # 2. Sanskrit Shloka Box
        shloka_tbl = doc.add_table(rows=1, cols=1)
        shloka_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        s_cell = shloka_tbl.cell(0, 0)
        set_cell_background(s_cell, "FDFBF7")  # Warm Light Parchment
        set_cell_margins(s_cell, top=120, bottom=120, left=160, right=160)
        set_cell_borders(s_cell, top="single", bottom="single", left="single", right="single", color="B8860B", sz="8")
        
        sp = s_cell.paragraphs[0]
        sp.alignment = WD_ALIGN_PARAGRAPH.CENTER
        sp.paragraph_format.space_after = Pt(4)
        r_dev = sp.add_run(f"{s['shloka_devanagari']}\n")
        r_dev.font.name = "Georgia"
        r_dev.font.size = Pt(12)
        r_dev.font.bold = True
        r_dev.font.color.rgb = C_MAROON

        r_iast = sp.add_run(s['shloka_iast'])
        r_iast.font.name = "Georgia"
        r_iast.font.size = Pt(9.5)
        r_iast.font.italic = True
        r_iast.font.color.rgb = C_SLATE

        # Spacing
        sp2 = doc.add_paragraph()
        sp2.paragraph_format.space_before = Pt(6)
        sp2.paragraph_format.space_after = Pt(2)

        # 3. Source References (Foundational Texts) Heading
        src_head_p = doc.add_paragraph()
        src_head_p.paragraph_format.space_before = Pt(4)
        src_head_p.paragraph_format.space_after = Pt(2)
        r_sh = src_head_p.add_run("Source References (Foundational Texts):")
        r_sh.font.name = "Arial"
        r_sh.font.size = Pt(9.5)
        r_sh.font.bold = True
        r_sh.font.color.rgb = C_MAROON

        # Source References Table (3 Rows x 2 Cols)
        src_tbl = doc.add_table(rows=3, cols=2)
        src_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        src_rows = [
            ("Narad Bhakti Sutra:", s["sources"]["narada"]),
            ("Shandilya Bhakti Sutra:", s["sources"]["shandilya"]),
            ("Bharatiya Jnana Tradition:", s["sources"]["bharatiya_jnana"]),
        ]
        for r_i, (label, val_text) in enumerate(src_rows):
            c_lbl = src_tbl.cell(r_i, 0)
            c_val = src_tbl.cell(r_i, 1)

            set_cell_background(c_lbl, "F8FAFC")
            set_cell_background(c_val, "FFFFFF")
            set_cell_margins(c_lbl, top=50, bottom=50, left=80, right=80)
            set_cell_margins(c_val, top=50, bottom=50, left=80, right=80)
            set_cell_borders(c_lbl, top="single", bottom="single", left="single", right="single", color="E2E8F0", sz="4")
            set_cell_borders(c_val, top="single", bottom="single", left="single", right="single", color="E2E8F0", sz="4")

            p_l = c_lbl.paragraphs[0]
            p_l.paragraph_format.space_after = Pt(0)
            rl = p_l.add_run(label)
            rl.font.name = "Arial"
            rl.font.size = Pt(8.5)
            rl.font.bold = True
            rl.font.color.rgb = C_NAVY

            p_v = c_val.paragraphs[0]
            p_v.paragraph_format.space_after = Pt(0)
            rv = p_v.add_run(val_text)
            rv.font.name = "Georgia"
            rv.font.size = Pt(8.5)
            rv.font.color.rgb = C_DARK_TEXT

        # Spacing
        sp3 = doc.add_paragraph()
        sp3.paragraph_format.space_before = Pt(6)
        sp3.paragraph_format.space_after = Pt(0)

        # 4. English Translation
        en_p = doc.add_paragraph()
        en_p.paragraph_format.space_before = Pt(4)
        en_p.paragraph_format.space_after = Pt(4)
        r_enl = en_p.add_run("English Translation: ")
        r_enl.font.name = "Arial"
        r_enl.font.size = Pt(9)
        r_enl.font.bold = True
        r_enl.font.color.rgb = C_MAROON
        r_ent = en_p.add_run(s["english_translation"])
        r_ent.font.name = "Arial"
        r_ent.font.size = Pt(9)
        r_ent.font.color.rgb = C_DARK_TEXT

        # 5. Marathi Purport (मराठी विवेचन व भावार्थ)
        mr_p = doc.add_paragraph()
        mr_p.paragraph_format.space_before = Pt(4)
        mr_p.paragraph_format.space_after = Pt(4)
        r_mrl = mr_p.add_run("मराठी विवेचन व भावार्थ: ")
        r_mrl.font.name = "Arial"
        r_mrl.font.size = Pt(9)
        r_mrl.font.bold = True
        r_mrl.font.color.rgb = C_MAROON
        r_mrt = mr_p.add_run(s["marathi_purport"])
        r_mrt.font.name = "Georgia"
        r_mrt.font.size = Pt(9)
        r_mrt.font.color.rgb = C_DARK_TEXT

        # 6. Philosophical Foundation (तत्त्वज्ञानात्मक अधिष्ठान)
        phil_p = doc.add_paragraph()
        phil_p.paragraph_format.space_before = Pt(4)
        phil_p.paragraph_format.space_after = Pt(4)
        r_pl = phil_p.add_run("Philosophical Foundation (तत्त्वज्ञानात्मक अधिष्ठान): ")
        r_pl.font.name = "Arial"
        r_pl.font.size = Pt(9)
        r_pl.font.bold = True
        r_pl.font.color.rgb = C_NAVY
        r_pt = phil_p.add_run(s["philosophical_foundation"])
        r_pt.font.name = "Georgia"
        r_pt.font.size = Pt(9)
        r_pt.font.color.rgb = C_DARK_TEXT

        # 7. Practical Application in Business & Management
        app_head_p = doc.add_paragraph()
        app_head_p.paragraph_format.space_before = Pt(4)
        app_head_p.paragraph_format.space_after = Pt(2)
        r_apl = app_head_p.add_run("Practical Application in Business & Management:")
        r_apl.font.name = "Arial"
        r_apl.font.size = Pt(9)
        r_apl.font.bold = True
        r_apl.font.color.rgb = C_GOLD

        for bullet_label, bullet_text in s["practical_applications"]:
            b_p = doc.add_paragraph()
            b_p.paragraph_format.left_indent = Inches(0.25)
            b_p.paragraph_format.space_before = Pt(1)
            b_p.paragraph_format.space_after = Pt(2)
            r_bl = b_p.add_run(f"• {bullet_label}: ")
            r_bl.font.name = "Arial"
            r_bl.font.size = Pt(8.5)
            r_bl.font.bold = True
            r_bl.font.color.rgb = C_DARK_TEXT
            r_bt = b_p.add_run(bullet_text)
            r_bt.font.name = "Georgia"
            r_bt.font.size = Pt(8.5)
            r_bt.font.color.rgb = C_SLATE

    # Save to disk and mirror to brain artifact directory
    doc.save(str(OUTPUT_DOCX))
    artifact_path = ARTIFACT_DIR / OUTPUT_DOCX.name
    shutil.copyfile(str(OUTPUT_DOCX), str(artifact_path))
    print(f"[Successfully generated document]: {OUTPUT_DOCX}")
    print(f"[Successfully mirrored to brain artifact]: {artifact_path}")

if __name__ == "__main__":
    build_reformatted_canonical_document()
