"""
================================================================================
Module: scripts.ten_new_sutras_canonical_data
Author: Hiranyam AI Labs (https://hiranyamai.com/)
Project: SK Sutras - by Shri Shripad Kulkarni
Description: Canonical scholarly data for the 10 NEW Approved Udyog Sutras
             (Sutras 11 to 20 / Fresh Execution Set 2).
             Integrates:
             - Narada Bhakti Sutras & Shandilya Bhakti Sutras
             - Sant Tukaram Maharaj's Teachings & Discourse (DOC-04):
               (Kondopant Lokre Copper Coin Parable, Five Foundations of
               Prosperity, Uttam Vyavahar, Daan/Bhog/Asakti, Daivacha Putla)
             - Authentic Classical IKS References (Gita, Upanishads, Niti)
             - Padaccheda, Anvaya, Word-by-word breakdown, Trilingual translation,
               and natural Marathi explanation.
================================================================================
"""

from typing import Any, Dict, List

# ==============================================================================
# THE 10 NEW UDYOG SUTRAS CANON (SUTRAS 11 TO 20)
# ==============================================================================
TEN_NEW_UDYOG_SUTRAS_CANON: List[Dict[str, Any]] = [
    # --------------------------------------------------------------------------
    # SUTRA 1 (OVERALL 11)
    # --------------------------------------------------------------------------
    {
        "sutra_no": 1,
        "overall_sutra_no": 11,
        "title": "उत्तम व्यवहार आणि विरक्त विनियोग (Ethical Commerce & Detached Stewardship)",
        "sanskrit": "॥ उत्तमव्यवहारेण धनसञ्चयः उदासविचारेण विनियोगः ॥",
        "matching_pair": {
            "narada": {
                "sutra": "भवतु निश्चयदाढ्र्यादूर्ध्वं शास्त्ररक्षणम् ॥ १२ ॥",
                "meaning_en": "Even after spiritual conviction is firmly established, scriptural and ethical discipline must be scrupulously safeguarded (NBS 12).",
                "meaning_mr": "निश्चय पक्का झाल्यावरही शास्त्राने सांगितलेले नैतिक नियम व मर्यादा यांचे काटेकोर पालन केलेच पाहिजे (नारद सूत्र १२)."
            },
            "shandilya": {
                "sutra": "सदाचारस्तदङ्गत्वेन विहितः ॥ ७२ ॥",
                "meaning_en": "Righteous moral conduct is ordained as an indispensable limb of truth and realization (SBS 72).",
                "meaning_mr": "सदाचार आणि शुद्ध आचरण हे सत्यप्राप्तीचे अविभाज्य अंग म्हणून शास्त्रात विहित केलेले आहे (शांडिल्य सूत्र ७२)."
            }
        },
        "bharatiya_jnana_basis": {
            "source": "Sant Tukaram Maharaj Abhanga (DOC-04 Section 2.1) & Brihaspati Niti Shastra",
            "verse": "जोडोनिया धन उत्तम व्यवहारे । उदास विचारे वेच करी ॥\nउत्तम ची गति तो एक पावेल । उत्तम भोगील दिव्य भोग ॥",
            "meaning_en": "Acquire wealth through righteous and transparent commerce; spend and distribute it with an elevated, detached mind.",
            "meaning_mr": "धन मिळवताना ते उत्तम, प्रामाणिक व्यवहाराने मिळवावे आणि त्याचा विनियोग करताना कोणताही स्वार्थ न बाळगता उदास (विरक्त) विचाराने समाजासाठी करावा."
        },
        "padaccheda": "उत्तम-व्यवहारेण । धन-सञ्चयः । उदास-विचारेण । विनियोगः ॥",
        "anvaya": "उत्तमव्यवहारेण धनसञ्चयः (कर्तव्यः), उदासविचारेण (च तस्य) विनियोगः (कर्तव्यः) ।",
        "word_by_word": "उत्तमव्यवहारेण (uttama-vyavahāreṇa) = न्याय्य, प्रामाणिक व पारदर्शक मार्गाने (through honest, righteous commerce); धनसञ्चयः (dhana-sañcayaḥ) = संपत्तीची निर्मिती व भांडवल संचय (accumulation of enterprise wealth); उदासविचारेण (udāsa-vicāreṇa) = आसक्तीरहित, उदात्त व लोककल्याणकारी विचाराने (with elevated, detached wisdom); विनियोगः (viniyogaḥ) = संपत्तीचा समाजोपयोगी वापर व वितरण (purposeful deployment and allocation).",
        "translation_en": "Enterprise wealth must be accumulated solely through righteous and transparent commerce, and its capital must be allocated with an elevated, detached wisdom for societal welfare.",
        "marathi_explanation": "उद्योगाचा पाया हा केवळ नफ्यावर नसून 'उत्तम व्यवहारावर' आधारलेला असला पाहिजे. संत तुकाराम महाराजांनी अत्यंत स्पष्ट शब्दात सांगितले आहे की, धन मिळवताना ते नीतीने, सचोटीने आणि ग्राहकाशी प्रामाणिक राहूनच मिळवले पाहिजे. जेव्हा असा प्रामाणिक नफा मिळतो, तेव्हा उद्योजकाने त्या संपत्तीचा मालक न होता तिचा विश्वस्त बनावे आणि 'उदास विचारे' म्हणजेच कोणताही वैयक्तिक अहंकार किंवा लोभ न बाळगता तिचा विनियोग कर्मचारी, समाज आणि व्यवसायाच्या निरंतर वाढीसाठी करावा. अनैतिक मार्गाने मिळवलेला पैसा तात्पुरता झगमगाट दाखवतो, पण अखेर संस्थेचा विनाश ओढवतो.",
        "business_and_psychology": "व्यवसाय व्यवस्थापनात पारदर्शकता (Corporate Governance) आणि नैतिक मूल्ये ही ब्रँडची सर्वात मोठी शक्ती असते. उद्योजकाने नफ्यामागे धावताना मूल्यांचा बळी देऊ नये. वित्तीय शिस्त आणि लोभावर नियंत्रण ठेवल्याने कंपनीची पत (Creditworthiness) दीर्घकाळ टिकून राहते."
    },
    # --------------------------------------------------------------------------
    # SUTRA 2 (OVERALL 12)
    # --------------------------------------------------------------------------
    {
        "sutra_no": 2,
        "overall_sutra_no": 12,
        "title": "विश्वास हेच मूळ भांडवल आणि लोभाचा विनाश (Trust as Core Capital & The Fall of Greed)",
        "sanskrit": "॥ विश्वासभङ्गो मूलघातको लोभात्प्रणश्यति सर्वसम्पद् ॥",
        "matching_pair": {
            "narada": {
                "sutra": "दुःसङ्गः सर्वथैव त्याज्यः ॥ ४३ ॥",
                "meaning_en": "Evil association, toxic greed, and corrupting influences must be completely abandoned by all means (NBS 43).",
                "meaning_mr": "दुर्जनांची संगत, अप्रामाणिक विचार आणि भ्रष्ट मार्ग यांचा सर्व प्रकारे त्याग केला पाहिजे (नारद सूत्र ४३)."
            },
            "shandilya": {
                "sutra": "द्रोहस्यापुण्यजनकत्वात् ॥ ७५ ॥",
                "meaning_en": "Because betrayal and breach of trust generate catastrophic moral and practical ruin (SBS 75).",
                "meaning_mr": "विश्वासघात आणि द्रोह हे पापाचे आणि समूळ विनाशाचे मूळ कारण ठरतात (शांडिल्य सूत्र ७५)."
            }
        },
        "bharatiya_jnana_basis": {
            "source": "Sant Tukaram Maharaj: Parable of the Copper Coin (DOC-04 Section 1.1) & Chanakya Niti",
            "verse": "विश्वासघातिनां लोके न प्रायश्चित्तं विद्यते ।\nतांब्याच्या नाण्याचा दृष्टांत: लोभापायी खोटे बोलल्याने अक्षय देणगी नष्ट झाली.",
            "meaning_en": "In this world, there is no expiation for breaching trust. The Copper Coin parable proves that greed permanently stops the flow of divine abundance.",
            "meaning_mr": "जगात विश्वासघाताला कोणतेही प्रायश्चित्त नाही. तुकोबारायांच्या तांब्याच्या नाण्याच्या दृष्टांतात कोंडोपंत लोकरेने लोभ धरून खोटे सांगितल्याने सोन्याची अक्षय कृपा कायमची नष्ट झाली."
        },
        "padaccheda": "विश्वास-भङ्गः । मूल-घातकः । लोभात् । प्रणश्यति । सर्व-सम्पत् ॥",
        "anvaya": "विश्वासभङ्गः (उद्यमस्य) मूलघातकः (भवति), लोभात् सर्वसम्पत् प्रणश्यति ।",
        "word_by_word": "विश्वासभङ्गः (viśvāsa-bhaṅgaḥ) = ग्राहकांचा व भागधारकांचा विश्वासघात (Breach of fiduciary trust); मूलघातकः (mūla-ghātakaḥ) = मुळावरच घाव घालणारा, पाया उद्ध्वस्त करणारा (Fatally destructive to the very root); लोभात् (lobhāt) = तात्कालिक स्वार्थापोटी आलेल्या लोभामुळे (Out of shortsighted greed); प्रणश्यति (praṇaśyati) = समूळ नष्ट होते (Utterly perishes); सर्वसम्पत् (sarva-sampad) = सर्व प्रतिष्ठा, पत व समृद्धी (All accumulated wealth and goodwill).",
        "translation_en": "Breach of fiduciary trust strikes fatally at the very root of enterprise; through shortsighted greed, all accumulated prosperity and goodwill perish.",
        "marathi_explanation": "व्यवसायाचे खरे भांडवल हे बँकेतील पैशात नसून ग्राहकांनी आणि समाजाने ठेवलेल्या विश्वासावर आधारलेले असते. संत तुकाराम महाराजांच्या तांब्याच्या नाण्याच्या दृष्टांतात कोंडोपंत लोकरेने लोभापायी खोटे बोलून विश्वासघात केला आणि त्यामुळे त्याला मिळालेली अक्षय सोन्याची देणगी कायमची नष्ट झाली. उद्योजकाने हे सदैव लक्षात ठेवले पाहिजे की, थोड्याशा जादा नफ्यासाठी किंवा तात्पुरत्या लाभासाठी ग्राहकांची किंवा भागीदारांची फसवणूक करणे म्हणजे सोन्याचे अंडे देणाऱ्या कोंबडीला मारण्यासारखे आहे. एकदा का विश्वास उडाला की कोट्यवधींचे साम्राज्यही पत्त्यांच्या बंगल्यासारखे कोसळते.",
        "business_and_psychology": "ग्राहक निष्ठा (Customer Trust) निर्माण करायला दशके लागतात, पण ती गमावायला एक खोटी कृती पुरेशी असते. लोभ हा उद्योजकाचा सर्वात मोठा मानसिक शत्रू आहे; तो बुद्धीवर असा पडदा टाकतो की माणसाला दीर्घकालीन नुकसानाची जाणीव राहत नाही."
    },
    # --------------------------------------------------------------------------
    # SUTRA 3 (OVERALL 13)
    # --------------------------------------------------------------------------
    {
        "sutra_no": 3,
        "overall_sutra_no": 13,
        "title": "समृद्धीचे पञ्चाङ्ग आणि पुरुषार्थाची सिद्धी (Five Foundations of Prosperity)",
        "sanskrit": "॥ पञ्चाङ्गसिद्धिरुद्यमे पुरुषार्थः कृपासंयोगेन फलति ॥",
        "matching_pair": {
            "narada": {
                "sutra": "तस्याः साधनं मुख्यकृपा महद्कृपा लेशो वा ॥ २८ ॥",
                "meaning_en": "The primary means of attainment is divine grace or even a tiny drop of the grace of noble mentors (NBS 28).",
                "meaning_mr": "सिद्धी प्राप्त होण्याचे मुख्य साधन म्हणजे ईश्वरी कृपा आणि सत्पुरुषांचा अल्पसा आशीर्वाद होय (नारद सूत्र २८)."
            },
            "shandilya": {
                "sutra": "कर्मविपाकादपरमपि निमित्तम् ॥ ४४ ॥",
                "meaning_en": "Besides the ripening of human action, unforeseen external factors and circumstances act as auxiliary causes (SBS 44).",
                "meaning_mr": "केवळ माणसाच्या कर्माच्या परिपाकाव्यतिरिक्त अनुकूल परिस्थिती आणि अदृष्ट घटकही कारण ठरतात (शांडिल्य सूत्र ४४)."
            }
        },
        "bharatiya_jnana_basis": {
            "source": "Sant Tukaram Maharaj: Five Foundations of Prosperity (DOC-04 Section 1.2) & Bhagavad Gita 18.14",
            "verse": "१. ईश्वरकृपा २. आई-वडिलांचा आशीर्वाद ३. गुरूंचा आशीर्वाद ४. अनुकूल प्रारब्ध ५. पराकाष्ठेचा पुरुषार्थ ।\nपञ्चैतानि महाबाहो कारणानि निबोध मे । सिद्धये सर्वकर्मणाम् ॥",
            "meaning_en": "Deglurkar discourse details 5 factors of Arth-Purushartha. Human exertion succeeds when harmonized with grace, mentors, and opportune timing.",
            "meaning_mr": "डिग्रजकर निरूपणात स्पष्ट केलेले समृद्धीचे पाच आधार: ईश्वरकृपा, माता-पिता आशीर्वाद, गुरूंचा आशीर्वाद, अनुकूल प्रारब्ध आणि स्वतःचा पुरुषार्थ."
        },
        "padaccheda": "पञ्चाङ्ग-सिद्धिः । उद्यमे । पुरुषार्थः । कृपा-संयोगेन । फलति ॥",
        "anvaya": "उद्यमे पञ्चाङ्गसिद्धिः (भवति), कृपासंयोगेन पुरुषार्थः फलति ।",
        "word_by_word": "पञ्चाङ्गसिद्धिः (pañcāṅga-siddhiḥ) = पाच घटकांच्या संतुलनावर आधारलेले यश (Success rooted in five foundational pillars); उद्यमे (udyame) = व्यवसायात (In enterprise); पुरुषार्थः (puruṣārthaḥ) = अथक वैयक्तिक प्रयत्न व कार्यक्षमता (Disciplined human effort); कृपासंयोगेन (kṛpā-saṁyogena) = ईश्वरी कृपा, पालक-गुरुकृपा व अनुकूल वेळेच्या संयोगाने (Through alignment with grace, mentorship, and timing); फलति (phalati) = फळाला येतो, यशस्वी होतो (Bears sovereign fruit).",
        "translation_en": "Enterprise success is fivefold in its foundational pillars; disciplined human exertion bears lasting fruit only when harmonized with grace, mentorship, and opportune timing.",
        "marathi_explanation": "उद्योगातील यशाचे श्रेय केवळ एका घटकाला देता येत नाही. संत तुकाराम महाराजांच्या निरूपणात स्पष्ट केले आहे की, संपत्तीच्या प्राप्तीमागे पाच प्रमुख शक्ती कार्यरत असतात: ईश्वराची कृपा, आई-वडिलांचे संस्कार व आशीर्वाद, मार्गदर्शक गुरूंचे मार्गदर्शन, अनुकूल काळ (प्रारब्ध), आणि स्वतःचा पराकाष्ठेचा प्रयत्न (पुरुषार्थ). उद्योजकाने केवळ नशिबावर हवाला ठेवून आळशी होऊ नये, आणि यश मिळाल्यावर 'हे सर्व माझ्या एकट्यामुळेच घडले' असा अहंकारही बाळगू नये. जेव्हा कठोर परिश्रमाला योग्य मार्गदर्शन आणि काळानुकूल संधीची जोड मिळते, तेव्हाच अफाट यश प्राप्त होते.",
        "business_and_psychology": "यशस्वी उद्योजकात 'विनम्रता' (Humility) असावी लागते. नशिबाला किंवा बाजाराच्या परिस्थितीला दोष देत बसणे हा प्रमाद आहे, आणि स्वतःलाच सर्वज्ञ समजणे हा अहंकार आहे. स्वतःची मेहनत १००% करणे आणि बाह्य घटकांचा आदर करणे हेच संतुलन आहे."
    },
    # --------------------------------------------------------------------------
    # SUTRA 4 (OVERALL 14)
    # --------------------------------------------------------------------------
    {
        "sutra_no": 4,
        "overall_sutra_no": 14,
        "title": "दानातून आणि भोगातून संपत्तीचे सार्थक (Tri-fold Wealth Allocation & Non-Attachment)",
        "sanskrit": "॥ दानेन भोगेन च धनसार्थक्यं निरासक्तिस्तु रक्षकम् ॥",
        "matching_pair": {
            "narada": {
                "sutra": "यो विविक्तस्थानं सेवते यो लोकबन्धमुन्मूलयति निस्त्रैगुण्यो भवति योगक्षेमं त्यजति ॥ ४८ ॥",
                "meaning_en": "He who uproots worldly clinging, transcends the gunas, and renounces anxious clutching over acquisition and preservation (NBS 48).",
                "meaning_mr": "जो सांसारिक मोहाचे मूळ उपटून टाकतो आणि प्राप्ती व रक्षणाच्या अस्वस्थ चिंतेचा त्याग करतो (नारद सूत्र ४८)."
            },
            "shandilya": {
                "sutra": "भोगत्यागाभ्यां च ॥ ६३ ॥",
                "meaning_en": "And through the harmonious integration of legitimate enjoyment and disciplined renunciation (SBS 63).",
                "meaning_mr": "योग्य उपभोग आणि आवश्यक त्याग या दोघांच्या संतुलनाने जीवन कृतार्थ होते (शांडिल्य सूत्र ६३)."
            }
        },
        "bharatiya_jnana_basis": {
            "source": "Sant Tukaram Maharaj on Daan, Bhog, and Asakti (DOC-04 Section 1.3) & Bhartrihari Niti Shataka 43",
            "verse": "दानं भोगो नाशस्तिस्रो गतयो भवन्ति वित्तस्य ।\nयो न ददाति न भुङ्क्ते तस्य तृतीया गतिर्भवति ॥",
            "meaning_en": "Giving, legitimate enjoyment, and total loss are the three destinies of wealth. He who neither gives nor enjoys meets destruction.",
            "meaning_mr": "संपत्तीचे तीनच मार्ग आहेत: दान, भोग आणि नाश. जो दान करत नाही आणि योग्य उपभोगही घेत नाही, त्याच्या धनाचा तिसरा मार्ग म्हणजे सर्वनाश निश्चित असतो."
        },
        "padaccheda": "दानेन । भोगेन । च । धन-सार्थक्यम् । निरासक्तिः । तु । रक्षकम् ॥",
        "anvaya": "दानेन भोगेन च धनसार्थक्यं (भवति), निरासक्तिः तु (तस्य) रक्षकम् (भवति) ।",
        "word_by_word": "दानेन (dānena) = समाजऋण फेडणाऱ्या दातृत्वाने व परोपकाराने (Through charitable giving and CSR); भोगेन (bhogena) = स्वतःचे व सहकाऱ्यांचे जीवनमान समृद्ध करण्याने (Through legitimate enjoyment and fair living); च (ca) = आणि (And); धनसार्थक्यम् (dhana-sārthakyam) = संपत्तीचे खरे सार्थक (True fulfillment of wealth); निरासक्तिः (nirāsaktiḥ) = मोहाचा व लोभाचा त्याग (Inner detachment from grasping); तु (tu) = खरोखर (Indeed); रक्षकम् (rakṣakam) = संपत्तीचे व नीतीचे संरक्षक (The ultimate shield and protector).",
        "translation_en": "Wealth attains its true significance through charitable giving and legitimate enjoyment, while detachment from possessive grasping serves as its perpetual shield.",
        "marathi_explanation": "संपत्ती मिळवणे हा गुन्हा नाही, परंतु ती केवळ साठवून ठेवणे हा विनाशकारी रोग आहे. नीतिकार भर्तृहरी आणि संत तुकाराम महाराज सांगतात की संपत्तीचे सार्थक दोनच गोष्टींत आहे: 'दान' म्हणजेच समाजाला परत देणे, आणि 'भोग' म्हणजेच स्वतःच्या व सहकाऱ्यांच्या रास्त गरजा पूर्ण करणे. या दोघांच्या पलीकडे जो संपत्तीला घट्ट चिकटून राहतो, त्याचा लोभ त्याच्या विनाशाला कारणीभूत ठरतो. उद्योजकाचे मन जर 'निरासक्त' असेल, तर व्यवसाय तोट्यात गेला तरी तो खचत नाही आणि प्रचंड नफा झाला तरी तो उन्मत्त होत नाही. ही अलिप्तता उद्योजकाला निर्भय बनवते.",
        "business_and_psychology": "अतिरिक्त संचय (Hoarding) हा आर्थिक चक्राला अडथळा आणतो. नफ्यातील योग्य भाग कर्मचाऱ्यांच्या कल्याणासाठी आणि सामाजिक कार्यासाठी (CSR) खर्च केल्यास कंपनीची प्रतिष्ठा वाढते. उद्योजकाने संपत्तीचा मालक न होता विश्वस्त (Trustee) व्हावे."
    },
    # --------------------------------------------------------------------------
    # SUTRA 5 (OVERALL 15)
    # --------------------------------------------------------------------------
    {
        "sutra_no": 5,
        "overall_sutra_no": 15,
        "title": "दैवाचा पुतळा – आचरणातून तत्त्वांचे प्रकटीकरण (Daivacha Putla - Living Values in Leadership)",
        "sanskrit": "॥ आचारेणैव धर्मस्य प्रत्यक्षत्वं नेतेति मूर्तिमान् ॥",
        "matching_pair": {
            "narada": {
                "sutra": "तस्मिंस्तज्जने भेदाभावात् ॥ ४१ ॥",
                "meaning_en": "Because between the supreme divine principle and the dedicated devotee, no distinction exists (NBS 41).",
                "meaning_mr": "ईश्वर आणि त्याची प्रत्यक्ष सेवा करणारा भक्त यांच्यात कोणताही भेद नसतो (नारद सूत्र ४१)."
            },
            "shandilya": {
                "sutra": "आचारदर्शनात् ॥ ८५ ॥",
                "meaning_en": "Because transcendent ethical truth becomes visible through tangible personal conduct (SBS 85).",
                "meaning_mr": "केवळ उपदेशाने नव्हे, तर प्रत्यक्ष आचरणाच्या दर्शनातूनच सत्याचे दर्शन घडते (शांडिल्य सूत्र ८५)."
            }
        },
        "bharatiya_jnana_basis": {
            "source": "Sant Tukaram Maharaj: Daivacha Putla (DOC-04 Section 1.4) & Bhagavad Gita 3.21",
            "verse": "यद्यदाचरति श्रेष्ठस्तत्तदेवेतरो जनः । स यत्प्रमाणं कुरुते लोकस्तदनुवर्तते ॥\nदैवाचा पुतळा: अदृश्य मूल्यांना नेत्याच्या वर्तनातून दृश्य रूप मिळते.",
            "meaning_en": "Whatever the leader practices, that alone people follow. The ethical leader is a living statue (Daivacha Putla) of organizational values.",
            "meaning_mr": "श्रेष्ठ लोक जसे आचरण करतात, इतर लोक तसेच अनुकरण करतात. संत तुकाराम महाराजांची 'दैवाचा पुतळा' संकल्पना सांगते की नेत्याचे चारित्र्य हेच मूल्यांचे चालते-बोलते रूप असते."
        },
        "padaccheda": "आचारेण । एव । धर्मस्य । प्रत्यक्षत्वम् । नेता । इति । मूर्तिमान् ॥",
        "anvaya": "आचारेण एव धर्मस्य प्रत्यक्षत्वं (भवति), नेता इति मूर्तिमान् (भवति) ।",
        "word_by_word": "आचारेण (ācāreṇa) = प्रत्यक्ष कृतीतून व वर्तनातून (Through personal conduct); एव (eva) = केवळ (Alone); धर्मस्य (dharmasya) = मूल्यांचे, व्यावसायिक नीतीचे (Of ethical values); प्रत्यक्षत्वम् (pratyakṣatvam) = जिवंत दृश्य रूप (Tangible visibility and proof); नेता (netā) = उद्योजक, संस्थेचा प्रमुख (The leader); इति (iti) = अशा प्रकारे (Thus); मूर्तिमान् (mūrtimān) = मूर्तिमंत प्रतीक, दैवाचा पुतळा (The living embodiment).",
        "translation_en": "Through exemplary personal conduct alone does ethical truth become visible; the true leader is a living incarnation of organizational values.",
        "marathi_explanation": "नीतिमत्तेची आणि प्रामाणिकपणाची भाषणे देऊन कंपन्यांमध्ये संस्कृती निर्माण होत नसते. संत तुकाराम महाराजांनी 'दैवाचा पुतळा' ही अप्रतिम संकल्पना मांडली आहे. अदृश्य असलेले दैवी तत्त्व किंवा कंपनीचे मूल्य हे नेत्याच्या प्रत्यक्ष वर्तनातून दिसले पाहिजे. जेव्हा एखादा संस्थापक स्वतः पारदर्शक राहतो, वेळेचे पालन करतो, कर्मचाऱ्यांशी न्यायाने वागतो आणि संकटात पुढे उभा राहतो, तेव्हा तो त्या मूल्यांचा 'मूर्तिमंत पुतळा' बनतो. अशा नेत्याचे अनुकरण संपूर्ण कंपनी आपोआप करते.",
        "business_and_psychology": "संस्थेची संस्कृती (Company Culture) ही नियमावलीतून नव्हे तर संस्थापकाच्या वर्तनातून झिरपते (Tone at the top). नेत्याचे शब्द आणि कृती यांत तफावत असल्यास कर्मचाऱ्यांचा विश्वास उडतो; कृतीतून विश्वास जिंकणे हीच खरी लीडरशिप आहे."
    },
    # --------------------------------------------------------------------------
    # SUTRA 6 (OVERALL 16)
    # --------------------------------------------------------------------------
    {
        "sutra_no": 6,
        "overall_sutra_no": 16,
        "title": "सत्य हेच अक्षय भांडवल (Truth as Inexhaustible Working Capital)",
        "sanskrit": "॥ सत्यमेव शाश्वतं भाण्डवलं कपटेन न सिध्यति ॥",
        "matching_pair": {
            "narada": {
                "sutra": "तत्तु विषयत्यागात् सङ्गत्यागाच्च ॥ ३५ ॥",
                "meaning_en": "Devotion and clarity are attained through abandoning deceptive sensuality and false associations (NBS 35).",
                "meaning_mr": "खोटेपणाचा आणि कपटी संगतीचा त्याग केल्यानेच चित्त शुद्ध व स्थिर होते (नारद सूत्र ३५)."
            },
            "shandilya": {
                "sutra": "सत्यवचने नियमः ॥ ७८ ॥",
                "meaning_en": "Truthfulness in speech and conduct is an unalterable, non-negotiable vow (SBS 78).",
                "meaning_mr": "सत्यभाषण आणि सत्यव्यवहार हा जीवनाचा अनिवार्य व अटळ नियम आहे (शांडिल्य सूत्र ७८)."
            }
        },
        "bharatiya_jnana_basis": {
            "source": "Sant Tukaram Maharaj Abhanga (DOC-04 Section 2.2) & Mahabharata Shanti Parva",
            "verse": "सत्य तेचि भांडवल आम्हा । आणिक नाही प्रेमा ॥\nसत्य बोलावे सत्य चालावे । सत्यचि मनी धरावे ॥",
            "meaning_en": "Truth alone is our working capital and currency; we know no other love. Enterprise never endures through deceit.",
            "meaning_mr": "सत्य हेच आमचे मूळ भांडवल आहे; सत्यानेच बोलावे, सत्यानेच चालावे आणि सत्यालाच मनी धरावे. कपटाने कधीही चिरंतन यश मिळत नाही."
        },
        "padaccheda": "सत्यम् । एव । शाश्वतम् । भाण्डवलम् । कपटेन । न । सिध्यति ॥",
        "anvaya": "सत्यम् एव शाश्वतं भाण्डवलं (भवति), कपटेन (उद्योगः) न सिध्यति ।",
        "word_by_word": "सत्यम् (satyam) = सत्य, पारदर्शकता, वस्तुस्थिती (Truth and factual transparency); एव (eva) = हेच (Alone); शाश्वतम् (śāśvatam) = कधीही न संपणारे, चिरंतन (Eternal and permanent); भाण्डवलम् (bhāṇḍavalam) = मूळ भांडवल, पत (Working capital and core asset); कपटेन (kapaṭena) = खोटेपणाने व फसवणुकीने (Through deceit or fraud); न (na) = कधीही नाही (Not); सिध्यति (sidhyati) = सिद्ध होते, टिकते (Endures or succeeds).",
        "translation_en": "Truth alone is the enduring and inexhaustible working capital; enterprise never achieves lasting success through deceit or fraudulent concealment.",
        "marathi_explanation": "व्यवसायात आर्थिक भांडवलापेक्षा 'सत्याचे भांडवल' अधिक मौल्यवान असते. संत तुकाराम महाराज गर्वाने सांगतात, 'सत्य तेचि भांडवल आम्हा, आणिक नाही प्रेमा.' आजच्या कॉर्पोरेट जगतात कंपन्या बॅलन्स शीटमध्ये फेरफार करून किंवा खोटी आकडेवारी दाखवून तात्पुरते मोठेपण मिळवू पाहतात; परंतु असा कपटाचा डोलारा कधीही टिकत नाही (उदा. सत्यम किंवा एनरॉन). जेव्हा उत्पादन, गुणवत्ता, वित्तीय व्यवहार आणि कर भरणा यात संपूर्ण सत्यता असते, तेव्हा तो व्यवसाय जगातील सर्वात बलाढ्य ब्रँड बनतो.",
        "business_and_psychology": "सत्य बोलण्याचे मानसिक धैर्य (Integrity). लपवाछपवी केल्याने सतत मानसिक ताण राहतो. पारदर्शक आर्थिक हिशोब आणि प्रामाणिक उत्पादन माहिती हीच गुंतवणूकदारांची आणि ग्राहकांची खात्री असते."
    },
    # --------------------------------------------------------------------------
    # SUTRA 7 (OVERALL 17)
    # --------------------------------------------------------------------------
    {
        "sutra_no": 7,
        "overall_sutra_no": 17,
        "title": "विस्ताराच्या शिखरावर नम्रतेचे संरक्षण (Humility at the Zenith of Success)",
        "sanskrit": "॥ वृद्धौ विनयो रक्षा अहङ्कारो विनाशहेतुः ॥",
        "matching_pair": {
            "narada": {
                "sutra": "ईश्वराभिमानिनो द्वेष्याः दैन्यप्रियाश्च ॥ २७ ॥",
                "meaning_en": "The supreme principle rejects those blinded by arrogant pride, and cherishes those rooted in genuine humility (NBS 27).",
                "meaning_mr": "अहंकाराने माजलेले लोक ईश्वराला अप्रिय असतात, आणि नम्रतेने वागणारे त्याला अत्यंत प्रिय असतात (नारद सूत्र २७)."
            },
            "shandilya": {
                "sutra": "अभिमानत्यागात् संसिद्धिः ॥ ९० ॥",
                "meaning_en": "Supreme accomplishment is attained through the complete eradication of egoistic pride (SBS 90).",
                "meaning_mr": "अहंकाराचा त्याग केल्यानेच माणसाला अंतिम सिद्धी आणि प्रतिष्ठा प्राप्त होते (शांडिल्य सूत्र ९०)."
            }
        },
        "bharatiya_jnana_basis": {
            "source": "Sant Tukaram Maharaj Abhanga (DOC-04 Section 2.3) & Hitopadesha",
            "verse": "लहानपण देगा देवा । मुंगी साखरेचा रवा ॥\nऐरावत रत्न थोर । तया अंकुशाचा मार ॥",
            "meaning_en": "Bestow humility upon me, Lord! The tiny ant enjoys sugar, while the royal elephant Airavata receives blows of the iron hook.",
            "meaning_mr": "हे देवा, मला लहानपण (नम्रता) दे; मुंगी होऊन साखरेचा रवा खाता येतो. इंद्राचा ऐरावत हत्ती मोठा असला तरी त्याला अंकुशाचा मार सहन करावा लागतो."
        },
        "padaccheda": "वृद्धौ । विनयः । रक्षा । अहङ्कारः । विनाश-हेतुः ॥",
        "anvaya": "(उद्यमस्य) वृद्धौ विनयः रक्षा (भवति), अहङ्कारः विनाशहेतुः (भवति) ।",
        "word_by_word": "वृद्धौ (vṛddhau) = कंपनीच्या व यशाच्या शिखरावर, विस्ताराच्या वेळी (In the zenith of growth and expansion); विनयः (vinayaḥ) = नम्रता, शिकण्याची व ऐकण्याची वृत्ती (Humility and customer attentiveness); रक्षा (rakṣā) = सर्वोत्तम संरक्षक ढाल (The ultimate protective armor); अहङ्कारः (ahaṅkāraḥ) = गर्विष्ठपणा, कॉर्पोरेट घमेंड (Arrogant executive hubris); विनाशहेतुः (vināśa-hetuḥ) = पतनाचे व विनाशाचे मुख्य कारण (The primary cause of collapse).",
        "translation_en": "In the zenith of corporate growth and expansion, humility is the ultimate defense; uncontrolled executive hubris is the primary cause of sudden collapse.",
        "marathi_explanation": "कंपनी जशी जशी मोठी होते, तसा तिच्यामध्ये अहंकार आणि आत्मसंतुष्टता शिरण्याचा धोका वाढतो. संत तुकारामांनी मुंगी आणि ऐरावताचा दाखला दिला आहे. लहान मुंगी जमिनीवर राहून साखरेचा रवा आनंदाने खाते; पण इंद्राचा विशाल ऐरावत हत्ती असला तरी त्याला अंकुशाचे फटके खावे लागतात. उद्योजकाने शिखरावर पोहोचल्यावरही ग्राहकांपुढे आणि नवीन तंत्रज्ञानापुढे नम्र राहिले पाहिजे. 'आम्हाला कोणी हरवू शकत नाही' हा अहंकार नोकिया किंवा कोडॅकसारख्या महाकाय कंपन्यांनाही संपवून टाकतो. नम्रता हीच निरंतर यशाची ढाल आहे.",
        "business_and_psychology": "अहंकार माणसाचे कान बंद करतो (Hubris-induced blindness). शिखरावर असतानाही लहान स्टार्टअप्सकडून शिकण्याची तयारी ठेवणे आणि ग्राहकांचा आवाज नम्रपणे ऐकणे हीच टिकून राहण्याची गुरुकिल्ली आहे."
    },
    # --------------------------------------------------------------------------
    # SUTRA 8 (OVERALL 18)
    # --------------------------------------------------------------------------
    {
        "sutra_no": 8,
        "overall_sutra_no": 18,
        "title": "वंचितांचा उद्धार हेच उद्योगाचे सर्वोच्च ध्येय (Inclusive Upliftment of the Vulnerable)",
        "sanskrit": "॥ दीनोद्धारपरमोद्योगः समाजकल्याणसाधनम् ॥",
        "matching_pair": {
            "narada": {
                "sutra": "अनिर्देश्यं प्रेमस्वरूपम् ॥ ५१ ॥",
                "meaning_en": "Authentic dedication and love cannot be narrowly defined; it manifests as boundless compassion (NBS 51).",
                "meaning_mr": "खऱ्या प्रेमाचे व समर्पणाचे स्वरूप शब्दातीत असते; ते सर्वसमावेशक करुणेच्या रूपात प्रगट होते (नारद सूत्र ५१)."
            },
            "shandilya": {
                "sutra": "दीनानुकम्पा परा भक्तिः ॥ ९८ ॥",
                "meaning_en": "Compassion towards the destitute, oppressed, and vulnerable constitutes the highest devotion (SBS 98).",
                "meaning_mr": "दीन, दुबळे आणि पीडित यांच्याविषयी वाटणारी खरी करुणा हीच सर्वोच्च भक्ती ठरते (शांडिल्य सूत्र ९८)."
            }
        },
        "bharatiya_jnana_basis": {
            "source": "Sant Tukaram Maharaj Abhanga (DOC-04 Section 2.4) & Lokmanya Tilak's Gita Rahasya",
            "verse": "जे का रंजले गांजले । त्यांसी म्हणे जो आपुले ॥\nतोचि साधु ओळखावा । देव तेथेचि जाणावा ॥",
            "meaning_en": "He who embraces the suffering, oppressed, and neglected as his own family—recognize him alone as a true saint; God resides verily in him.",
            "meaning_mr": "जे लोक रंजलेले, गांजलेले व उपेक्षित आहेत त्यांना जो आपले मानतो, तोच खरा साधू समजावा आणि तिथेच देवाचे दर्शन होते. टिळकांच्या गीतारहस्यानुसार हाच लोकसंग्रह आहे."
        },
        "padaccheda": "दीन-उद्धार-परमः । उद्योगः । समाज-कल्याण-साधनम् ॥",
        "anvaya": "दीनोद्धारपरमः उद्योगः समाजकल्याणसाधनम् (भवति) ।",
        "word_by_word": "दीनोद्धारपरमः (dīnoddhāra-paramaḥ) = वंचित, दुर्बल व सर्वसामान्य घटकांच्या उन्नतीला समर्पित (Dedicated to uplifting the vulnerable and underserved); उद्योगः (udyogaḥ) = व्यवसाय, संस्था (Enterprise); समाजकल्याणसाधनम् (samāja-kalyāṇa-sādhanam) = लोककल्याणाचे आणि राष्ट्रउभारणीचे पवित्र साधन (The supreme instrument of social flourishing).",
        "translation_en": "The enterprise that holds the upliftment and empowerment of the vulnerable as its highest purpose becomes the supreme instrument of societal flourishing.",
        "marathi_explanation": "व्यवसायाचे ध्येय केवळ उच्चभ्रू वर्गाची सेवा करणे हे असू शकत नाही. संत तुकाराम महाराजांचा हा अजरामर अभंग आहे: 'जे का रंजले गांजले, त्यांसी म्हणे जो आपुले, तोचि साधु ओळखावा, देव तेथेचि जाणावा.' जो उद्योग समाजातील तळागाळातील शेतकऱ्यांचे, कष्टकऱ्यांचे आणि उपेक्षित घटकांचे जीवन सुलभ करण्यासाठी उत्पादन तयार करतो (उदा. अमूल, मायक्रोफायनान्स किंवा परवडणारी आरोग्यसेवा), त्या उद्योगात साक्षात ईश्वर वास करतो. सामाजिक उत्तरदायित्व (CSR) हा केवळ कायदेशीर सोपस्कार नसून तो उद्योगाचा गाभा असायला हवा.",
        "business_and_psychology": "तळागाळातील समस्या सोडवणे (Bottom of the Pyramid Innovation). गरिबांच्या क्रयशक्तीचा आणि गरजांचा आदर करून किफायतशीर उत्पादने बनवणे हेच सर्वात मोठे समाजकल्याण आणि व्यवसाय-विस्तार आहे."
    },
    # --------------------------------------------------------------------------
    # SUTRA 9 (OVERALL 19)
    # --------------------------------------------------------------------------
    {
        "sutra_no": 9,
        "overall_sutra_no": 19,
        "title": "अप्रमाद आणि निरंतर जागरूकता (Ceaseless Strategic & Operational Alertness)",
        "sanskrit": "॥ अप्रमादो नित्यजागरूकता कार्यसिद्धिप्रदायिनी ॥",
        "matching_pair": {
            "narada": {
                "sutra": "क्षणार्धमपि न व्यर्थं नेयम् ॥ ७७ ॥",
                "meaning_en": "Not even half a moment of precious time should be squandered in idle distraction or negligence (NBS 77).",
                "meaning_mr": "अर्धा क्षणही वाया जाऊ न देता आपल्या कर्तव्यात सदैव मग्न राहिले पाहिजे (नारद सूत्र ७७)."
            },
            "shandilya": {
                "sutra": "अप्रमादो नियमः ॥ ५५ ॥",
                "meaning_en": "Freedom from negligence, slack, and complacency is an absolute, non-negotiable rule (SBS 55).",
                "meaning_mr": "प्रमाद (गाफीलपणा किंवा निष्काळजीपणा) टाळणे हा यशाचा अटळ नियम आहे (शांडिल्य सूत्र ५५)."
            }
        },
        "bharatiya_jnana_basis": {
            "source": "Sant Tukaram Maharaj Abhanga (DOC-04 Section 2.5) & Kautilya's Arthashastra",
            "verse": "आपुलिया हिता जो असे जागता । धन्य त्याची माता सुकृती तो ॥\nकौटिल्य: प्रमादातून राज्य आणि कोशाचा नाश होतो; उत्थानाने रक्षण होते.",
            "meaning_en": "Blessed is he who remains ceaselessly vigilant towards his genuine welfare. Kautilya mandates elimination of executive negligence (Pramada).",
            "meaning_mr": "आपल्या खऱ्या हिताविषयी जो सतत जागृत आणि सावध असतो, तोच खरा धन्य व सुकृती होय. कौटिल्याने प्रमादाला उद्योगाचा सर्वात मोठा शत्रू मानले आहे."
        },
        "padaccheda": "अप्रमादः । नित्य-जागरूकता । कार्य-सिद्धि-प्रदायिनी ॥",
        "anvaya": "अप्रमादः नित्यजागरूकता (च) कार्यसिद्धिप्रदायिनी (भवति) ।",
        "word_by_word": "अप्रमादः (apramādaḥ) = गाफीलपणाचा, आळसाचा संपूर्ण अभाव (Absolute freedom from negligence); नित्यजागरूकता (nitya-jāgarūkatā) = बाजारपेठ, रोख प्रवाह व कामाविषयी सतत सतर्कता (Perpetual operational vigilance); कार्यसिद्धिप्रदायिनी (kārya-siddhi-pradāyinī) = उद्दिष्टपूर्ती व शाश्वत यश देणारी (The bestower of successful accomplishment).",
        "translation_en": "Freedom from operational complacency and perpetual strategic alertness are the direct bestowers of organizational accomplishment.",
        "marathi_explanation": "उद्योगात गाफीलपणा (Pramada) हा सर्वात मोठा गुप्त शत्रू आहे. संत तुकाराम महाराज म्हणतात, 'आपुलिया हिता जो असे जागता, धन्य त्याची माता सुकृती तो.' उद्योजकाने आपल्या व्यवसायाच्या खऱ्या हिताविषयी सदैव जागरूक राहिले पाहिजे. बाजारातील बदलती तंत्रज्ञाने, ग्राहकांची बदलती आवड, स्पर्धकांच्या हालचाली आणि कंपनीचा आर्थिक ताळेबंद याविषयी जो नेता चोवीस तास दक्ष असतो, त्याचे जहाज वादळातही सुरक्षित राहते. एका क्षणाचा निष्काळजीपणा वर्षानुवर्षांचे कष्ट एका झटक्यात नष्ट करू शकतो.",
        "business_and_psychology": "जोखीम व्यवस्थापन (Risk Management) आणि कॅश-फ्लोवर बारीक नजर ठेवणे. यशाच्या नशेत गाफील न राहता संकट येण्यापूर्वीच सावधगिरी बाळगणे हेच परिपक्व नेतृत्वाचे लक्षण आहे."
    },
    # --------------------------------------------------------------------------
    # SUTRA 10 (OVERALL 20)
    # --------------------------------------------------------------------------
    {
        "sutra_no": 10,
        "overall_sutra_no": 20,
        "title": "मंदी आणि लाभाच्या वादळात समत्वबुद्धी (Equanimity Amid Turbulence: Thevile Anante)",
        "sanskrit": "॥ लाभालाभे समत्वबुद्धिः धैर्यं च विजिगीषोः ॥",
        "matching_pair": {
            "narada": {
                "sutra": "शान्तिरूपात् परमानन्दरूपाच्च ॥ ६० ॥",
                "meaning_en": "Because true devotion is of the nature of sublime peace and unshakeable inner serenity (NBS 60).",
                "meaning_mr": "कारण खरी साधना ही अतीव शांती आणि अवर्णनीय समाधानाच्या रूपाने प्रगट होते (नारद सूत्र ६०)."
            },
            "shandilya": {
                "sutra": "चित्तप्रसादात् सर्वदुःखहानिः ॥ २० ॥",
                "meaning_en": "From serene mental clarity proceeds the total dissolution of distress, anxiety, and panic (SBS 20).",
                "meaning_mr": "मनाच्या शांततेतून आणि प्रसन्नतेतून सर्व दुःखांचा व भीतीचा समूळ नाश होतो (शांडिल्य सूत्र २०)."
            }
        },
        "bharatiya_jnana_basis": {
            "source": "Sant Tukaram Maharaj Abhanga (DOC-04 Section 2.6) & Bhagavad Gita 2.48",
            "verse": "ठेविले अनंते तैसेचि रहावे । चित्ती असो द्यावे समाधान ॥\nसिद्ध्यसिद्ध्योः समो भूत्वा समत्वं योग उच्यते ॥",
            "meaning_en": "Remain poised in whatever circumstance Providence places you; let inner peace abide. Equanimity in success and failure is called Yoga.",
            "meaning_mr": "ईश्वराने ज्या स्थितीत ठेवले आहे तिथे मनाचे समाधान ढळू देऊ नये. गीतेत श्रीकृष्णांनी यश-अपयशात समत्व राखण्यालाच योग म्हटले आहे."
        },
        "padaccheda": "लाभ-अलाभे । समत्व-बुद्धिः । धैर्यम् । च । विजिगीषोः ॥",
        "anvaya": "विजिगीषोः लाभालाभे समत्वबुद्धिः धैर्यं च (अनिवार्यं भवति) ।",
        "word_by_word": "लाभालाभे (lābhālābhe) = नफा व तोटा, तेजी व मंदी या दोन्ही प्रसंगांत (In both profit and loss); समत्वबुद्धिः = मानसिक समतोल व बौद्धिक स्थैर्य (Equanimity of intellect and emotional poise); धैर्यम् (dhairyam) = संकटात न डगमगणारे आंतरिक धैर्य (Unshakeable courage and fortitude); च (ca) = आणि (And); विजिगीषोः (vijigīṣoḥ) = विजयाची आकांक्षा बाळगणाऱ्या उद्योजकाचे (Of the visionary leader striving for victory).",
        "translation_en": "Equanimity of intellect in profit and loss, accompanied by unshakeable fortitude, characterizes the visionary entrepreneur destined for victory.",
        "marathi_explanation": "व्यवसायात दररोज नफाच होईल असे कधीही होत नाही; मंदी, संकट, आणि तोटा हे व्यावसायिक प्रवासाचे अविभाज्य भाग आहेत. संत तुकाराम महाराजांचा हा प्रसिद्ध संदेश आहे: 'ठेविले अनंते तैसेचि रहावे, चित्ती असो द्यावे समाधान.' गीतेमध्येही भगवान श्रीकृष्णांनी 'लाभालाभौ जयाजयौ' समान मानण्याचा उपदेश दिला आहे. जेव्हा मोठा नफा होतो तेव्हा हुरळून न जाणे आणि जेव्हा प्रचंड तोटा किंवा संकट येते तेव्हा डोके शांत ठेवून मार्ग शोधणे, हेच महान उद्योजकाचे लक्षण आहे. ज्याची बुद्धी स्थिर असते, तोच मंदीच्या लाटेतूनही संस्थेला सुखरूप बाहेर काढू शकतो.",
        "business_and_psychology": "मानसिक कणखरता (Resilience & Emotional Stability). व्यावसायिक अपयशाने खचून न जाता आणि यशाने उन्मत्त न होता स्वतःच्या ध्येयावर अविचल राहणे हे उद्योजकीय मानसशास्त्राचे सर्वोच्च शिखर आहे."
    }
]
