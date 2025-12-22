"""
İki videonun sayısal olarak ne kadar benzediğini hesaplayan modül.
"""

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from embedder import embed_two_texts 
from preprocess import preprocess_transcript  


# ==========================================================
# 1) SEMANTIC SIMILARITY (SBERT)
# ==========================================================

def compute_semantic_similarity(preA: dict, preB: dict) -> float:
    """
    SBERT semantic similarity.
    SBERT'e clean_text değil, translated tam cümle verilmelidir.
    """

    textA = preA.get("translated")
    textB = preB.get("translated")
    print("textA : ",textA)
    print("textB : ",textB)
    

    vecA, vecB = embed_two_texts(textA, textB)

    cosine = np.dot(vecA, vecB) / (np.linalg.norm(vecA) * np.linalg.norm(vecB))
    return float(cosine)


# ==========================================================
# 2) TF-IDF SIMILARITY
# ==========================================================

def compute_tfidf_similarity(preA: dict, preB: dict) -> float:
    textA = preA.get("clean_text", "")
    textB = preB.get("clean_text", "")

    if not textA.strip() or not textB.strip():
        return 0.0

    vectorizer = TfidfVectorizer()
    matrix = vectorizer.fit_transform([textA, textB])

    a = matrix[0].toarray()[0]
    b = matrix[1].toarray()[0]

    cosine = np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))
    return float(cosine)


# ==========================================================
# 3) KEYWORD OVERLAP
# ==========================================================
""" ortak kullandığı kavramlar,konu başlıkları birbirine yakınsa videolar içerik olarak benzer sayılır. """
def compute_keyword_overlap(preA: dict, preB: dict) -> float:
    tokensA = set(preA.get("tokens", []))
    tokensB = set(preB.get("tokens", []))

    if not tokensA or not tokensB:
        return 0.0

    #Jaccard Similarity
    inter = len(tokensA.intersection(tokensB)) #ortak kullandığı anahtar kelime sayısı
    union = len(tokensA.union(tokensB)) #toplam benzersiz kelime havuzu

    return inter / union




# ==========================================================
# 4) ANA METOT
# ==========================================================

def compare_videos(preA: dict, preB: dict) -> dict:
    semantic = compute_semantic_similarity(preA, preB)
    tfidf = compute_tfidf_similarity(preA, preB)
    overlap = compute_keyword_overlap(preA, preB)

    return {
        "semantic_similarity": semantic,
        "tfidf_similarity": tfidf,
        "keyword_overlap": overlap,
    }


# ==========================================================
# 5) TEST
# ==========================================================

if __name__ == "__main__":
    print("\n🚀 SIMILARITY TEST\n")

    

    rawA = "Employees quickly adopted the newly introduced AI system."
    rawB = "The staff began using the new AI platform rapidly after it was deployed."

    preA = preprocess_transcript(rawA)
    preB = preprocess_transcript(rawB)

    result = compare_videos(preA, preB)

    # Dikkate alınacak metrik 
    print(result.get("semantic_similarity"))   


"""
| Cosine Similarity | Anlam                           |
| ----------------- | ------------------------------- |
| 0.90 – 1.00       | *Neredeyse aynı cümle*          |
| 0.75 – 0.90       | *Aynı bağlam / çok yakın anlam* |
| 0.60 – 0.75       | *Anlamsal olarak benzer*        |
| 0.45 – 0.60       | *İlişkili ama zayıf benzerlik*  |
| < 0.45            | *Benzerlik düşük*               |

"""