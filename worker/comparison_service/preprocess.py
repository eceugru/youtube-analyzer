""" Bu dosya transcript'in “ham metin” olmaktan çıkıp analize hazır  bir metne dönüşmesini sağlar. """

import re
import unicodedata
from typing import Dict, List
from deep_translator import GoogleTranslator
from langdetect import detect, LangDetectException


# =========================
# Dil tespiti
# =========================
""" Whisper her zaman doğru dilde transkript dökmeyebilir. Kullanıcı Türkçe video yükleyebilir, 
İngilizce olabilir, karışık olabilir.Video hangi dildeyse çeviri modülüne doğru dil bilgisini vermek gerekir."""

def detect_language(text: str) -> str:
    """Transcript dilini tespit eder. Hata olursa İngilizce kabul edelim."""
    try:
        return detect(text)
    except LangDetectException:
        return "en"


# =========================
# Çeviri - GoogleTranslator
# =========================

def translate_to_english(text: str, source_lang: str) -> str:
    """
    Metni İngilizce'ye çevirir. deep_translator GoogleTranslator kullanır.

    """
    if source_lang == "en":
        return text

    # GoogleTranslator tek parçada çevirirken bazen timeout / request broken verir.
    lines = text.split("\n")
    translated_lines = []

    for line in lines:
        if not line.strip():
            continue

        try:
            translated = GoogleTranslator(source=source_lang, target="en").translate(line)
            translated_lines.append(translated)

        except Exception as e:
            print(f"⚠️ Translation error on line: {e}")
            #arada hata verebilir tüm metnin çökmesini istenmez bozuk olsa bile bir çıktı verir
            translated_lines.append(line)

    return " ".join(translated_lines)
    

# =========================
# Temizleme
# =========================

URL_PATTERN = re.compile(r"http\S+|www\.\S+")
HTML_PATTERN = re.compile(r"<.*?>")
EMOJI_PATTERN = re.compile("[\U0001F600-\U0001F64F"
                           "\U0001F300-\U0001F5FF"
                           "\U0001F680-\U0001F6FF"
                           "\U0001F1E0-\U0001F1FF]+")


def clean_text_basic(text: str) -> str:
    """Lowercase, link/emoji/html temizliği, noktalama temizleme."""
    text = text.lower()
    text = URL_PATTERN.sub(" ", text)
    text = HTML_PATTERN.sub(" ", text)
    text = EMOJI_PATTERN.sub(" ", text)
    text = re.sub(r"[^\w\s]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


# =========================
# Tokenization & sentences
# =========================

def split_sentences(text: str) -> List[str]:
    #videonun hangi kısımlarının eksik olduğu, hangi konuların yüzeysel anlatıldığı gibi
    # çıkarımları cümle bazlı analizle yapıyor.

    sentences = re.split(r"(?<=[.!?])\s+", text)
    return [s.strip() for s in sentences if s.strip()]


def tokenize(text: str) -> List[str]:
    return [t for t in text.split() if t.strip()]


# =========================
# Stopword + Lemma
# =========================

EN_STOPWORDS = {
    "the","a","an","and","or","but","if","then","else","is","am","are","was","were",
    "be","being","been","this","that","these","those","it","its","of","for","to","in",
    "on","at","by","with","from","as","about","into","through","over","after","before",
    "up","down","out","off","again","further","once","here","there","so","than","too",
    "very","can","could","should","would","will","just","not","no","nor","do","does",
    "did","have","has","had","i","you","he","she","we","they","them","their","our",
    "your"
}


def remove_stopwords(tokens: List[str]) -> List[str]:
    return [t for t in tokens if t not in EN_STOPWORDS]


def simple_lemmatize(tokens: List[str]) -> List[str]:
    lemmas = []
    for t in tokens:
        if t.endswith("ing") and len(t) > 4:
            lemmas.append(t[:-3])
        elif t.endswith("ed") and len(t) > 3:
            lemmas.append(t[:-2])
        elif t.endswith("s") and len(t) > 3:
            lemmas.append(t[:-1])
        else:
            lemmas.append(t)
    return lemmas


# =========================
# FULL PREPROCESS PIPELINE
# =========================

def preprocess_transcript(raw: str) -> Dict:
    if not raw.strip():
        return {
            "original_text": raw,
            "translated": "",
            "clean_text": "",
            "sentences": [],
            "tokens": []
        }

    # 1) Dil tespiti
    lang = detect_language(raw)

    # 2) İngilizceye çeviri → her zaman normalize edilmiş hale getirmek istiyorsun
    translated = translate_to_english(raw, lang)

    # 3) Temizleme
    clean = clean_text_basic(translated)

    # 4) Cümleler
    sentences = split_sentences(translated)

    # 5) Tokenization + stopword + lemma
    tokens = tokenize(clean)
    tokens = remove_stopwords(tokens)
    tokens = simple_lemmatize(tokens)

    final_clean_text = " ".join(tokens)

    return {
        "original_text": raw,
        "language": lang,
        "translated": translated,
        "clean_text": final_clean_text,
        "sentences": sentences,
        "tokens": tokens
    }


def preprocess_pair(textA: str, textB: str) -> Dict:
    return {
        "videoA": preprocess_transcript(textA),
        "videoB": preprocess_transcript(textB)
    }


