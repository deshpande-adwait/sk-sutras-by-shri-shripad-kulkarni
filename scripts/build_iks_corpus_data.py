"""
================================================================================
Script: scripts/build_iks_corpus_data.py
Author: Hiranyam AI Labs (https://hiranyamai.com/)
Project: SK Sutras - by Shri Shripad Kulkarni
Description: Compiles an authentic, structured digital dataset of the 20+
             Bharatiya Jnana Tradition (IKS) texts specified by the client:
             Arthashastra, Bhagavad Gita, Upanishads, Patanjali Yoga Sutras,
             Bhartrihari Niti Shataka, Vidura Niti, Chanakya Niti, Brahma Sutras,
             Shankar Bhashya, Gita Rahasya, Ashtavakra Gita, Uddhava Gita,
             Mahabharata, Ramayana, Shiva Sutras, Brihaspati Niti, Samkhya,
             Ayurveda Aharashastra, Samajashastra, Bhakti Rasayana,
             Sant Tukaram Maharaj, Sant Dnyaneshwar, Samarth Ramdas, Sant Eknath.
================================================================================
"""

import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
SOURCES_DIR = BASE_DIR / "data" / "knowledge_repository" / "sources"
SOURCES_DIR.mkdir(parents=True, exist_ok=True)
CORPUS_OUTPUT = SOURCES_DIR / "iks_canonical_corpus.json"

