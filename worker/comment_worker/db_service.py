from pymongo import MongoClient

# -----------------------------
# MongoDB Ayarları
# -----------------------------
MONGO_URI = "mongodb://mongodb:27017/"
DB_NAME = "YouTube_feedback_intelligence"
COLLECTION_NAME = "comments"

# -----------------------------
# Bağlantı
# -----------------------------

def get_db():
    client = MongoClient(MONGO_URI)
    return client[DB_NAME]

# -----------------------------
# Yorumları kaydet
# -----------------------------

def save_comments(video_id, yorumListesi):
    if not yorumListesi:
        print("Kaydedilecek yorum bulunamadı.")
        return 0

    db = get_db()
    collection = db[COLLECTION_NAME]

    formatted = []
    for y in yorumListesi:
        formatted.append({
            "videoId": video_id,
            "author": y.get("author"),
            "text": y.get("text"),
            "text_en": y.get("text_en"),
            "sentiment": y.get("sentiment"),
            "score": y.get("score"),
            "kaynak": y.get("kaynak"),
            "like_count": y.get("like_count"),
            "publishedAt": y.get("date")
        })
    res = collection.insert_many(formatted, ordered = False)
    print(f"✅ {len(res.inserted_ids)} yorum MongoDB'ye kaydedildi ({video_id})")
    return len(res.inserted_ids)

def get_comments(video_id):
    db = get_db()
    collection = db["comments"]
    result = collection.find({"videoId" : video_id})
    return result

def save_summary(videoId, commentsSummary):
    db = get_db()
    collection = db["comments-summary"]
    result = []
    result.append({
        "videoId" : videoId,
        "videoCommetsSummary" : commentsSummary
    })
    res = collection.insert_many(result, ordered = False)

    print(f"✅ {len(res.inserted_ids)} özet MongoDB'ye kaydedildi ({videoId})")
    return len(res.inserted_ids)





