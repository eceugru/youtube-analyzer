from deep_translator import GoogleTranslator
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from transformers import pipeline
import nltk
import re
import warnings
from langdetect import detect

warnings.filterwarnings("ignore")
from transformers import logging
logging.set_verbosity_error()

# Gerekli indirmeler
nltk.download('vader_lexicon', quiet=True)

# Modelleri yükle
vader = SentimentIntensityAnalyzer()
bert = pipeline("sentiment-analysis",
                model="cardiffnlp/twitter-roberta-base-sentiment-latest")

# ---------------------------------------------------
# Yorumları İngilizce'ye çevir
# ---------------------------------------------------
# Dil kontrolü yapılarak çeviri yapılıyor.
def ceviri(yorumListesi):
    print("🌍 Çeviri kontrolü başlatıldı...")
    translator = GoogleTranslator(source='auto', target='en')
    
    for item in yorumListesi:
        text = item.get('text', '')
        
        if not text:
            continue
        try:
            language = detect(text)
        except Exception:
            language = "Unknown"
        
        if language != "en":
            try:  
                translated = translator.translate(text)
                item['text_en'] = translated
            except Exception as e:
                print(f"⚠️ Çeviri hatası: {e}")
                item['text_en'] = text
        else:
            item['text_en'] = text # Yorum ingilizce ise çeviri yok
    
    return yorumListesi


# ---------------------------------------------------
# Hibrit (VADER + BERT) duygu analizi
# ---------------------------------------------------


MIXED_PAT = re.compile(
    r"\b(but|however|though|although|yet)\b|not\s+(great|good|bad|terrible)|not\s+\w+\s+either",
    re.IGNORECASE
)

def to_tr_label(label: str) -> str:
    lab = label.lower()
    if "pos" in lab: return "Pozitif"
    if "neg" in lab: return "Negatif"
    return "Nötr"

def duygu_analizi_hibrit(yorumListesi):
    for item in yorumListesi:
        text = item.get('text_en')

        # Boşsa atla
        if not text or not isinstance(text, str):
            item['sentiment'] = "Analiz yapılamadı"
            item['score'] = 0
            item['kaynak'] = "None"
            continue

        # pos: pozitif kelimelerin oranı neg: negatif kelimelerin oranı compound: genel duygu skoru (-1 ile +1 arası)
        sc = vader.polarity_scores(text)
        compound, pos, neg = sc['compound'], sc['pos'], sc['neg']

        # Bu satırlar kararsız cümleler içindir
        mixed_cues = (pos > 0.2 and neg > 0.2) or MIXED_PAT.search(text) is not None
        borderline = abs(compound) < 0.4

        try:
            if mixed_cues or borderline:
                #Cümle belirsizse
                r = bert(text)[0]
                item['sentiment'] = to_tr_label(r['label'])
                item['score'] = round(float(r['score']), 3)
                item['kaynak'] = "BERT"
            else:
                # Cümle netse
                if compound >= 0.3:
                    item['sentiment'] = "Pozitif"
                elif compound <= -0.3:
                    item['sentiment'] = "Negatif"
                else:
                    item['sentiment'] = "Nötr"
                item['score'] = round(float(compound), 3)
                item['kaynak'] = "VADER"
        except Exception as e:
            #analiz sırasında hata olursa
            print(f" Analiz hatası: {e} -> {text[:50]}")
            item['sentiment'] = "Analiz yapılamadı"
            item['score'] = 0
            item['kaynak'] = "None"

    return yorumListesi


# ---------------------------------------------------
# Tüm akışı birleştir
# ---------------------------------------------------
def analiz_et(yorum_listesi):
    yorumlar = ceviri(yorum_listesi)
    yorumlar = duygu_analizi_hibrit(yorumlar)
    return yorumlar