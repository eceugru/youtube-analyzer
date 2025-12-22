"""Bu dosya, transkript karşılaştırması için gerekli olan anlamsal (semantic) embedding vektörlerini oluşturur. """

from sentence_transformers import SentenceTransformer
import numpy as np

_sbert_model = None


def load_sbert_once():
    global _sbert_model
    if _sbert_model is None:
        print("🧬 SBERT modeli yükleniyor...")
        _sbert_model = SentenceTransformer("sentence-transformers/paraphrase-mpnet-base-v2")
    return _sbert_model


# ==========================================================
# 1) Tek metin embed
# ==========================================================
def embed_text(text: str):
    """
    SBERT'e direkt string verilir.
    """
    model = load_sbert_once()
    vector = model.encode(text) #768 boyutlu vector
    return np.array(vector)


# ==========================================================
# 2) İki metni embed et
# ==========================================================
def embed_two_texts(textA: str, textB: str):
    """
    Semantic similarity için iki metni aynı anda encode eder.
    """
    model = load_sbert_once()
    vectors = model.encode([textA, textB])

    vecA = np.array(vectors[0])
    vecB = np.array(vectors[1])

    return vecA, vecB



# ==========================================================
# TEST BLOKU
# ==========================================================
if __name__ == "__main__":
    print("🚀 EMBEDDER TEST BAŞLATILDI")

    textA = "The company introduced a new AI strategy."
    textB = "A new AI plan was deployed in the organization."

    vecA, vecB = embed_two_texts(textA, textB)

    print("vector A:", vecA.shape)
    print("vector B:", vecB.shape)

    cosine = np.dot(vecA, vecB) / (np.linalg.norm(vecA) * np.linalg.norm(vecB))
    print("cosine:", cosine)
