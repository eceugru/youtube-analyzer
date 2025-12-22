import networkx as nx
import requests
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import os

LLAMA_HOST = os.getenv("LLAMA_HOST", "http://ollama:11434")

def simple_sentence_split(text):
    """Basit ama etkili bir cümle bölücü (nokta, ünlem, soru işareti üzerinden)."""
    sentences = []
    for s in text.replace("!", ".").replace("?", ".").split("."):
        s = s.strip()
        if len(s) > 3:  # çok kısa cümleleri ele
            sentences.append(s)
    return sentences
 
#------------------------
# Yorum özeti çıkarma 
#------------------------
def summarize_comments(comments, top_k=5, max_chars=2000, llama_host=LLAMA_HOST):
    """
    Yorum listesini (İngilizce) alır, TextRank + Llama3 ile özet döndürür.
    """
    # --- 1️⃣ TextRank (extractive) ---
    text = " ".join(c.strip() for c in comments if c and isinstance(c, str))
    text = text[:max_chars]

    sentences = simple_sentence_split(text)
    if not sentences:
        return {"summary": "", "selected_sentences": [], "scores": {}}

    vectorizer = TfidfVectorizer(stop_words="english")
    X = vectorizer.fit_transform(sentences)
    sim = cosine_similarity(X)

    nx_graph = nx.from_numpy_array(sim)
    scores = nx.pagerank(nx_graph)

    ranked = sorted(((scores[i], s) for i, s in enumerate(sentences)), reverse=True)

    selected = [s for _, s in ranked[:top_k]]
    score_map = {sentences[i]: float(scores[i]) for i in range(len(sentences))}

    # --- 2️⃣ Llama3 (abstractive) ---
    joined = "\n- " + "\n- ".join(selected)
    prompt = (
        "Summarize the following YouTube comments into a short, natural English paragraph. "
        "Focus on main ideas, emotions, and suggestions:\n"
        f"{joined}\n\nSummary:"
    )

    payload = {
        "model": "llama3",
        "prompt": prompt,
        "stream": False,
        "options": {"temperature": 0.3, "num_predict": 256}
    }

    try:
        r = requests.post(f"{llama_host}/api/generate", json=payload, timeout=120)
        r.raise_for_status()
        data = r.json()
        summary = data.get("response", "").strip()
    except Exception as e:
        summary = f"[Llama3 error: {e}]"

    return {"summary": summary}
