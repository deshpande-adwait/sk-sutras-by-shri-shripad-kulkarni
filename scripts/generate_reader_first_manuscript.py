"""
================================================================================
Script: scripts/generate_reader_first_manuscript.py
Author: Hiranyam AI Labs (https://hiranyamai.com/)
Project: SK Sutras - by Shri Shripad Kulkarni
Description: Generates the comprehensive, publication-ready, reader-first Word
             manuscript for the 10 Canonical Udyog Sutras with strictly ZERO
             technical jargon. Enforces the mandatory sequence:
             SOURCE FIRST -> SOURCE MEANING -> DERIVATION / CONNECTION ->
             NEW UDYOGA SUTRA -> ITS TRANSLATION -> DETAILED EXPLANATION ->
             PRACTICAL EXAMPLES -> DOS & DON'TS -> KEY TAKEAWAY.
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

# Target Output Directory & Files (Preserves original file untouched)
OUTPUT_DIR = BASE_DIR / "docs" / "reader_first_edition"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_FILE = OUTPUT_DIR / "SK_SUTRAS_UDYOGA_SUTRAS_READER_FIRST_EDITION.docx"

ARTIFACT_DIR = Path(r"C:\Users\deshp\.gemini\antigravity\brain\94293167-6c7d-4773-b091-412c085b8cdc")
ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)
ARTIFACT_FILE = ARTIFACT_DIR / "SK_SUTRAS_UDYOGA_SUTRAS_READER_FIRST_EDITION.docx"

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


def _clean_doc_code(text_val: Any) -> str:
    """Cleans internal document codes (DOC-01 to DOC-04) into classical titles."""
    val = str(text_val or "")
    val = re.sub(r"DOC-01\s*(\([^)]*\))?:?\s*", "उद्योग महाग्रंथ विचार: ", val)
    val = re.sub(r"DOC-02\s*(\([^)]*\))?:?\s*", "नीतिपूर्ण व्यापार व आचारसंहिता: ", val)
    val = re.sub(r"DOC-03\s*(\([^)]*\))?:?\s*", "स्वावलंबन व संकटात संयम: ", val)
    val = re.sub(r"DOC-04\s*(\([^)]*\))?:?\s*", "संत तुकाराम महाराज विचार: ", val)
    val = re.sub(r"•\s*\[\]:\s*", "• ", val)
    return val.strip()


# Precise Transliteration Mappings for Source Verses & New Sutras
TRANSLITERATIONS = {
    "narada": {
        1: "athāto bhaktiṁ vyākhyāsyāmaḥ ||",
        2: "sā tvasmin paramapremarūpā ||",
        3: "amṛtasvarūpā ca ||",
        4: "yallabdhvā pumān siddho bhavati amṛto bhavati tṛpto bhavati ||",
        5: "yatprāpya na kiñcid vāñchati na śocati na dveṣṭi na ramate notsāhī bhavati ||",
        6: "yajjñātvā matto bhavati stabdho bhavati ātmārāmo bhavati ||",
        7: "sā na kāmayamānā nirodharūpatvāt ||",
        8: "nirodhastu lokavedavyāpāranyāsaḥ ||",
        9: "tasminnananyatā tadvirodhiṣūdāsīnatā ca ||",
        10: "anyāśrayāṇāṁ tyāgo'nanyatā ||"
    },
    "shandilya": {
        1: "athāto bhaktijijñāsā ||",
        2: "sā parānuraktirīśvare ||",
        3: "sa ca bhaktiprasādāt ||",
        4: "prārabdhakṣaye paramaṁ padam ||",
        5: "namaskāraśca bhaktyā ||",
        6: "bhaktimataḥ sarvaṁ saphalaṁ bhavati ||",
        7: "na kriyā paraprayojanābhāvāt ||",
        8: "tannyāsaśca bhaktau ||",
        9: "pātakanāśanaṁ ca ||",
        10: "dainyaṁ ca śaraṇāgatiḥ ||"
    },
    "new_sutra": {
        1: "|| athāto udyogajijñāsā || 1 ||",
        2: "udyogaḥ svakarmaṇi paramānuraktiḥ || 2 ||",
        3: "|| karmabhaktiprasādāt siddhiḥ || 3 ||",
        4: "|| niṣkāmodyamena paramā tṛptiḥ || 4 ||",
        5: "|| namrodyamo bhaktiḥ || 5 ||",
        6: "|| udyoganiṣṭhasya sarvaṁ saphalam || 6 ||",
        7: "|| niṣkāmodyogaḥ svayaṁpūrṇaḥ || 7 ||",
        8: "|| karmārpaṇameva nirodhaḥ || 8 ||",
        9: "|| dharmaniṣṭhayā doṣakṣayaḥ || 9 ||",
        10: "|| vinayena dharmaikāśrayaḥ || 10 ||"
    }
}

# Concrete Actionable DOs & DON'Ts for Modern Enterprise tailored to each Sutra
DOS_AND_DONTS = {
    1: {
        "dos": [
            "नवीन व्यवसाय किंवा प्रकल्प सुरू करण्यापूर्वी ग्राहकाची खरी समस्या, बाजार आणि स्वतःची क्षमता यांवर किमान ३० प्रत्यक्ष संवाद व क्षेत्रीय चाचण्या करा.",
            "प्रत्येक प्रकल्पाच्या सुरुवातीला 'आम्ही हे का करत आहोत, कोणासाठी करत आहोत आणि कोणत्या मूल्यांनी करणार आहोत?' या तीन प्रश्नांची स्पष्ट लेखी सनद निश्चित करा.",
            "भांडवल आणि वेळ गुंतवण्यापूर्वी सखोल जिज्ञासा आणि अभ्यासाची शिस्त पाळा; ज्ञान हीच पायाभूत गुंतवणूक माना."
        ],
        "donts": [
            "केवळ उत्साहाच्या किंवा देखाव्याच्या भरात कसलीही पूर्वतयारी व चौकशी न करता थेट भांडवल ओतण्याची घाई करू नका.",
            "ग्राहकाच्या खऱ्या समस्येकडे दुर्लक्ष करून स्वतःच्या पूर्वग्रहावर किंवा कल्पनेवर आंधळा विश्वास ठेवणे टाळा.",
            "जलद नफ्याच्या मोहात पडून सुरुवातीलाच नैतिक मूल्यांशी किंवा कायद्याशी कोणतीही तडजोड करू नका."
        ],
        "reflection_question": "माझ्या चालू व्यवसायाची किंवा नवीन प्रकल्पाची सुरुवात खऱ्या लोककल्याणकारी जिज्ञासेतून झाली आहे, की केवळ आंधळ्या नफ्याच्या स्पर्धेतून?",
        "takeaway": "उत्तुंग भरारीपूर्वी सखोल जिज्ञासा हीच शाश्वत उद्योगाची पहिली पायरी आहे."
    },
    2: {
        "dos": [
            "आपल्या धर्मसंमत स्वकर्मावर, उत्पादनाच्या गुणवत्तेवर आणि ग्राहकाच्या सेवेवर मनापासून अखंड निष्ठा व प्रेम ठेवा.",
            "नफ्याला अंतिम ध्येय न मानता कामातील उत्कृष्टतेचे स्वाभाविक फळ (By-product) म्हणून स्वीकारा.",
            "कमावलेली संपत्ती समाजाची न्यासठेव (Trust) मानून तिचा विनियोग समाजोन्नतीसाठी उदास विचाराने करा."
        ],
        "donts": [
            "केवळ जलद पैसे कमावण्याच्या लोभाने स्वतःच्या मूल्यांविरुद्ध जाणारे किंवा समाजाला हानी पोहोचवणारे काम निवडणे टाळा.",
            "कामातील कारागिरी आणि प्रामाणिकपणा सोडून केवळ देखावा, मार्केटिंग आणि फुगवलेल्या प्रचारावर अवलंबून राहणे टाळा.",
            "ग्राहकाला किंवा सहकाऱ्यांना फसवून तात्पुरता आर्थिक लाभ मिळवण्याची घातक प्रवृत्ती मुळापासून टाळा."
        ],
        "reflection_question": "मी माझ्या दैनंदिन कामात केवळ नफा मोजत आहे, की माझ्या उत्पादनात आणि सेवेत माझे संपूर्ण समर्पण व प्रेम ओतत आहे?",
        "takeaway": "कामावरील पराकोटीची निष्ठा हीच उद्योगाला ईश्वरी उपासनेचे पावित्र्य मिळवून देते."
    },
    3: {
        "dos": [
            "रोजचे कर्तव्यकर्म पूर्ण कौशल्याने, प्रामाणिकपणे आणि शांत एकाग्रतेने पार पाडा.",
            "यशाला कामावरील भक्तीतून लाभणारा 'प्रसाद' मानून सदैव कृतज्ञ, विनयशील आणि पाय जमिनीवर ठेवणारे राहा.",
            "संकटात किंवा कठीण प्रसंगातही खचून न जाता सक्रिय उद्योग, सातत्य आणि दक्षता (उत्थान) अखंड चालू ठेवा."
        ],
        "donts": [
            "यशाचा अहंकार बाळगून 'सर्व काही माझ्या एकट्यामुळे झाले' अशी उद्धट भावना मनात आणणे टाळा.",
            "कष्टांची तयारी न ठेवता केवळ नशिबावर किंवा बाह्य मदतीवर अवलंबून राहून निष्क्रिय बसणे टाळा.",
            "निकालाच्या अवाजवी चिंतेने (Outcome Anxiety) त्रस्त होऊन हातातील चालू कामाचा दर्जा घसरू देणे टाळा."
        ],
        "reflection_question": "यशाच्या क्षणी मी अहंकाराने फुगून जातो, की कामातून मिळालेला प्रसाद मानून सहकाऱ्यांप्रती कृतज्ञ होतो?",
        "takeaway": "समर्पित कर्मातून लाभलेली चित्तप्रसन्नता हीच अढळ यशाची जननी आहे."
    },
    4: {
        "dos": [
            "प्रक्रियेवर (Process) आणि कर्माच्या दर्जावर पूर्ण लक्ष केंद्रित करा; फळाच्या अधिकाराचा हव्यास सोडा.",
            "संस्थेला व्यक्तीनिरपेक्ष करण्यासाठी उत्तम कार्यप्रणाली, उत्तराधिकार योजना आणि पारदर्शक कारभार उभारा.",
            "प्रत्येक दिवसाच्या शेवटी मिळालेल्या पैशांपेक्षा कर्तव्यपूर्तीचे अंतर्गत समाधान आणि शांत झोप मोजा."
        ],
        "donts": [
            "केवळ पुढील तिमाहीच्या नफ्याचा किंवा मूल्यांकनाचा दबाव आणून सहकाऱ्यांचे मानसिक व शारीरिक शोषण करणे टाळा.",
            "संस्थेला स्वतःची खाजगी जहागीर समजून सर्व अधिकार स्वतःभोवती केंद्रित ठेवण्याची चूक टाळा.",
            "तात्पुरत्या अपयशाने निराश होऊन किंवा बाजार घसरल्याने स्वतःचे मूळ ध्येय आणि मूल्ये बदलणे टाळा."
        ],
        "reflection_question": "माझे समाधान केवळ बँक खात्यातील आकड्यांवर अवलंबून आहे, की कामातील प्रामाणिक कर्तव्यपूर्तीवर?",
        "takeaway": "फळाच्या चिंतेतून मुक्त होऊन केलेल्या उत्कृष्ट कर्मातूनच सर्वोच्च समाधान लाभते."
    },
    5: {
        "dos": [
            "यशाचे संपूर्ण श्रेय जाहीरपणे आपल्या सहकाऱ्यांना, कामगारांना आणि ग्राहकांना विनम्रतेने द्या.",
            "ग्राहक, सहकारी आणि अगदी कनिष्ठ कर्मचाऱ्यांचा अभिप्रायही आदरपूर्वक ऐकून स्वतःमध्ये सतत सुधारणा करा.",
            "आपल्या अधिकाराचा आणि संपत्तीचा उपयोग संस्थेतील प्रत्येकाच्या उन्नतीसाठी व कल्याणासाठी करा."
        ],
        "donts": [
            "संस्थेत स्वतःचा अहंकार किंवा 'मी म्हणेन तेच अंतिम सत्य' ही एकाधिकारशाही वृत्ती बाळगणे टाळा.",
            "सहकाऱ्यांच्या कष्टाचे श्रेय स्वतः लाटणे आणि चुकांचे खापर इतरांच्या माथ्यावर फोडणे टाळा.",
            "यशाच्या कैफात लहान पुरवठादार, कारागीर किंवा नवख्या व्यक्तींचा अनादर करणे टाळा."
        ],
        "reflection_question": "मी अधिकार गाजवणारा मालक म्हणून वागत आहे, की सर्वांची सेवा करणारा नम्र विश्वस्त म्हणून?",
        "takeaway": "अहंकाराचा लोप करून विनीत भावाने केलेला उद्यम हीच खरी ईश्वरपूजा आहे."
    },
    6: {
        "dos": [
            "लहान असो वा मोठे, प्रत्येक कामात उत्कृष्टतेची सर्वोच्च मानके आणि काटेकोर शिस्त पाळा.",
            "बाजारातील कोणत्याही वादळात किंवा मंदीत आपल्या नैतिक तत्त्वांशी आणि सत्यवचनाशी प्रामाणिक राहा.",
            "ग्राहकाला दिलेला शब्द, कामाचा दर्जा आणि वेळेवर देयके देऊन विश्वासार्हतेचे भांडवल कमवा."
        ],
        "donts": [
            "तात्कालिक अडचण आली म्हणून कामाचा दर्जा कमी करणे किंवा निकृष्ट घटकांचा वापर करणे टाळा.",
            "अल्पावधीत मोठे होण्याच्या हव्यासापोटी संस्थेची मूळ मूल्ये आणि सुरक्षितता धोक्यात आणणे टाळा.",
            "स्पर्धकाला हरवण्यासाठी अफवा पसरवणे, खोटी विधाने करणे किंवा अनैतिक हेरगिरी करणे टाळा."
        ],
        "reflection_question": "माझी निष्ठा केवळ तात्पुरत्या आर्थिक लाभावर टिकून आहे, की कर्माच्या शाश्वत उत्कृष्टतेवर?",
        "takeaway": "सत्यावर आणि गुणवत्तेवर अढळ निष्ठा ठेवणारा उद्योजक कधीही अपयशी होत नाही."
    },
    7: {
        "dos": [
            "उद्योगाला स्वतःच एक तपश्चर्या आणि जीवनसाधना मानून कर्माच्या प्रत्येक क्षणात परिपूर्ण आनंद घ्या.",
            "बाह्य स्तुती, प्रसिद्धी किंवा पुरस्कारांवर विसंबून न राहता स्वतःच्या विवेकाच्या कसोटीवर खरे उतरा.",
            "शाश्वत, पर्यावरणपूरक आणि समाजहितैषी व्यवसाय मॉडेल उभे करा जे दीर्घकाळ टिकून राहील."
        ],
        "donts": [
            "केवळ गुंतवणूकदारांना भुलवण्यासाठी किंवा कंपनीची खोटी पत वाढवण्यासाठी आकडे फुगवणे टाळा.",
            "नैतिकतेचा आणि सामाजिक उत्तरदायित्वाचा वापर केवळ प्रसिद्धीचे साधन (PR Stunt) म्हणून करणे टाळा.",
            "स्वतःच्या नफ्यासाठी नैसर्गिक साधनसंपत्तीचे किंवा समाजाचे अवाजवी शोषण करणे टाळा."
        ],
        "reflection_question": "माझा उद्योग बाह्य टाळ्यांवर आणि मूल्यांकनावर जगत आहे, की स्वतःच्या आंतरिक मूल्यांनी स्वयंपूर्ण आहे?",
        "takeaway": "फळाच्या भुकेतून मुक्त झालेला उद्यम स्वतःच एक परिपूर्ण आणि आनंदी जीवनमार्ग बनतो."
    },
    8: {
        "dos": [
            "सर्व व्यावसायिक व्यवहार पूर्ण ताकदीने आणि कौशल्याने चालवा, पण कर्तेपणाचा अहंकार ईश्वराला अर्पण करा.",
            "कठीण प्रसंगात आणि अनपेक्षित नुकसानीत 'प्रयत्न माझे, निकाल नियतीचा' या न्यायाने निर्भय राहा.",
            "मिळालेल्या नफ्यातून समाजातील गरजू घटकांसाठी, शिक्षणासाठी व आरोग्यासाठी नियमित वाटा राखून ठेवा."
        ],
        "donts": [
            "वैराग्याचा चुकीचा अर्थ काढून कामाचा आळस करणे किंवा व्यावसायिक जबाबदाऱ्या झटकून पळणे टाळा.",
            "मिळालेल्या संपत्तीला स्वतःची खाजगी जहागीर मानून तिचा अपव्यय किंवा अहंकार करणे टाळा.",
            "निर्णय घेताना भीतीपोटी किंवा स्वार्थापोटी नैतिक जबाबदारीपासून दूर पळणे टाळा."
        ],
        "reflection_question": "मी माझ्या व्यवसायाचे सर्व व्यवहार समाजहित आणि नीतिमत्तेच्या चरणी समर्पित भावनेने करत आहे का?",
        "takeaway": "कर्मत्याग नव्हे, तर अहंकाराचा त्याग करून केलेले कर्मार्पण म्हणजेच खरा उद्योगसंन्यास."
    },
    9: {
        "dos": [
            "व्यवसायात नकळत चूक किंवा प्रमाद घडल्यास तो त्वरित मान्य करा आणि बाधितांची सन्मानाने भरपाई करा.",
            "प्रत्येक चुकीनंतर दोषारोप न करता मूळ कारणाचा शोध घेऊन कायमस्वरूपी प्रक्रिया-सुधारणा लागू करा.",
            "कितीही मोठा दबाव आला तरी कायद्याची चौकट आणि नीतीचा मार्ग न सोडणारा कणखरपणा दाखवा."
        ],
        "donts": [
            "झालेली चूक झाकण्यासाठी खोट्याचा आधार घेणे, आकडे बदलणे किंवा तपास यंत्रणांची दिशाभूल करणे टाळा.",
            "आपल्या चुकीचे खापर हाताखालील निष्पाप कर्मचाऱ्यांवर फोडून स्वतः नामानिराळे राहणे टाळा.",
            "अडचणीतून सुटण्यासाठी लाचखोरी, वशिला किंवा अनैतिक समझोते करणे पूर्णपणे टाळा."
        ],
        "reflection_question": "संकटाच्या वेळी मी चूक लपवण्याचा प्रयत्न करतो, की धर्मनिष्ठेने ती सुधारून सत्यावर ठाम राहतो?",
        "takeaway": "धर्मावरील अढळ निष्ठा आणि प्रामाणिक सुधारणा हीच भूतकाळातील दोषांचे क्षालन करते."
    },
    10: {
        "dos": [
            "प्रत्येक महत्त्वाच्या निर्णयाच्या क्षणी 'हा निर्णय धर्मसंमत, सत्य आणि न्याय्य आहे का?' ही एकच कसोटी लावा.",
            "शॉर्टकट, राजकीय वशिलेबाजी आणि अहंकाराचे सर्व कुबडे फेकून देऊन केवळ स्वकर्तृत्व आणि धर्माचा आश्रय घ्या.",
            "सर्व भागधारकांशी (ग्राहक, कर्मचारी, समाज) पारदर्शक आणि निर्मळ नाते जोपासा."
        ],
        "donts": [
            "व्यवसायाच्या वाढीसाठी किंवा संरक्षणासाठी भ्रष्ट हितसंबंधांवर किंवा बेकायदेशीर मार्गांवर अवलंबून राहणे टाळा.",
            "स्वतःला कायद्यापेक्षा आणि नैतिकतेपेक्षा श्रेष्ठ समजण्याची घमेंड मनात बाळगणे टाळा.",
            "अल्पकालीन नफ्यासाठी दीर्घकालीन विश्वासार्हता पणाला लावण्याची चूक टाळा."
        ],
        "reflection_question": "माझ्या व्यवसायाचा खरा आधार काय आहे — तात्पुरती वशिलेबाजी आणि शॉर्टकट, की अढळ धर्मनिष्ठा?",
        "takeaway": "विनम्रतेने धर्माचा एकच आश्रय घेणारा नेता कोणत्याही वादळात निर्भय आणि अजेय राहतो."
    }
}


def build_reader_first_document(
    sutras: Optional[List[Dict[str, Any]]] = None,
    output_path: Optional[Path] = None,
) -> Path:
    """
    ================================================================================
    Function: build_reader_first_document
    Purpose: Generates the authoritative, reader-first Word manuscript (.docx)
             following the strict pedagogical sequence:
             SOURCE FIRST -> SOURCE MEANING -> DERIVATION / CONNECTION ->
             NEW UDYOGA SUTRA -> ITS TRANSLATION -> DETAILED EXPLANATION ->
             PRACTICAL EXAMPLES -> DOS & DON'TS -> KEY TAKEAWAY.
    Parameters:
        - sutras: Canonical sutra data (defaults to TEN_NEW_UDYOG_SUTRAS_CANON).
        - output_path: Destination path (defaults to OUTPUT_FILE).
    Returns:
        - Path: Absolute path to the generated document.
    ================================================================================
    """
    target_sutras = sutras if sutras is not None else TEN_NEW_UDYOG_SUTRAS_CANON
    target_output = output_path if output_path is not None else OUTPUT_FILE

    doc = docx.Document()

    # Configure Margins and Mandatory Footer across all sections
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

    # ==================== COVER / TITLE PAGE ====================
    title_p = doc.add_paragraph()
    title_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    title_p.paragraph_format.space_before = Pt(16)
    title_p.paragraph_format.space_after = Pt(4)
    r_t1 = title_p.add_run("॥ श्रीमद् उद्योग सूत्राणि ॥\n")
    r_t1.font.name = "Georgia"
    r_t1.font.size = Pt(24)
    r_t1.font.bold = True
    r_t1.font.color.rgb = C_MAROON

    r_t2 = title_p.add_run("SHRIMAD UDYOG SUTRAS – TEN CANONICAL SUTRAS\n")
    r_t2.font.name = "Arial"
    r_t2.font.size = Pt(13)
    r_t2.font.bold = True
    r_t2.font.color.rgb = C_NAVY

    r_t3 = title_p.add_run("दस प्रामाणिक उद्योग सूत्रे : मूळ ज्ञानस्रोत, सुलभ निरूपण व दैनंदिन आचरण\n")
    r_t3.font.name = "Georgia"
    r_t3.font.size = Pt(11.5)
    r_t3.font.italic = True
    r_t3.font.color.rgb = C_SLATE

    # Metadata Banner
    meta_tbl = doc.add_table(rows=1, cols=1)
    meta_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    meta_cell = meta_tbl.cell(0, 0)
    set_cell_background(meta_cell, "FBF9F5")
    set_cell_margins(meta_cell, top=100, bottom=100, left=160, right=160)
    m_p = meta_cell.paragraphs[0]
    m_p.alignment = WD_ALIGN_PARAGRAPH.CENTER

    m_p.add_run("ग्रंथकार (Author): श्री श्रीपाद कुलकर्णी (Shri Shripad Kulkarni)\n")
    m_p.add_run("मार्गदर्शक तत्त्व: 'सूत्र लहान, विचार महान, निरूपण सुटसुटीत, संक्षिप्त आणि आचरण व्यावहारिक'\n")
    m_p.add_run(
        "सद्ग्रंथ प्रेरणा: नारद भक्ती सूत्रे, शांडिल्य भक्ती सूत्रे, श्रीमद्भगवद्गीता, कौटिलीय अर्थशास्त्र, "
        "संत तुकाराम महाराज अभंगगाथा, समर्थ रामदास दासबोध, ईशावास्योपनिषद, पतंजली योगसूत्रे, भर्तृहरी नीतिशतक व विदुरनीती\n"
    )
    m_p.add_run("प्रकाशन आवृत्ती: २०२६ | वाचक-सुलभ संस्करण (Reader-First Edition)\n")
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
        ("१. प्रस्तावना : हे पुस्तक का लिहिले? (Introduction — Why this book?)", "Front Matter"),
        ("२. 'उद्योग सूत्र' म्हणजे काय? (What is an Udyoga Sutra?)", "Front Matter"),
        ("३. ज्ञानस्रोत व सद्ग्रंथ परंपरा (Sources & Knowledge Foundations)", "Front Matter"),
        ("४. उद्योग सूत्रांची निर्मिती कशी झाली? (How Udyoga Sutras are Derived)", "Front Matter"),
        ("५. प्रत्येक प्रकरणाचे वाचन कसे करावे? (How to Read Each Chapter)", "Front Matter"),
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
        s_theme = s_data["theme"].split("|")[0].replace("English:", "").strip()
        if len(s_theme) > 50:
            s_theme = s_theme[:47] + "..."

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

    # ==================== BOOK-LEVEL READER ORIENTATION ====================
    fm_headings = [
        ("१. प्रस्तावना : हे पुस्तक का लिहिले? (Introduction — Why this book?)", [
            "भारतीय संस्कृतीमध्ये ज्ञानाची, चिंतनाची आणि आचरणाची एक अखंड, समृद्ध परंपरा चालत आलेली आहे. सहस्रो वर्षांपूर्वी आपल्या ऋषी-मुनींनी जीवनाच्या अंतिम सत्याचा शोध घेताना जे सिद्धांत मांडले, ते केवळ अध्यात्मापुरते मर्यादित नव्हते. मानवी मनाचे नियम, कार्यकुशलता, सचोटी, समर्पण आणि सामाजिक कल्याण या सर्व अंगांना त्यामध्ये स्पर्श करण्यात आला होता.",
            "आज एकविसाव्या शतकात जेव्हा आपण जागतिक व्यापार, स्टार्टअप्स, कॉर्पोरेट व्यवस्थापन आणि उद्योजकतेच्या युगात वावरत आहोत, तेव्हा बाह्य तंत्रज्ञान बदलले असले तरी मूलभूत मानवी प्रश्न तेच आहेत: संकटात मन स्थिर कसे ठेवावे? यशाच्या शिखरावर असताना नैतिक तोल कसा सांभाळावा? केवळ नफ्याच्या मागे न लागता समाजोपयोगी मूल्ये कशी निर्माण करावीत? आणि कर्मचाऱ्यांना व सहकाऱ्यांना कामात खरा अर्थ कसा सापडेल?",
            "हे पुस्तक म्हणजे प्राचीन भारतीय ज्ञानपरंपरेतील (Bharatiya Jnana) शाश्वत मूल्यांचा आधुनिक उद्योग, व्यवसाय, नेतृत्व आणि व्यवस्थापनाशी घडवून आणलेला एक अत्यंत जिव्हाळापूर्ण व विचारप्रवर्तक संवाद आहे. या ग्रंथाचा उद्देश प्राचीन तत्त्वांचे केवळ गोडवे गाणे हा नसून, आधुनिक उद्योजकाला, संस्थापकाला आणि व्यवस्थापकाला दैनंदिन कामात प्रत्यक्ष दिशा देणारा एक व्यावहारिक आचारमार्ग खुला करून देणे हा आहे."
        ]),
        ("२. 'उद्योग सूत्र' म्हणजे काय? (What is an Udyoga Sutra?)", [
            "आपल्या परंपरेत 'सूत्र' या वाङ्मयप्रकाराला अनन्यसाधारण महत्त्व आहे. व्याकरणाच्या भाषेत सूत्राची व्याख्या करताना म्हटले आहे:\n'अल्पाक्षरमसंदिग्धं सारवद्विश्वतोमुखम् । अस्तोभमनवद्यं च सूत्रं सूत्रविदो विदुः ॥'\nम्हणजेच, कमीत कमी अक्षरे, संशयशून्य स्पष्टता, अथांग तत्त्वसार, सर्वतोमुखी उपयुक्तता आणि कोणताही निरर्थक शब्द नसलेली रचना म्हणजे सूत्र.",
            "या ग्रंथातील 'उद्योग सूत्र' म्हणजे आधुनिक व्यवसाय, नेतृत्व आणि उद्यमशीलतेचे मार्गदर्शक तत्त्व दर्शवणारे एक संक्षिप्त, लयबद्ध आणि स्मरणीय संस्कृत वचन आहे. 'सूत्र लहान, विचार महान' या सूत्रीय शिस्तीचे येथे काटेकोर पालन करण्यात आले आहे.",
            "सूत्र स्वतः आकाराने लहान असले तरी त्याचे 'निरूपण' (Exposition / Bhashya), त्याची 'सत्यकथा' (Real-life Case Studies) आणि दैनंदिन जीवनातील 'आचरण' (Actionable Steps) हे विस्तृत व सखोल आहेत. वाचक केवळ सूत्र वाचून थांबणार नाही, तर त्यामागील खोल विचार समजून घेऊन तो आपल्या उद्योगात प्रत्यक्ष अमलात आणू शकेल."
        ]),
        ("३. ज्ञानस्रोत व सद्ग्रंथ परंपरा (Sources and Knowledge Foundations)", [
            "हा ग्रंथ कोणत्याही कल्पनेवर किंवा हवेतील विचारांवर आधारलेला नाही. यातील प्रत्येक उद्योग सूत्र भारतीय ज्ञानपरंपरेतील मान्यताप्राप्त, प्रामाणिक सद्ग्रंथांवर आधारलेले आहे:",
            "• नारद भक्ती सूत्रे (Narada Bhakti Sutras): प्रेमाची, समर्पणाची आणि निःस्वार्थ सेवेची सर्वोच्च मानके देणारा आदिग्रंथ. यातील 'समर्पण' हे उद्योगात 'कामावरील अढळ निष्ठा' म्हणून अवतरते.\n"
            "• शांडिल्य भक्ती सूत्रे (Shandilya Bhakti Sutras): भक्तीला एक तार्किक, शिस्तबद्ध आणि बुद्धिमान शास्त्र म्हणून प्रस्थापित करणारा ग्रंथ. यातील 'जिज्ञासा' आणि 'परानुराग' हे उद्योजकीय संशोधनाचा पाया बनतात.\n"
            "• श्रीमद्भगवद्गीता (Bhagavad Gita): निष्काम कर्मयोग आणि 'लोकसंग्रह' (समाजाचे धारण-पोषण) यांची विश्वमान्य शिकवण.\n"
            "• कौटिलीय अर्थशास्त्र (Kautilya Arthashastra): सक्रिय उद्यमशीलता, अखंड दक्षता (उत्थान) आणि संपत्तीचे न्याय्य रक्षण.\n"
            "• संत तुकाराम महाराज अभंगगाथा: 'जोडोनियां धन उत्तम व्यवहारे । उदास विचारे वेच करी ॥' या वचनातून मिळणारा नैतिक संपत्तीनिर्मितीचा व विश्वस्तभावाचा संदेश.\n"
            "• समर्थ रामदास दासबोध: 'आधीं प्रचिती मग अनुमती' आणि कार्यकुशलतेचा अखंड वस्तुपाठ.\n"
            "• ईशावास्योपनिषद: 'तेन त्यक्तेन भुञ्जीथा मा गृधः कस्यस्विद्धनम्' — संपत्ती ही समाजाची न्यासठेव मानणारा उपनिषद विचार.\n"
            "• पतंजली योगसूत्रे: संस्थापकाचे व नेत्याचे मानसिक आरोग्य, ताणमुक्ती आणि संकटातील चित्तस्थैर्य.\n"
            "• भर्तृहरी नीतिशतक व विदुरनीती: कोणत्याही दबावाखाली सत्याचा आणि न्यायाचा मार्ग न सोडणारा धीरोदात्त नैतिक कणखरपणा.",
            "लक्षात घ्यावे: प्रत्येक प्रकरणाचे मूळ सूत्र त्या प्रकरणाच्या विषयानुसार योग्य त्या सद्ग्रंथातून निवडले आहे; कोणत्याही सूत्रावर कृत्रिमपणे एकाच ग्रंथाची सक्ती केलेली नाही."
        ]),
        ("४. उद्योग सूत्रांची निर्मिती कशी झाली? (How Udyoga Sutras are Derived)", [
            "या ग्रंथातील नवीन उद्योग सूत्रांची रचना एका अत्यंत जबाबदार, पाच-टप्प्यांच्या अभ्यासपूर्ण पद्धतीतून झाली आहे:",
            "१. मूळ तत्त्वाचा शोध (Source Identification): नारद व शांडिल्य भक्ती सूत्रांमधील किंवा इतर सद्ग्रंथांमधील मूळ संस्कृत श्लोक व त्याचा मूळ संदर्भातील अर्थ समजून घेणे.\n"
            "२. समकालीन उद्योगाशी संवाद (Enterprise Dialogue): त्या तत्त्वाचा आजच्या व्यवसाय, नेतृत्व, कर्मचारी-संबंध आणि ग्राहकसेवेमधील खरा अन्वयार्थ काय होतो, याचा सखोल विचार करणे.\n"
            "३. सूत्रीय संक्षेपण (Sutra Formulation): त्या विचाराला अत्यंत संक्षिप्त, पाणिनीय व्याकरणाला धरून आणि स्मरणीय अशा नव्या संस्कृत उद्योग सूत्रात गुंफणे. हे नवीन सूत्र आधुनिक काळातील असून ते प्राचीन श्लोकांचा आधुनिक आविष्कार आहे, प्राचीन उद्धरण नव्हे.\n"
            "४. बहुआयामी निरूपण (Comprehensive Exposition): सूत्राचे सुलभ मराठी विवेचन, ऐतिहासिक सत्यकथा आणि मानसिक संतुलनासाठी योगविचार मांडणे.\n"
            "५. प्रत्यक्ष आचारसंहिता (Actionable DOs & DON'Ts): आधुनिक संस्थापकांसाठी, व्यवस्थापकांसाठी आणि नेत्यांसाठी काय करावे व काय टाळावे, याचे स्पष्ट मार्गदर्शक नियम तयार करणे."
        ]),
        ("५. प्रत्येक प्रकरणाचे वाचन कसे करावे? (How to Read Each Chapter)", [
            "वाचकाला प्रत्येक प्रकरणात एका अत्यंत नैसर्गिक, शिस्तबद्ध आणि सुसंगत वाचन-प्रवासाचा अनुभव यावा, यासाठी संपूर्ण पुस्तकात एकच क्रम ठेवण्यात आला आहे:",
            "पायरी १ — मूळ आधार आणि संदर्भ श्लोक (Source Foundation): प्रथम मूळ सद्ग्रंथातील श्लोक, त्यांचा सरळ अर्थ आणि त्यांचा मूळ संदर्भ.\n"
            "पायरी २ — मूळ तत्त्वाकडून उद्योग सूत्राकडे (Derivation Bridge): त्या मूळ विचारातून आधुनिक उद्योग सूत्राची प्रेरणा कशी मिळाली, याचा वैचारिक सेतू.\n"
            "पायरी ३ — नवीन उद्योग सूत्र व भाषांतर (New Udyoga Sutra): नव्याने रचलेले संस्कृत उद्योग सूत्र, त्याचे मराठी व इंग्रजी भाषांतर आणि व्याकरण.\n"
            "पायरी ४ — सविस्तर विवेचन व निरूपण (Detailed Bhashya): सूत्राचा सखोल, सुटसुटीत तात्विक व व्यावहारिक अर्थ.\n"
            "पायरी ५ — व्यावहारिक उपयोजन व सत्यकथा (Practical Case Studies & Yoga): जागतिक व भारतीय उद्योगजगतातील सत्यकथा आणि पतंजली योगविचारातून मानसिक ताणमुक्ती.\n"
            "पायरी ६ — काय करावे आणि काय टाळावे (DOs & DON'Ts): आधुनिक उद्योगासाठी नेमकी, आचरणात आणण्याजोगी आचारसंहिता.\n"
            "पायरी ७ — चिंतन व अंतिम सूत्रसार (Reflection & Key Takeaway): अंतर्मुख करणारा प्रश्न आणि एका ओळीचा आचरण मंत्र."
        ])
    ]

    for title, paras in fm_headings:
        hp = doc.add_paragraph()
        hp.paragraph_format.space_before = Pt(12)
        hp.paragraph_format.space_after = Pt(4)
        hrun = hp.add_run(title)
        hrun.font.name = "Georgia"
        hrun.font.size = Pt(12.5)
        hrun.font.bold = True
        hrun.font.color.rgb = C_MAROON

        for para in paras:
            p = doc.add_paragraph()
            p.paragraph_format.space_before = Pt(2)
            p.paragraph_format.space_after = Pt(4)
            p.paragraph_format.line_spacing = 1.15
            run = p.add_run(para)
            run.font.name = "Georgia"
            run.font.size = Pt(9.5)
            run.font.color.rgb = C_SLATE

    doc.add_page_break()

    # ==================== TEN CANONICAL SUTRA CHAPTERS ====================
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

        s1_intro = doc.add_paragraph()
        s1_intro.paragraph_format.space_before = Pt(2)
        s1_intro.paragraph_format.space_after = Pt(4)
        r_s1_intro = s1_intro.add_run(
            "या प्रकरणातील तत्त्वाचा मूळ आधार प्राचीन भक्तिसूत्रांतील खालील दोन प्रामाणिक वचनांवर अधिष्ठित आहे. "
            "कोणत्याही नवीन विचाराकडे वळण्यापूर्वी प्रथम हे मूळ श्लोक, त्यांचे भाषांतर व त्यांचा मूळ संदर्भ समजून घेणे आवश्यक आहे:"
        )
        r_s1_intro.font.name = "Georgia"
        r_s1_intro.font.size = Pt(9)
        r_s1_intro.font.italic = True
        r_s1_intro.font.color.rgb = C_SLATE

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

        # Bharatiya Knowledge Base Foundations
        f_tbl = doc.add_table(rows=1, cols=1)
        f_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        f_cell = f_tbl.cell(0, 0)
        set_cell_background(f_cell, "F5F2EB")
        set_cell_margins(f_cell, top=50, bottom=50, left=100, right=100)
        fp = f_cell.paragraphs[0]
        fp.paragraph_format.space_after = Pt(0)
        fr1 = fp.add_run("भारतीय ज्ञान परंपरा व सद्ग्रंथ विचार (Bharatiya Wisdom Foundations):\n")
        fr1.font.name = "Arial"
        fr1.font.size = Pt(8.5)
        fr1.font.bold = True
        fr1.font.color.rgb = C_NAVY

        clean_doc01 = _clean_doc_code(bjf.get('doc01_mahadgrantha', ''))
        clean_doc02 = _clean_doc_code(bjf.get('doc02_karyavritti17', ''))
        clean_doc03 = _clean_doc_code(bjf.get('doc03_karyavritti05', ''))
        clean_doc04 = _clean_doc_code(bjf.get('doc04_sant_tukaram', ''))
        clean_iks = _clean_doc_code(bjf.get('iks_scriptural_references', ''))

        fr2 = fp.add_run(
            f"• {clean_doc01}\n"
            f"• {clean_doc02}\n"
            f"• {clean_doc03}\n"
            f"• {clean_doc04}\n"
            f"• प्राचीन सद्ग्रंथ संदर्भ: {clean_iks}"
        )
        fr2.font.name = "Georgia"
        fr2.font.size = Pt(8)
        fr2.font.color.rgb = C_SLATE

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
        dr2 = dp.add_run(
            f"{phil_text}\n\n"
            f"महत्त्वाची नोंद: पुढील उद्योग सूत्र हे कोणत्याही प्राचीन ग्रंथातील जशाच्या तसा घेतलेला श्लोक नाही. "
            f"तर वरील मूळ ज्ञानस्रोतांचे मंथन करून आधुनिक उद्योजकता, व्यवस्थापन, नेतृत्व आणि व्यावसायिक नीती यांच्या संदर्भात "
            f"नव्याने सूत्रबद्ध केलेले हे एक समकालीन, प्रामाणिक 'उद्योग सूत्र' आहे."
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

    # Save to Revised Document File & Mirror to Brain Artifact
    target_output.parent.mkdir(parents=True, exist_ok=True)
    doc.save(str(target_output))

    try:
        shutil.copy2(target_output, ARTIFACT_FILE)
    except Exception as e:
        print(f"Warning: Could not mirror to artifact dir: {e}")

    print(f"Successfully generated Reader-First Edition manuscript:")
    print(f"  Docs: {target_output}")
    print(f"  Artifact: {ARTIFACT_FILE}")
    return target_output


if __name__ == "__main__":
    build_reader_first_document()
