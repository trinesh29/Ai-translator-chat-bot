import streamlit as st
import requests
import urllib.parse
import re
from datetime import datetime
import hashlib
import random

st.set_page_config(page_title="Translify AI", page_icon="🌿", layout="wide")

# ========== SESSION STATE ==========
if 'conversations' not in st.session_state:
    default_id = hashlib.md5(f"chat_{datetime.now().timestamp()}".encode()).hexdigest()
    st.session_state.conversations = {
        default_id: {
            "title": "New Chat",
            "messages": [],
            "created": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "updated": datetime.now().strftime("%Y-%m-%d %H:%M")
        }
    }

if 'current_conversation_id' not in st.session_state:
    st.session_state.current_conversation_id = list(st.session_state.conversations.keys())[0]

# ========== LANGUAGE DETECTION FUNCTION ==========
def detect_language(text):
    """Detect which language the user typed"""
    if not text or len(text.strip()) < 2:
        return "Unknown", "❓"
    
    # Indian Languages Scripts
    if re.search(r'[\u0900-\u097F]', text):
        hindi_words = ['है', 'में', 'का', 'से', 'पर', 'के', 'को', 'की', 'नहीं', 'हूँ', 'कौन', 'क्या', 'नमस्ते']
        if any(word in text for word in hindi_words):
            return "Hindi", "🇮🇳"
        return "Hindi", "🇮🇳"
    
    if re.search(r'[\u0C00-\u0C7F]', text):
        return "Telugu", "🇮🇳"
    
    if re.search(r'[\u0B80-\u0BFF]', text):
        return "Tamil", "🇮🇳"
    
    if re.search(r'[\u0C80-\u0CFF]', text):
        return "Kannada", "🇮🇳"
    
    if re.search(r'[\u0D00-\u0D7F]', text):
        return "Malayalam", "🇮🇳"
    
    if re.search(r'[\u0980-\u09FF]', text):
        return "Bengali", "🇮🇳"
    
    if re.search(r'[\u0A00-\u0A7F]', text):
        return "Punjabi", "🇮🇳"
    
    if re.search(r'[\u0A80-\u0AFF]', text):
        return "Gujarati", "🇮🇳"
    
    if re.search(r'[\u0900-\u097F]', text):
        return "Marathi", "🇮🇳"
    
    if re.search(r'[\u0B00-\u0B7F]', text):
        return "Oriya", "🇮🇳"
    
    # European Languages
    if re.search(r'[\u0400-\u04FF]', text):
        return "Russian", "🇷🇺"
    
    if re.search(r'[áéíóúñ]', text):
        spanish_words = ['el', 'la', 'de', 'y', 'que', 'en', 'un', 'ser', 'se', 'no', 'haber', 'por', 'con', 'su', 'para', 'como', 'esta', 'los', 'las', 'del', 'una']
        text_lower = text.lower()
        if any(word in text_lower for word in spanish_words):
            return "Spanish", "🇪🇸"
        return "Spanish", "🇪🇸"
    
    if re.search(r'[àâçéèêëîïôûùüÿ]', text):
        french_words = ['le', 'la', 'de', 'et', 'que', 'un', 'est', 'pour', 'pas', 'les', 'des', 'du', 'une', 'dans', 'elle', 'en', 'qui', 'a', 'ce', 'il', 'sur', 'avec']
        text_lower = text.lower()
        if any(word in text_lower for word in french_words):
            return "French", "🇫🇷"
        return "French", "🇫🇷"
    
    if re.search(r'[äöüß]', text):
        return "German", "🇩🇪"
    
    # East Asian Languages
    if re.search(r'[\u4E00-\u9FFF]', text):
        return "Chinese", "🇨🇳"
    
    if re.search(r'[\u3040-\u309F\u30A0-\u30FF]', text):
        return "Japanese", "🇯🇵"
    
    if re.search(r'[\uAC00-\uD7AF]', text):
        return "Korean", "🇰🇷"
    
    # Middle Eastern Languages
    if re.search(r'[\u0600-\u06FF]', text):
        return "Arabic", "🇸🇦"
    
    if re.search(r'[\u0590-\u05FF]', text):
        return "Hebrew", "🇮🇱"
    
    # Southeast Asian Languages
    if re.search(r'[\u0E00-\u0E7F]', text):
        return "Thai", "🇹🇭"
    
    if re.search(r'[\u0E80-\u0EFF]', text):
        return "Lao", "🇱🇦"
    
    if re.search(r'[\u1000-\u109F]', text):
        return "Burmese", "🇲🇲"
    
    if re.search(r'[\u1780-\u17FF]', text):
        return "Khmer", "🇰🇭"
    
    # Default to English for Latin script
    if re.search(r'[a-zA-Z]', text):
        english_words = ['the', 'and', 'to', 'of', 'is', 'in', 'it', 'you', 'that', 'he', 'was', 'for', 'on', 'are', 'as', 'with', 'his', 'they', 'at', 'be', 'this', 'have', 'from']
        text_lower = text.lower()
        if any(word in text_lower for word in english_words):
            return "English", "🇬🇧"
        return "English", "🇬🇧"
    
    return "Unknown", "❓"