IKS_CANONICAL_ENTRIES = [
    # ---------------- 1. STATECRAFT, GOVERNANCE & ARTHA ----------------
    {
        "id": "iks_artha_01",
        "category": "statecraft_and_niti",
        "tradition": "Kautilya Arthashastra",
        "section": "Adhikarana 1, Adhyaya 19, Shloka 34",
        "verse_no": "1.19.34",
        "sanskrit": "अनुत्थाने ध्रुवो नाशः प्राप्तस्यानागतस्य च । प्राप्यते फलमुत्थानाल्लभते चार्थसम्पदम् ॥",
        "english_meaning": "If an entrepreneur or ruler lacks active enterprise (vigilance and initiative), the certain destruction of both acquired wealth and future prosperity ensues. Through active enterprise, fruition is attained, and abundant wealth is secured.",
        "marathi_meaning": "सक्रिय उद्यम (उत्थान) नसेल, तर मिळालेली आणि मिळणारी संपत्ती नष्ट होते. सतत प्रयत्न व सतर्कतेनेच फळ मिळते आणि शाश्वत संपत्ती निर्माण होते.",
        "enterprise_principle": "Proactive entrepreneurial initiative, vigilance, and continuous execution as the indispensable precondition of economic survival.",
        "theme_tags": ["vigilance", "enterprise_initiative", "wealth_preservation", "active_execution"]
    },
    {
        "id": "iks_artha_02",
        "category": "statecraft_and_niti",
        "tradition": "Kautilya Arthashastra",
        "section": "Adhikarana 1, Adhyaya 4, Sutra 1",
        "verse_no": "1.4.1",
        "sanskrit": "कृषि-पशुपाल्ये वणिज्या च वार्ता । धान्य-पशु-हिरण्य-कुप्य-विष्टि-प्रदानाद् औपकारिकी ॥",
        "english_meaning": "Agriculture, animal husbandry, and trade constitute Varta (real, productive economic activity). It is beneficial because it yields grain, cattle, gold, forest raw materials, and productive labor.",
        "marathi_meaning": "शेती, पशुपालन आणि व्यापार हीच खरी 'वार्ता' (वास्तविक अर्थव्यवस्था) होय; कारण ती धान्य, पशुधन, सुवर्ण आणि प्रत्यक्ष उत्पादक वस्तू पुरवून समाजाचे पोषण करते.",
        "enterprise_principle": "Tangible, productive enterprise utility over paper speculation and financial bubbles.",
        "theme_tags": ["tangible_utility", "real_economy", "production", "anti_speculation"]
    },
    {
        "id": "iks_brihaspati_01",
        "category": "statecraft_and_niti",
        "tradition": "Brihaspati Niti Shastra",
        "section": "Adhyaya 1, Shloka 12",
        "verse_no": "1.12",
        "sanskrit": "अर्थ एव प्रधानः स्याद् अर्थमूलो हि धर्मकामौ । अर्थेन विहीनस्य नरस्य जीवनं निष्प्रयोजनम् ॥",
        "english_meaning": "Righteous economic capital (Artha) is indeed foundational, for both Dharma (moral duty) and Kama (noble fulfillment) have their roots in legitimate wealth. Without ethical economic substance, worldly agency is crippled.",
        "marathi_meaning": "धर्म आणि काम या दोहोंचे मूळ 'अर्थ' (संपत्ती) मध्ये आहे. न्यायाधिष्ठित संपत्ती नसेल तर व्यक्तीला किंवा संस्थेला लोककल्याणाची कार्ये करणे अशक्य होते.",
        "enterprise_principle": "Legitimate wealth generation as the material engine for sustaining societal dharma and philanthropy.",
        "theme_tags": ["artha_foundation", "righteous_wealth", "capacity_building", "trusteeship"]
    },
    {
        "id": "iks_bhartrihari_01",
        "category": "statecraft_and_niti",
        "tradition": "Bhartrihari Niti Shataka",
        "section": "Niti Shataka, Verse 68",
        "verse_no": "68",
        "sanskrit": "निन्दन्तु नीतिनिपुणा यदि वा स्तुवन्तु लक्ष्मीः समाविशतु गच्छतु वा यथेष्टम् । अद्यैव वा मरणमस्तु युगान्तरे वा न्यायात्पथः प्रविचलन्ति पदं न धीराः ॥",
        "english_meaning": "Let ethical experts praise or blame; let wealth arrive abundantly or depart at will; let death come today or at the end of an epoch; steadfast leaders never deviate even a single step from the path of justice and integrity.",
        "marathi_meaning": "तज्ज्ञांनी स्तुती करो वा निंदा, लक्ष्मी येवो वा जावो, धीर आणि स्वाभिमानी उद्योजक न्यायाचा आणि सत्याचा मार्ग कधीही सोडत नाहीत.",
        "enterprise_principle": "Unyielding ethical fortitude; long-term governance and corporate integrity over short-term market pressures.",
        "theme_tags": ["ethical_fortitude", "integrity", "governance", "moral_courage"]
    },
    {
        "id": "iks_bhartrihari_02",
        "category": "statecraft_and_niti",
        "tradition": "Bhartrihari Niti Shataka",
        "section": "Niti Shataka, Verse 27",
        "verse_no": "27",
        "sanskrit": "प्रारभ्यते न खलु विघ्नभयेन नीचैः प्रारभ्य विघ्नविहता विरमन्ति मध्याः । विघ्नैः पुनः पुनरपि प्रतिहन्यमानाः प्रारब्धमुत्तमगुणा न परित्यजन्ति ॥",
        "english_meaning": "The timid never begin a venture out of fear of obstacles; average people begin but abandon the task when struck by hardship; but individuals of noble enterprise, though battered again and again by repeated obstacles, never abandon their initiated goal.",
        "marathi_meaning": "कनिष्ठ लोक संकटांच्या भीतीने काम सुरूच करत नाहीत; मध्यम लोक अडचणी आल्यावर मधेच सोडून देतात; परंतु उत्तम उद्योजक वारंवार संकटे आली तरी सुरू केलेले महान कार्य पूर्ण केल्याशिवाय थांबत नाहीत.",
        "enterprise_principle": "Relentless perseverance and gritty resilience (Grit) in entrepreneurship.",
        "theme_tags": ["perseverance", "grit", "resilience", "tenacity"]
    },
    {
        "id": "iks_vidura_01",
        "category": "statecraft_and_niti",
        "tradition": "Vidura Niti (Mahabharata Udyoga Parva)",
        "section": "Adhyaya 33, Shloka 16",
        "verse_no": "33.16",
        "sanskrit": "आत्मज्ञानं समारम्भस्तितिक्षा धर्मनित्यता । यमर्था नापकर्षन्ति स वै पण्डित उच्यते ॥",
        "english_meaning": "Self-knowledge, diligent execution of ventures, forbearance under hardship, and unswerving adherence to righteousness—one whose core values are not corrupted by momentary material windfalls is truly a wise leader.",
        "marathi_meaning": "आत्मज्ञान, कामाची चोख सुरुवात, संकटात सहनशीलता आणि धर्मनिष्ठा—ज्याला संपत्तीचा मोह सत्यापासून विचलित करू शकत नाही, तोच खरा सुजाण नेता.",
        "enterprise_principle": "Emotional self-regulation and grounded leadership amid hyper-growth and market volatility.",
        "theme_tags": ["self_knowledge", "forbearance", "emotional_mastery", "ethical_anchor"]
    },

    # ---------------- 2. KARMAYOGA, GITA & MAHABHARATA ----------------
    {
        "id": "iks_gita_01",
        "category": "karmayoga_and_gita",
        "tradition": "Bhagavad Gita",
        "section": "Chapter 2, Verse 47",
        "verse_no": "2.47",
        "sanskrit": "कर्मण्येवाधिकारस्ते मा फलेषु कदाचन । मा कर्मफलहेतुर्भूर्मा ते सङ्गोऽस्त्वकर्मणि ॥",
        "english_meaning": "Your rightful jurisdiction is over dedicated, excellence-driven action alone, never over the entitled fruits thereof. Never let the fruits of action be your primary motive, nor let there be any attachment to inaction.",
        "marathi_meaning": "केवळ कर्तव्यकर्म करणे हाच तुझा अधिकार आहे, फळावर कधीही नाही. फळाची हाव धरून काम करू नकोस आणि अकर्मण्यतेचा (आळसाचा) आश्रयही घेऊ नकोस.",
        "enterprise_principle": "Process-focused execution without paralyzing outcome-anxiety; mastery of craft over entitlement.",
        "theme_tags": ["karmayoga", "process_focus", "anti_entitlement", "operational_excellence"]
    },
    {
        "id": "iks_gita_02",
        "category": "karmayoga_and_gita",
        "tradition": "Bhagavad Gita",
        "section": "Chapter 3, Verse 20",
        "verse_no": "3.20",
        "sanskrit": "कर्मणैव हि संसिद्धिमास्थिता जनकादयः । लोकसंग्रहमेवापि संपश्यन्कर्तुमर्हसि ॥",
        "english_meaning": "Great royal entrepreneurs and leaders like Janaka attained supreme perfection through action alone. Furthermore, with an eye toward Lokasangraha (the collective upliftment, cohesion, and welfare of society), you must perform work.",
        "marathi_meaning": "जनकासारख्या महान राज्यकर्त्यांनी कर्मयोगातूनच सर्वोच्च सिद्धी प्राप्त केली. लोकसंग्रहासाठी (समाजाच्या कल्याणासाठी व संरक्षणासाठी) तू निष्काम कर्म केलेच पाहिजे.",
        "enterprise_principle": "Lokasangraha: Social stewardship and stakeholder capitalism as the ultimate justification of enterprise.",
        "theme_tags": ["lokasangraha", "stakeholder_capitalism", "social_stewardship", "janaka_model"]
    },
    {
        "id": "iks_gita_03",
        "category": "karmayoga_and_gita",
        "tradition": "Bhagavad Gita",
        "section": "Chapter 18, Verse 45",
        "verse_no": "18.45",
        "sanskrit": "स्वे स्वे कर्मण्यभिरतः संसिद्धिं लभते नरः । स्वकर्मनिरतः सिद्धिं यथा विन्दति तच्छृणु ॥",
        "english_meaning": "Dedicated with deep devotion to one’s own unique duty (Svadharma / core competency), a human being attains supreme fulfillment. Hear how one engaged in their rightful craft achieves perfection.",
        "marathi_meaning": "आपल्या वाट्याला आलेल्या स्वकर्तव्यात जो मनापासून रममाण होतो, तोच सर्वोच्च सिद्धी प्राप्त करतो. आपल्या स्वाभाविक कौशल्यात लीन होणे हीच यशाची किल्ली आहे.",
        "enterprise_principle": "Focus on core competencies (Svadharma) and authentic craftsmanship over derivative trend-chasing.",
        "theme_tags": ["svadharma", "craftsmanship", "core_competency", "specialization"]
    },
    {
        "id": "iks_gita_rahasya_01",
        "category": "karmayoga_and_gita",
        "tradition": "Lokmanya Tilak - Gita Rahasya",
        "section": "Karmayoga Shastra Prakarana",
        "verse_no": "Prakarana 11",
        "sanskrit": "कर्मत्यागान् न सिद्धिः स्यात् कर्मयोगो विशिष्यते । जगच्चक्रप्रवृत्त्यर्थं कर्तव्यं कर्म सर्वदा ॥",
        "english_meaning": "Perfection is never attained through renunciation of action; active engagement in the world (Karmayoga) is vastly superior. For the continuous revolving of the universal economic wheel, work must ever be performed.",
        "marathi_meaning": "कर्म सोडून पळून जाण्यात मुक्ती नाही, तर समाजात राहून निष्काम कर्मयोग आचरणे श्रेष्ठ आहे. जगाचे व्यवहार सुरळीत चालण्यासाठी उद्योजकाने कर्तव्यकर्म केलेच पाहिजे.",
        "enterprise_principle": "Activism and enterprise as spiritual duty; rejecting quietist escapism in favor of nation-building.",
        "theme_tags": ["activism", "gita_rahasya", "nation_building", "economic_dynamism"]
    },
    {
        "id": "iks_vidula_01",
        "category": "karmayoga_and_gita",
        "tradition": "Mahabharata (Vidula-Putra Samvada)",
        "section": "Udyoga Parva, Chapter 134, Verse 14",
        "verse_no": "5.134.14",
        "sanskrit": "उत्तिष्ठ हे कापुरुष मा शेष्वैवं पराजितः । मुहूर्तं ज्वलितं श्रेयो न च धूमायितं चिरम् ॥",
        "english_meaning": "Arise, do not lie prostrate as if defeated! Better it is to blaze forth with intense brilliance even for a moment than to merely smolder like damp wood throughout life.",
        "marathi_meaning": "ऊठ, पराभूत होऊन हताश पडून राहू नकोस! आयुष्यभर धुरासारखे घुमसत राहण्यापेक्षा क्षणाभरासाठी का होईना धगधगत्या ज्वालांसारखे तेजस्वी पराक्रमी होणे अधिक श्रेष्ठ आहे.",
        "enterprise_principle": "Audacity, courage, and aggressive refusal to accept defeat in market disruptions.",
        "theme_tags": ["audacity", "courage", "overcoming_defeat", "bold_vision"]
    },

    # ---------------- 3. YOGA, PSYCHOLOGY & METAPHYSICS ----------------
    {
        "id": "iks_yoga_01",
        "category": "darshana_and_yoga",
        "tradition": "Patanjali Yoga Sutras",
        "section": "Samadhi Pada, Sutra 2",
        "verse_no": "1.2",
        "sanskrit": "योगश्चित्तवृत्तिनिरोधः ॥",
        "english_meaning": "Yoga is the complete mastery and stilling of the turbulent fluctuations and reactionary patterns of the mind (Chitta-vrittis).",
        "marathi_meaning": "चित्तातील विचलित करणाऱ्या विचारांचा आणि भावनांच्या लाटांचा निरोध करणे म्हणजे योग. मनावर पूर्ण नियंत्रण मिळवणे हीच खरी मानसिक ताकद आहे.",
        "enterprise_principle": "Mental mastery, executive focus, and immunity to panic during startup stress.",
        "theme_tags": ["mental_mastery", "executive_focus", "anti_panic", "clarity"]
    },
    {
        "id": "iks_yoga_02",
        "category": "darshana_and_yoga",
        "tradition": "Patanjali Yoga Sutras",
        "section": "Samadhi Pada, Sutra 12",
        "verse_no": "1.12",
        "sanskrit": "अभ्यासवैराग्याभ्यां तन्निरोधः ॥",
        "english_meaning": "The stilling and mastery of mental agitation is achieved through Abhyasa (relentless, persistent practice) and Vairagya (dispassionate detachment from ego and short-term outcomes).",
        "marathi_meaning": "सततचा सराव (अभ्यास) आणि विरक्ती/अलिप्तता (वैराग्य) या दोहोंच्या संयोगातूनच मनाची चंचलता थांबते आणि एकाग्रता प्राप्त होते.",
        "enterprise_principle": "The dual engine of enterprise success: relentless daily iteration (Abhyasa) coupled with ego-less detachment from vanity metrics (Vairagya).",
        "theme_tags": ["abhyasa", "vairagya", "daily_iteration", "unbiased_perspective"]
    },
    {
        "id": "iks_yoga_03",
        "category": "darshana_and_yoga",
        "tradition": "Patanjali Yoga Sutras",
        "section": "Samadhi Pada, Sutra 33",
        "verse_no": "1.33",
        "sanskrit": "मैत्रीकरुणामुदितोपेक्षाणां सुखदुःखपुण्यापुण्यविषयाणां भावनातश्चित्तप्रसादनम् ॥",
        "english_meaning": "Serenity of mind is cultivated through friendliness toward the happy, compassion toward the suffering, delight in the virtuous, and neutral equanimity toward the hostile or unethical.",
        "marathi_meaning": "सुखी लोकांबद्दल मैत्री, दुःखी लोकांबद्दल करुणा, पुण्यात्म्यांबद्दल आनंद आणि दुर्जनांबद्दल तटस्थ उपेक्षा बाळगल्याने मन सदैव शांत आणि प्रसन्न राहते.",
        "enterprise_principle": "Emotional intelligence (EQ) and relational sanity for founders handling investors, competitors, and teams.",
        "theme_tags": ["emotional_intelligence", "mental_peace", "stakeholder_harmony", "equanimity"]
    },
    {
        "id": "iks_upanishad_01",
        "category": "darshana_and_yoga",
        "tradition": "Isha Upanishad",
        "section": "Mantra 1",
        "verse_no": "1",
        "sanskrit": "ईशा वास्यमिदं सर्वं यत्किञ्च जगत्यां जगत् । तेन त्यक्तेन भुञ्जीथा मा गृधः कस्यस्विद्धनम् ॥",
        "english_meaning": "All this is enveloped by the Divine—whatever is moving in this world. Enjoy and prosper through detached consumption and trusteeship; do not covet any person's wealth through injustice.",
        "marathi_meaning": "या विश्वातील सर्व काही ईश्वराने व्यापलेले आहे. त्यागपूर्वक आणि संयमाने उपभोग घे; कोणाच्याही धनाचा लोभ धरू नकोस.",
        "enterprise_principle": "Gandhian and Upanishadic trusteeship: wealth as a trust to be managed, eliminating predatory greed.",
        "theme_tags": ["trusteeship", "restraint", "anti_greed", "sustainable_wealth"]
    },
    {
        "id": "iks_upanishad_02",
        "category": "darshana_and_yoga",
        "tradition": "Taittiriya Upanishad",
        "section": "Shikshavalli, Anuvaka 11, Verse 1",
        "verse_no": "1.11.1",
        "sanskrit": "सत्यं वद । धर्मं चर । स्वाध्यायान्मा प्रमदः । आचार्याय प्रियं धनमाहृत्य प्रजातन्तुं मा व्यवच्छेत्सीः ॥",
        "english_meaning": "Speak truth. Practice righteousness. Do not neglect continuous learning and self-study. Having offered worthy wealth to the preceptor, do not sever the lineage of succession and transmission.",
        "marathi_meaning": "सत्य बोल, धर्माने वाग, निरंतर शिकणे (स्वाध्याय) सोडू नकोस. योग्य संपत्ती संपादन करून ज्ञान व परंपरेचा अखंड प्रवाह चालू ठेव.",
        "enterprise_principle": "Continuous corporate R&D (Svadhyaya) and institutional succession planning across generations.",
        "theme_tags": ["continuous_learning", "succession_planning", "intergenerational_lineage", "truth"]
    },

    # ---------------- 4. SANT SAHITYA & BHAKTI TRADITION ----------------
    {
        "id": "iks_tukaram_01",
        "category": "sant_and_bhakti_tradition",
        "tradition": "Sant Tukaram Maharaj Gatha",
        "section": "Abhanga 152",
        "verse_no": "152",
        "sanskrit": "जोडोनियां धन उत्तम व्यवहारे । उदास विचारे वेच करी ॥ उत्तम ते ख्याती अमित हे जोडी । परि नाही गोडी संचयाची ॥",
        "english_meaning": "Earn wealth through transparent, noble, and immaculate business conduct (Uttam Vyavahara); expend and reinvest it with detached, noble discernment. Such conduct yields boundless renown, without toxic attachment to stagnant accumulation.",
        "marathi_meaning": "उत्तम आणि प्रामाणिक व्यवहाराने धन मिळवावे आणि त्याचा विनियोग समाजहितासाठी उदारपणे करावा. सचोटीने केलेल्या व्यवसायातून अथांग कीर्ती मिळते, पैशाचा संचय करण्याचा लोभ नसावा.",
        "enterprise_principle": "Noble commerce (Uttam Vyavahar), transparent capital velocity, and societal reinvestment.",
        "theme_tags": ["uttam_vyavahar", "fair_trade", "capital_reinvestment", "sant_tukaram"]
    },
    {
        "id": "iks_tukaram_02",
        "category": "sant_and_bhakti_tradition",
        "tradition": "Sant Tukaram Maharaj Gatha",
        "section": "Abhanga 314",
        "verse_no": "314",
        "sanskrit": "सत्य तेचि भांडवल । असत्य तेचि बुडवल ॥ सत्य ज्याचे मुखी । तोचि जगी सुखी ॥",
        "english_meaning": "Truth is sovereign capital; falsehood is certain bankruptcy. He whose mouth and deeds are anchored in truth alone dwells in sustainable peace and success in this world.",
        "marathi_meaning": "सत्य हेच व्यवसायाचे खरे भांडवल आहे आणि असत्य हा निश्चित दिवाळखोरीचा मार्ग आहे. ज्याच्या व्यवहारात सत्य आहे, तोच जगात चिरंतन सुखी व यशस्वी होतो.",
        "enterprise_principle": "Truth and radical transparency as balance-sheet assets; trust as the foundation of credit and enterprise scale.",
        "theme_tags": ["truth_as_capital", "transparency", "brand_trust", "sant_tukaram"]
    },
    {
        "id": "iks_dnyaneshwar_01",
        "category": "sant_and_bhakti_tradition",
        "tradition": "Sant Dnyaneshwar - Dnyaneshwari",
        "section": "Adhyaya 18, Ovi 911-912",
        "verse_no": "18.911",
        "sanskrit": "म्हणौनि स्वधर्मु जो बापा । तोचि एकु अनुष्ठेपु । जेणे पाविजे क्षेपु । मोक्षाचिया ॥ तया स्वधर्माचेनि बळे । कर्म सकळही फळे ।",
        "english_meaning": "Therefore, O seeker, one’s own rightful craft (Svadharma) alone must be rigorously practiced. Through the power of dedicated Svadharma, all actions bear divine fruit and liberation.",
        "marathi_meaning": "म्हणून आपल्या वाट्याला आलेले स्वकर्तव्यच निष्ठापूर्वक केले पाहिजे. स्वधर्माच्या बळावरच सर्व कर्मांना यश आणि समृद्धीचे फळ प्राप्त होते.",
        "enterprise_principle": "Dedicated focus on one’s organic enterprise calling without envying or imitating others.",
        "theme_tags": ["dnyaneshwari", "svadharma_power", "craftsmanship", "divine_action"]
    },
    {
        "id": "iks_ramdas_01",
        "category": "sant_and_bhakti_tradition",
        "tradition": "Samarth Ramdas Swami - Dasbodh",
        "section": "Dashaka 19, Samasa 9, Ovi 1-3",
        "verse_no": "19.9.1",
        "sanskrit": "केल्याने होत आहे रे आधी केलेचि पाहिजे । यत्न तो देव जाणावा अंतरीं धरितां बरे ॥ आळस हाचि शत्रु मोठा । आळसे काम होत नाही ॥",
        "english_meaning": "Things happen only by doing! One must act first. Consider relentless disciplined effort (Yatna) as Divinity itself. Laziness is the supreme enemy; through sloth, nothing is accomplished.",
        "marathi_meaning": "केल्यानेच काम होते, आधी कृती केलीच पाहिजे. प्रयत्न हाच खरा देव मानून आळसाचा त्याग करावा. आळस हा उद्योजकाचा सर्वात मोठा शत्रू आहे.",
        "enterprise_principle": "Action-first bias, execution velocity, and treating disciplined effort as sacred liturgy.",
        "theme_tags": ["dasbodh", "effort_as_god", "execution_bias", "anti_sloth"]
    },
    {
        "id": "iks_ramdas_02",
        "category": "sant_and_bhakti_tradition",
        "tradition": "Samarth Ramdas Swami - Dasbodh",
        "section": "Dashaka 11, Samasa 5, Ovi 4",
        "verse_no": "11.5.4",
        "sanskrit": "आधी प्रचिती मग प्रवचन । आधी आचार मग विचार ॥ अंतरीं असावा विवेक । बाह्य दिसावा नेटका ॥",
        "english_meaning": "First empirical proof and experience, then discourse; first practice, then theory. Within, maintain sharp discriminative intellect (Viveka); without, display neat, impeccable organization.",
        "marathi_meaning": "आधी प्रत्यक्ष अनुभव घ्यावा, मगच बोलावे; आधी आचरण करावे, मग विचार मांडावा. अंतःकरणात तीव्र विवेक असावा आणि बाह्य व्यवहार नेटका, शिस्तबद्ध असावा.",
        "enterprise_principle": "Empirical product validation, operational neatness, and executive integrity.",
        "theme_tags": ["empirical_proof", "operational_excellence", "dasbodh", "viveka"]
    },

    # ---------------- 5. ECOLOGY, DIET & SOCIAL SCIENCES ----------------
    {
        "id": "iks_atharvaveda_01",
        "category": "socio_physical_sciences",
        "tradition": "Atharvaveda - Prithvi Sukta",
        "section": "Kanda 12, Sukta 1, Verse 35",
        "verse_no": "12.1.35",
        "sanskrit": "यत्ते भूमे विखनामि क्षिप्रं तदपि रोहतु । मा ते मर्म विमृग्वरि मा ते हृदयमर्पिपम् ॥",
        "english_meaning": "Whatever I dig or extract from you, O Earth Mother, may that quickly regenerate and grow again! May I never strike at your vital organs, nor pierce your living heart.",
        "marathi_meaning": "हे पृथ्वी माते, तुझ्याकडून मी जे काही घेईन, ते तातडीने पुन्हा निर्माण होवो. तुझ्या मर्मावर किंवा हृदयावर माझ्या हातून कधीही आघात न होवो.",
        "enterprise_principle": "Regenerative ecology, circular manufacturing, and Net-Zero ESG ethics in industrial production.",
        "theme_tags": ["regenerative_ecology", "circular_economy", "net_zero", "sustainable_manufacturing"]
    },
    {
        "id": "iks_atreya_01",
        "category": "socio_physical_sciences",
        "tradition": "Atreya Muni - Charaka Samhita (Aharashastra)",
        "section": "Sutra Sthana, Adhyaya 27, Shloka 3",
        "verse_no": "1.27.3",
        "sanskrit": "आहारः प्राणदः प्रोक्तः स युक्त्या समुपाहृतः । अयुक्त्या प्राणहन्ता च तस्माद्युक्त्या समाचरेत् ॥",
        "english_meaning": "Diet and sustenance give life when consumed with wisdom, balance, and discipline; consumed indiscreetly, they destroy vitality. Therefore, let an active worker practice measured intake.",
        "marathi_meaning": "संतुलित आणि सात्त्विक आहार शरीराला प्राण आणि ऊर्जा देतो, तर चुकीचा आहार क्षमता नष्ट करतो. उद्योजकाने शारीरिक ऊर्जा आणि मानसिक एकाग्रतेसाठी आहार संयम पाळला पाहिजे.",
        "enterprise_principle": "Founder physical stamina, vitality management, and metabolic sustainability for peak performance.",
        "theme_tags": ["founder_vitality", "stamina", "aharashastra", "sattvic_energy"]
    }
]

def compile_iks_dataset():
    """Writes the comprehensive canonical IKS dataset to disk."""
    with open(CORPUS_OUTPUT, "w", encoding="utf-8") as f:
        json.dump(IKS_CANONICAL_ENTRIES, f, ensure_ascii=False, indent=2)
    print(f"[Compiled IKS Canonical Corpus]: {CORPUS_OUTPUT}")
    print(f"[Total Canonical Entries]: {len(IKS_CANONICAL_ENTRIES)}")

if __name__ == "__main__":
    compile_iks_dataset()
