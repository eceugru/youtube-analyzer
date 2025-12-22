import json
import requests
import re
from preprocess import preprocess_transcript
from similarity_service import compute_semantic_similarity, compute_tfidf_similarity, compute_keyword_overlap

""" SBERT + TF-IDF + Keyword Overlap ile hesaplanan nicel (sayısal) benzerliği LLaMA 3 gibi bir büyük dil modeline yorumlatmak """

OLLAMA_URL = "http://ollama:11434/api/generate"
MODEL = "llama3"


# ==========================================================
# LLM'e istek atan fonksiyon
# ==========================================================
def call_ollama(prompt: str) -> str:
    payload = {
        "model": MODEL,
        "prompt": prompt,
        "stream": False
    }

    r = requests.post(OLLAMA_URL, json=payload)
    r.raise_for_status()

    return r.json().get("response")


# ==========================================================
# JSON ÇIKTISINI SAĞLIKLI AYIKLAYAN DÜZELTİLMİŞ FONKSİYON
# ==========================================================
def extract_json(response_text: str):
    try:
        start = response_text.index("{")
        end = response_text.rindex("}") + 1
        json_text = response_text[start:end]
        return json.loads(json_text)
    except:
        return {
            "error": "JSON parse failed",
            "raw": response_text
        }



# ==========================================================
# Ana fonksiyon — A + B videolarını analiz eder
# ==========================================================
def compare_with_llm(preA: dict, preB: dict, semantic: float, tfidf: float, overlap: float):

    # ------------------------------------
    # METİNLERİ VE TOKEN/CÜMLELERİ AL
    # ------------------------------------
    textA = preA.get("translated", "")
    tokensA = ", ".join(preA.get("tokens", []))
    sentencesA = "\n".join(preA.get("sentences", []))

    textB = preB.get("translated", "")
    tokensB = ", ".join(preB.get("tokens", []))
    sentencesB = "\n".join(preB.get("sentences", []))

    # ------------------------------------
    # PROMPT — LLM’E GİDEN METİN
    # ------------------------------------
    prompt = f"""
You are an expert analyst in semantic similarity, video comparison and content strategy.

I will give you:
- Semantic similarity score: {semantic}
- TF-IDF similarity score: {tfidf}
- Keyword overlap: {overlap}

Video A Tokens:
{tokensA}

Video B Tokens:
{tokensB}

Video A Sentences:
{sentencesA}

Video B Sentences:
{sentencesB}

Your tasks:
1. Extract the major topics of Video A.
2. Extract the major topics of Video B.
3. Identify similarities between the two videos.
4. Identify differences: what appears ONLY in Video A and ONLY in Video B.
5. Explain why Video B might be more engaging — but do it deeply:
   - Evaluate pacing, emotional tone, humor, storytelling elements
   - Highlight audience retention factors (surprise, relatability, sensory language)
   - Compare how Video B communicates ideas vs. Video A
   - Explain how Video B triggers stronger viewer reactions
   - Mention social media engagement aspects (shareability, comment potential)
6. Provide **5 detailed suggestions** to improve Video A's engagement quality.
7. Decide whether the videos are about the same topic.

IMPORTANT:
✔ Respond ONLY in valid JSON format  
✔ No commentary outside JSON  
✔ JSON must be strictly structured as:

{{
  "topics_videoA": [],
  "topics_videoB": [],
  "unique_to_videoA": [],
  "unique_to_videoB": [],
  "similarities": [],
  "why_videoB_more_engaging": "",
  "recommendations_for_videoA": []
}}

Now produce the JSON.
"""

    # ------------------------------------
    # OLLAMA ÇAĞRISI
    # ------------------------------------
    raw = call_ollama(prompt)

    # ------------------------------------
    # JSON AYIKLA
    # ------------------------------------
    return extract_json(raw)

# ==========================================================
# TEST
# ==========================================================
if __name__ == "__main__":

    rawB = "Yeni iPhone 16 Pro elime ulaştı ve arkadaşlar… telefon resmen benimle dalga geçiyor gibi!Kutuyu açtım, daha ekranı açmadan ‘beni düşürme, pahalıyım’ diye bağırıyor.Kameraya gelirsek… artık bu kadar çok kamera olunca, telefon beni değil ben telefonu çekiyorum.Yeni A18 çipi ise o kadar hızlı ki, sabah alarmı ertelemeye çalıştığımda bile bana ‘hayırdır, tembellik moduna mı geçtin?’ diye tepki veriyor.Ekran 120 Hz zaten yağ gibi akıyor. Kaydırırken kendimi TikTok olimpiyatlarında yarışıyor gibi hissediyorum.Şarj tarafında tam bir efsane: bir gün boyunca elimden düşürmedim, bana mısın demedi.Bu arada USB-C geldi ama Apple “USB-C yaptık ama yine de özeliz” demek ister gibi.Kısacası yeni iPhone 16 Pro: hızlı, havalı ve hafif alaycı.Bu telefon değil, karakterli bir arkadaş gibi. Ama o arkadaşın kredi kartı ekstresini görünce ağlıyorsun işte…"
    rawA = "Bu videoda yeni iPhone 16 Pro’nun donanım ve sistem mimarisini inceliyoruz.Cihaz, Apple’ın A18 Pro işlemcisiyle geliyor. Bu çipte 3 nm üretim teknolojisine sahip 6 çekirdekli CPU, 6 çekirdekli GPU ve optimize edilmiş Neural Engine bulunuyor.Önceki nesle göre CPU performansı %15, GPU tarafında ise %25’e kadar iyileştirme ölçülüyor.Kamera sisteminde 48 MP ana sensör, 1/1.3” sensör boyutu ve yeni bir optik stabilizasyon mimarisi var.Telefoto lens 5x optik yakınlaştırma sunuyor ve foton işleme yazılımı yeniden tasarlanmış durumda.Ekranda LTPO 120 Hz panel kullanılıyor, parlaklık 2.500 nit’e kadar çıkabiliyor.Cihaz USB-C 3.2 standardını destekliyor, böylece 20 Gb/s veri aktarımı mümkün hale geliyor.Batarya tarafında %12 daha yüksek yoğunlukta bir hücre var ve A18 Pro'nun verimliliği ile birlikte testlerde ortalama 1.5 günlük kullanım elde ediliyor.Cihaz genel olarak performans optimizasyonu, kamera algoritmaları ve bağlantı standartları açısından Apple’ın önceki nesline kıyasla ciddi bir mühendislik gelişimi sunuyor."

    preA = preprocess_transcript(rawA)
    preB = preprocess_transcript(rawB)

    semantic = compute_semantic_similarity(preA, preB)
    tfidf = compute_tfidf_similarity(preA, preB)
    overlap = compute_keyword_overlap(preA, preB)

    result = compare_with_llm(preA, preB, semantic, tfidf, overlap)
    print(result)

    