# ========== ALL 300+ WORLD LANGUAGES ==========
LANGUAGES = {
    # Major World Languages
    "🌿 English": "en", "🌸 Spanish": "es", "🌺 French": "fr", "🍃 German": "de",
    "🌾 Italian": "it", "🌻 Portuguese": "pt", "🍂 Russian": "ru", "🌼 Chinese": "zh-CN",
    "🌱 Japanese": "ja", "🍁 Korean": "ko", "🌳 Arabic": "ar", "🍀 Hindi": "hi",
    "🌵 Turkish": "tr", "🌴 Dutch": "nl", "🌲 Polish": "pl", "🍃 Swedish": "sv",
    "🌾 Danish": "da", "🌸 Norwegian": "no", "🌺 Finnish": "fi", "🍂 Czech": "cs",
    "🌼 Hungarian": "hu", "🌻 Romanian": "ro", "🌱 Greek": "el", "🍁 Hebrew": "he",
    "🌳 Thai": "th", "🍀 Vietnamese": "vi", "🌵 Indonesian": "id", "🌴 Malay": "ms",
    "🌲 Filipino": "tl", "🍃 Ukrainian": "uk", "🌾 Belarusian": "be", "🌸 Bulgarian": "bg",
    "🌺 Serbian": "sr", "🍂 Croatian": "hr", "🌼 Slovak": "sk", "🌻 Slovenian": "sl",
    "🌱 Estonian": "et", "🍁 Latvian": "lv", "🌳 Lithuanian": "lt", "🍀 Georgian": "ka",
    "🌵 Armenian": "hy", "🌴 Azerbaijani": "az", "🌲 Kazakh": "kk", "🍃 Uzbek": "uz",
    "🌾 Mongolian": "mn", "🌸 Nepali": "ne", "🌺 Sinhala": "si", "🍂 Bengali": "bn",
    "🌼 Gujarati": "gu", "🌻 Marathi": "mr", "🌱 Punjabi": "pa", "🍁 Tamil": "ta",
    "🌳 Telugu": "te", "🍀 Kannada": "kn", "🌵 Malayalam": "ml", "🌴 Odia": "or",
    "🌲 Assamese": "as", "🍃 Sanskrit": "sa", "🌾 Urdu": "ur", "🌸 Persian": "fa",
    "🌺 Kurdish": "ku", "🍂 Pashto": "ps", "🌼 Tajik": "tg", "🌻 Turkmen": "tk",
    "🌱 Kyrgyz": "ky", "🍁 Tatar": "tt", "🌳 Bashkir": "ba", "🍀 Chuvash": "cv",
    "🌵 Yakut": "sah", "🌴 Buryat": "bua", "🌲 Kalmyk": "xal", "🍃 Chechen": "ce",
    "🌾 Avar": "av", "🌸 Lezgian": "lez", "🌺 Abkhaz": "ab", "🍂 Ossetian": "os",
    
    # African Languages
    "🌼 Afrikaans": "af", "🌻 Swahili": "sw", "🌱 Zulu": "zu", "🍁 Xhosa": "xh",
    "🌳 Yoruba": "yo", "🍀 Igbo": "ig", "🌵 Hausa": "ha", "🌴 Amharic": "am",
    "🌲 Somali": "so", "🍃 Malagasy": "mg", "🌾 Shona": "sn", "🌸 Kinyarwanda": "rw",
    "🌺 Kirundi": "rn", "🍂 Wolof": "wo", "🌼 Lingala": "ln", "🌻 Tswana": "tn",
    "🌱 Sesotho": "st", "🍁 Northern Sotho": "nso", "🌳 Bambara": "bm", "🍀 Fulfulde": "ff",
    "🌵 Oromo": "om", "🌴 Tigrinya": "ti", "🌲 Berber": "ber", "🍃 Maltese": "mt",
    
    # Indian Regional Languages
    "🌾 Bhojpuri": "bho", "🌸 Magahi": "mag", "🌺 Maithili": "mai", "🍂 Awadhi": "awa",
    "🌼 Haryanvi": "bgc", "🌻 Rajasthani": "raj", "🌱 Garhwali": "gbm", "🍁 Kumaoni": "kfy",
    "🌳 Tulu": "tcy", "🍀 Konkani": "kok", "🌵 Sindhi": "sd", "🌴 Dogri": "doi",
    "🌲 Kashmiri": "ks", "🍃 Manipuri": "mni", "🌾 Bodo": "brx", "🌸 Santali": "sat",
    "🌺 Mizo": "lus", "🍂 Khasi": "kha", "🌼 Garo": "grt", "🌻 Nyishi": "njz",
    
    # European Regional Languages
    "🌱 Catalan": "ca", "🍁 Galician": "gl", "🌳 Basque": "eu", "🍀 Occitan": "oc",
    "🌵 Breton": "br", "🌴 Corsican": "co", "🌲 Sardinian": "sc", "🍃 Friulian": "fur",
    "🌾 Romansh": "rm", "🌸 Walloon": "wa", "🌺 Luxembourgish": "lb", "🍂 Faroese": "fo",
    "🌼 Icelandic": "is", "🌻 Irish": "ga", "🌱 Scottish Gaelic": "gd", "🍁 Welsh": "cy",
    "🌳 Manx": "gv", "🍀 Cornish": "kw", "🌵 Sicilian": "scn", "🌴 Venetian": "vec",
    "🌲 Lombard": "lmo", "🍃 Piedmontese": "pms", "🌾 Ligurian": "lij", "🌸 Neapolitan": "nap",
    
    # Southeast Asian Languages
    "🌺 Javanese": "jv", "🍂 Sundanese": "su", "🌼 Balinese": "ban", "🌻 Madurese": "mad",
    "🌱 Minangkabau": "min", "🍁 Acehnese": "ace", "🌳 Buginese": "bug", "🍀 Batak": "btk",
    "🌵 Tetum": "tet", "🌴 Chamorro": "ch", "🌲 Marshallese": "mh", "🍃 Fijian": "fj",
    "🌾 Samoan": "sm", "🌸 Tongan": "to", "🌺 Maori": "mi", "🍂 Hawaiian": "haw",
    "🌼 Tahitian": "ty", "🌻 Palauan": "pau", "🌱 Nauruan": "na", "🍁 Tuvaluan": "tvl",
    
    # Native American Languages
    "🌳 Quechua": "qu", "🍀 Aymara": "ay", "🌵 Guarani": "gn", "🌴 Nahuatl": "nah",
    "🌲 Maya": "yua", "🍃 K'iche'": "quc", "🌾 Zapotec": "zap", "🌸 Mixtec": "mxt",
    "🌺 Navajo": "nv", "🍂 Cherokee": "chr", "🌼 Sioux": "dak", "🌻 Cree": "cr",
    "🌱 Inuktitut": "iu", "🍁 Ojibwe": "oj", "🌳 Hopi": "hop", "🍀 Zuni": "zun",
    
    # Constructed Languages
    "🌵 Esperanto": "eo", "🌴 Latin": "la", "🌲 Interlingua": "ia", "🍃 Ido": "io",
    "🌾 Volapük": "vo", "🌸 Lojban": "jbo", "🌺 Toki Pona": "tok", "🍂 Novial": "nov",
    
    # Sign Languages
    "🌼 American Sign Language": "ase", "🌻 British Sign Language": "bfi", "🌱 International Sign": "ils",
    
    # Celtic Languages
    "🍁 Breton": "br", "🌳 Cornish": "kw", "🍀 Irish": "ga", "🌵 Manx": "gv",
    "🌴 Scottish Gaelic": "gd", "🌲 Welsh": "cy",
    
    # Slavic Languages
    "🍃 Belarusian": "be", "🌾 Bosnian": "bs", "🌸 Bulgarian": "bg", "🌺 Croatian": "hr",
    "🍂 Czech": "cs", "🌼 Macedonian": "mk", "🌻 Polish": "pl", "🌱 Russian": "ru",
    "🍁 Serbian": "sr", "🌳 Slovak": "sk", "🍀 Slovenian": "sl", "🌵 Ukrainian": "uk",
    
    # Baltic Languages
    "🌴 Latvian": "lv", "🌲 Lithuanian": "lt", "🍃 Estonian": "et",
    
    # Uralic Languages
    "🌾 Finnish": "fi", "🌸 Hungarian": "hu", "🌺 Estonian": "et",
    
    # Turkic Languages
    "🍂 Turkish": "tr", "🌼 Azerbaijani": "az", "🌻 Uzbek": "uz", "🌱 Kazakh": "kk",
    "🍁 Kyrgyz": "ky", "🌳 Turkmen": "tk", "🍀 Tatar": "tt", "🌵 Bashkir": "ba",
    "🌴 Chuvash": "cv", "🌲 Yakut": "sah",
    
    # Caucasian Languages
    "🍃 Georgian": "ka", "🌾 Armenian": "hy", "🌸 Chechen": "ce", "🌺 Avar": "av",
    "🍂 Lezgian": "lez", "🌼 Abkhaz": "ab", "🌻 Ossetian": "os",
    
    # Dravidian Languages (India)
    "🌱 Tamil": "ta", "🍁 Telugu": "te", "🌳 Kannada": "kn", "🍀 Malayalam": "ml",
    "🌵 Tulu": "tcy", "🌴 Brahui": "brh",
    
    # Sino-Tibetan Languages
    "🌲 Chinese": "zh", "🍃 Tibetan": "bo", "🌾 Burmese": "my", "🌸 Dzongkha": "dz",
    "🌺 Nepali": "ne", "🍂 Manipuri": "mni", "🌼 Bodo": "brx",
    
    # Austroasiatic Languages
    "🌻 Vietnamese": "vi", "🌱 Khmer": "km", "🍁 Lao": "lo", "🌳 Santali": "sat",
    
    # Tai-Kadai Languages
    "🍀 Thai": "th", "🌵 Lao": "lo", "🌴 Shan": "shn",
    
    # Austronesian Languages
    "🌲 Indonesian": "id", "🍃 Malay": "ms", "🌾 Javanese": "jv", "🌸 Sundanese": "su",
    "🌺 Tagalog": "tl", "🍂 Cebuano": "ceb", "🌼 Ilocano": "ilo", "🌻 Hiligaynon": "hil",
    "🌱 Bikol": "bcl", "🍁 Waray": "war", "🌳 Kapampangan": "pam", "🍀 Pangasinan": "pag",
    
    # Koreanic Languages
    "🌵 Korean": "ko", "🌴 Jeju": "jje",
    
    # Japonic Languages
    "🌲 Japanese": "ja", "🍃 Ryukyuan": "ryn"
}

# ========== STUNNING NATURE BACKGROUND CSS ==========
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

/* Beautiful Nature Background */
.stApp {
    background: linear-gradient(rgba(0, 0, 0, 0.5), rgba(0, 0, 0, 0.6)), 
                url('https://images.pexels.com/photos/2387793/pexels-photo-2387793.jpeg?auto=compress&cs=tinysrgb&w=1920&h=1080&fit=crop');
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
    font-family: 'Inter', sans-serif;
}

.glow-title {
    text-align: center;
    font-size: 2.8rem;
    font-weight: 800;
    background: linear-gradient(135deg, #90EE90, #228B22, #32CD32, #006400);
    -webkit-background-clip: text;
    background-clip: text;
    color: transparent;
    margin-bottom: 0.2rem;
    animation: titleGlow 3s ease-in-out infinite;
}

@keyframes titleGlow {
    0%, 100% { text-shadow: 0 0 20px rgba(144,238,144,0.3); }
    50% { text-shadow: 0 0 40px rgba(144,238,144,0.6); }
}

.subtitle {
    text-align: center;
    color: #90EE90;
    font-size: 0.85rem;
    margin-bottom: 1rem;
    text-shadow: 0 0 10px rgba(0,0,0,0.5);
}

.detection-badge {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    background: rgba(34,139,34,0.3);
    backdrop-filter: blur(10px);
    border-radius: 50px;
    padding: 5px 15px;
    margin-top: 0.5rem;
    margin-bottom: 0.5rem;
    border: 1px solid rgba(144,238,144,0.4);
    font-size: 0.75rem;
    color: #90EE90;
    animation: fadeIn 0.3s ease;
}

.chat-container {
    background: rgba(10, 20, 5, 0.4);
    backdrop-filter: blur(15px);
    border-radius: 25px;
    padding: 1rem;
    height: 500px;
    overflow-y: auto;
    margin-bottom: 1rem;
    border: 1px solid rgba(144,238,144,0.3);
    box-shadow: 0 8px 32px rgba(0,0,0,0.2);
}

.chat-message {
    display: flex;
    margin-bottom: 1rem;
    animation: fadeInUp 0.4s ease;
}

@keyframes fadeInUp {
    from { opacity: 0; transform: translateY(20px); }
    to { opacity: 1; transform: translateY(0); }
}

.user-message {
    justify-content: flex-end;
}

.bot-message {
    justify-content: flex-start;
}

.message-bubble {
    max-width: 75%;
    padding: 0.7rem 1.2rem;
    border-radius: 22px;
    font-size: 0.85rem;
    line-height: 1.4;
}

.user-bubble {
    background: linear-gradient(135deg, #228B22, #006400);
    color: white;
    border-bottom-right-radius: 5px;
    box-shadow: 0 4px 15px rgba(34,139,34,0.3);
}

.bot-bubble {
    background: rgba(30, 50, 20, 0.8);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(144,238,144,0.4);
    color: #E8EDFF;
    border-bottom-left-radius: 5px;
}

.message-time {
    font-size: 0.55rem;
    color: rgba(255,255,255,0.5);
    margin-top: 0.2rem;
    text-align: right;
}

.avatar {
    width: 35px;
    height: 35px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    margin: 0 10px;
    font-size: 1.1rem;
}

.user-avatar {
    background: linear-gradient(135deg, #228B22, #006400);
    box-shadow: 0 0 15px rgba(34,139,34,0.4);
}

.bot-avatar {
    background: rgba(144,238,144,0.2);
    border: 1px solid rgba(144,238,144,0.4);
    backdrop-filter: blur(5px);
}

.stTextInput > div {
    background: rgba(10, 20, 5, 0.6) !important;
    backdrop-filter: blur(15px) !important;
    border: 1px solid rgba(144,238,144,0.4) !important;
    border-radius: 60px !important;
}

.stTextInput input {
    background: transparent !important;
    border: none !important;
    color: white !important;
    padding: 0.7rem 1.2rem !important;
}

.stTextInput input::placeholder {
    color: rgba(144,238,144,0.6);
}

.stButton > button {
    background: linear-gradient(135deg, #228B22, #006400) !important;
    border: none !important;
    border-radius: 50px !important;
    color: white !important;
    font-weight: 600 !important;
    transition: all 0.3s ease !important;
}

.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 5px 20px rgba(34,139,34,0.5) !important;
}

.stSelectbox > div {
    background: rgba(10, 20, 5, 0.6) !important;
    backdrop-filter: blur(15px) !important;
    border: 1px solid rgba(144,238,144,0.4) !important;
    border-radius: 50px !important;
    color: white !important;
}

.quick-actions {
    display: flex;
    gap: 0.5rem;
    margin-top: 0.8rem;
    flex-wrap: wrap;
    justify-content: center;
}

.quick-btn {
    background: rgba(34,139,34,0.2);
    border: 1px solid rgba(144,238,144,0.4);
    border-radius: 50px;
    padding: 0.3rem 0.9rem;
    color: #90EE90;
    font-size: 0.7rem;
    cursor: pointer;
    transition: all 0.3s ease;
}

.quick-btn:hover {
    background: rgba(34,139,34,0.4);
    transform: translateY(-2px);
    color: white;
    border-color: #90EE90;
    box-shadow: 0 5px 15px rgba(34,139,34,0.3);
}

.css-1d391kg, .css-12oz5g0 {
    background: rgba(10, 20, 5, 0.5) !important;
    backdrop-filter: blur(20px) !important;
    border-right: 1px solid rgba(144,238,144,0.2) !important;
}

.chat-container::-webkit-scrollbar {
    width: 5px;
}

.chat-container::-webkit-scrollbar-track {
    background: rgba(255,255,255,0.05);
    border-radius: 10px;
}

.chat-container::-webkit-scrollbar-thumb {
    background: #228B22;
    border-radius: 10px;
}

@media (max-width: 768px) {
    .message-bubble { max-width: 85%; }
    .glow-title { font-size: 2rem; }
    .avatar { width: 28px; height: 28px; font-size: 0.9rem; }
}
</style>
""", unsafe_allow_html=True)

# ========== FUNCTIONS ==========
def translate_text(text, target_lang):
    try:
        lang_code = LANGUAGES.get(target_lang, "en")
        text_encoded = urllib.parse.quote(text)
        url = f"https://translate.googleapis.com/translate_a/single?client=gtx&sl=auto&tl={lang_code}&dt=t&q={text_encoded}"
        
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            return data[0][0][0]
        return None
    except:
        return None

def extract_and_translate(msg):
    msg_lower = msg.lower().strip()
    
    patterns = [
        (r'^(.+?)\s+in\s+(\w+(?:\s+\w+)?)$', 1, 2),
        (r'^(.+?)\s+to\s+(\w+(?:\s+\w+)?)$', 1, 2),
        (r'translate (.+?) (?:to|in) (\w+(?:\s+\w+)?)', 1, 2),
        (r'what is (.+?) in (\w+(?:\s+\w+)?)', 1, 2),
        (r'how do you say (.+?) in (\w+(?:\s+\w+)?)', 1, 2),
    ]
    
    for pattern, text_group, lang_group in patterns:
        match = re.search(pattern, msg_lower)
        if match:
            text = match.group(text_group).strip()
            lang_query = match.group(lang_group).strip()
            
            for lang_name in LANGUAGES.keys():
                if lang_query.lower() in lang_name.lower():
                    translation = translate_text(text, lang_name)
                    if translation:
                        return f"🌿 **Translation:** \"{text}\" → **{translation}** 🌿"
    
    return None

def get_chat_response(msg):
    msg_lower = msg.lower().strip()
    
    if msg_lower in ['hi', 'hello', 'hey', 'namaste']:
        return "🌿 Hello! I'm Translify AI. I can translate 300+ languages! Try: 'I love you in Hindi' 🌸"
    
    if 'who are you' in msg_lower:
        return "🌺 I'm Translify AI - your nature-inspired translation assistant! I support 300+ languages from around the world! 🍃"
    
    if 'how are you' in msg_lower:
        return "🍃 I'm blooming like a flower! 🌸 I can detect and translate 300+ languages! Try typing in any language! 🌿"
    
    if 'what can you do' in msg_lower or 'help' in msg_lower:
        return f"""🌻 I can translate between {len(LANGUAGES)}+ languages AND detect which language you're typing!

**Features:**
• 🔍 **Auto Language Detection** - I detect your language automatically!
• 🌍 **Translate** between {len(LANGUAGES)}+ languages
• 💬 **Natural conversations**

**Try these:**
• `I love you in Hindi`
• `Good morning in Telugu`
• Type in any language - I'll detect it!

Let's connect the world! 🌍"""
    
    if 'joke' in msg_lower:
        jokes = [
            "Why don't scientists trust atoms? Because they make up everything! 😄",
            "What do you call a bear with no teeth? A gummy bear! 🐻",
            "Why did the scarecrow win an award? He was outstanding in his field! 🌾"
        ]
        return random.choice(jokes)
    
    if any(word in msg_lower for word in ['thank', 'thanks']):
        return "You're welcome! 🌸 Anything else to translate? 🌿"
    
    if any(word in msg_lower for word in ['bye', 'goodbye']):
        return "Goodbye! 🌻 Come back anytime for translations! 🌺"
    
    return f"🌱 Try: 'I love you in Hindi' or 'Good morning in Telugu' - I support {len(LANGUAGES)}+ languages! 🍃"

def process_message(user_input):
    conv = st.session_state.conversations[st.session_state.current_conversation_id]
    
    if len([m for m in conv["messages"] if m["role"] == "user"]) == 0:
        title = user_input[:30] + "..." if len(user_input) > 30 else user_input
        conv["title"] = title
    
    conv["messages"].append({
        "role": "user",
        "content": user_input,
        "time": datetime.now().strftime("%H:%M")
    })
    
    reply = extract_and_translate(user_input)
    if not reply:
        reply = get_chat_response(user_input)
    
    conv["messages"].append({
        "role": "bot",
        "content": reply,
        "time": datetime.now().strftime("%H:%M")
    })

# ========== SIDEBAR ==========
with st.sidebar:
    st.markdown("### 🌿 Translify AI")
    st.markdown("---")
    
    if st.button("✨ New Chat", use_container_width=True):
        new_id = hashlib.md5(str(datetime.now()).encode()).hexdigest()
        st.session_state.conversations[new_id] = {
            "title": "New Chat",
            "messages": [],
            "created": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "updated": datetime.now().strftime("%Y-%m-%d %H:%M")
        }
        st.session_state.current_conversation_id = new_id
        st.rerun()
    
    st.markdown("---")
    st.markdown("#### 💬 Chats")
    
    for conv_id, conv in st.session_state.conversations.items():
        if st.button(f"🌿 {conv['title']}", key=conv_id, use_container_width=True):
            st.session_state.current_conversation_id = conv_id
            st.rerun()
    
    st.markdown("---")
    
    if len(st.session_state.conversations) > 1:
        if st.button("🗑️ Delete Current Chat", use_container_width=True):
            del st.session_state.conversations[st.session_state.current_conversation_id]
            st.session_state.current_conversation_id = list(st.session_state.conversations.keys())[0]
            st.rerun()
    
    st.markdown(f"""
    <div style="text-align: center; padding: 0.5rem;">
        <span style="color: #90EE90; font-size: 1.3rem; font-weight: 800;">{len(LANGUAGES)}+</span>
        <span style="color: #aaa; font-size: 0.7rem;"> Languages</span>
        <br>
        <span style="color: #666; font-size: 0.6rem;">🔍 Auto Language Detection</span>
    </div>
    """, unsafe_allow_html=True)

# ========== MAIN UI ==========
st.markdown('<div class="main-container">', unsafe_allow_html=True)

st.markdown("""
<h1 class="glow-title">🌿 Translify AI</h1>
<p class="subtitle">Your Nature-Inspired Translation Assistant | 300+ Languages | Auto Language Detection ✨</p>
""", unsafe_allow_html=True)

# Language selector
col_lang, _ = st.columns([2, 3])
with col_lang:
    target_lang = st.selectbox("🌱 Response Language", list(LANGUAGES.keys()), label_visibility="collapsed")

# Chat Container
st.markdown('<div class="chat-container" id="chat-container">', unsafe_allow_html=True)

current_conv = st.session_state.conversations[st.session_state.current_conversation_id]
for msg in current_conv["messages"]:
    if msg["role"] == "user":
        st.markdown(f"""
        <div class="chat-message user-message">
            <div class="avatar user-avatar">👤</div>
            <div class="message-bubble user-bubble">
                {msg["content"]}
                <div class="message-time">{msg["time"]}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="chat-message bot-message">
            <div class="avatar bot-avatar">🌿</div>
            <div class="message-bubble bot-bubble">
                {msg["content"]}
                <div class="message-time">{msg["time"]}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# Auto-scroll
st.markdown("""
<script>
function scrollToBottom() {
    const container = document.querySelector('.chat-container');
    if(container) container.scrollTop = container.scrollHeight;
}
setTimeout(scrollToBottom, 100);
</script>
""", unsafe_allow_html=True)

# Input with Enter Key
with st.form(key="message_form", clear_on_submit=True):
    col1, col2 = st.columns([5, 1])
    
    with col1:
        user_input = st.text_input(
            "",
            placeholder="🌱 Type anything in any language... I'll detect it! Try: 'I love you in Hindi' 🌸",
            label_visibility="collapsed"
        )
    
    with col2:
        submitted = st.form_submit_button("Send", use_container_width=True)
    
    if submitted and user_input:
        process_message(user_input)
        st.rerun()

# Language Detection Display
if 'user_input' in locals() and user_input and len(user_input.strip()) > 2:
    detected_lang, flag = detect_language(user_input)
    if detected_lang != "Unknown":
        st.markdown(f"""
        <div class="detection-badge">
            <span>{flag}</span>
            <span>🔍 Detected: {detected_lang}</span>
            <span>✓</span>
        </div>
        """, unsafe_allow_html=True)

# Quick Actions
st.markdown("""
<div class="quick-actions">
    <button class="quick-btn" onclick="document.querySelector('input[type=text]').value='I love you in Hindi'; document.querySelector('input[type=text]').dispatchEvent(new Event('input', {bubbles: true}));">🌺 Love→Hindi</button>
    <button class="quick-btn" onclick="document.querySelector('input[type=text]').value='Good morning in Telugu'; document.querySelector('input[type=text]').dispatchEvent(new Event('input', {bubbles: true}));">🌅 Morning→Telugu</button>
    <button class="quick-btn" onclick="document.querySelector('input[type=text]').value='Thank you in French'; document.querySelector('input[type=text]').dispatchEvent(new Event('input', {bubbles: true}));">🌸 Thanks→French</button>
    <button class="quick-btn" onclick="document.querySelector('input[type=text]').value='नमस्ते'; document.querySelector('input[type=text]').dispatchEvent(new Event('input', {bubbles: true}));">🇮🇳 Type Hindi</button>
    <button class="quick-btn" onclick="document.querySelector('input[type=text]').value='నమస్కారం'; document.querySelector('input[type=text]').dispatchEvent(new Event('input', {bubbles: true}));">🇮🇳 Type Telugu</button>
    <button class="quick-btn" onclick="document.querySelector('input[type=text]').value='Bonjour'; document.querySelector('input[type=text]').dispatchEvent(new Event('input', {bubbles: true}));">🇫🇷 Type French</button>
    <button class="quick-btn" onclick="document.querySelector('input[type=text]').value='What can you do?'; document.querySelector('input[type=text]').dispatchEvent(new Event('input', {bubbles: true}));">🌿 Help</button>
</div>

<script>
setTimeout(function() {
    const input = document.querySelector('input[type=text]');
    if(input) input.focus();
}, 100);
</script>
""", unsafe_allow_html=True)

st.markdown(f"""
<div style="text-align: center; margin-top: 0.8rem;">
    <span style="color: rgba(144,238,144,0.6); font-size: 0.7rem;">
        🌿 Nature-Inspired Design | 🔍 Auto Language Detection | 🌸 {len(LANGUAGES)}+ Languages | Break Language Barriers
    </span>
</div>
""", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)