from pymongo import MongoClient
import os

MONGO_URI = os.getenv("MONGO_URI")

DB_NAME = "YouTube_feedback_intelligence"
COLLECTION_JOB = "analysis-job"

# -----------------------------
# Bağlantı
# -----------------------------
def get_db():
    client = MongoClient(MONGO_URI)
    return client[DB_NAME]



def get_comments(video_id):
    db = get_db()
    collection = db["comments"]
    result = collection.find({"videoId" : video_id})
    return result


def save_summary(videoId, commentsSummary):
    db = get_db()
    collection = db["comments-summary"]

    doc = {
        "videoId" : videoId,
        "summary" : commentsSummary
    }

    res = collection.update_one(
        {"videoId" : videoId},
        {"$set" : doc},
        upsert = True # Bu kritere uyan kayıt varsa güncelle, yoksa yeni bir tane oluştur.
    )
    return 


    print(f"✅ {len(res.inserted_ids)} özet MongoDB'ye kaydedildi ({videoId})")
    return len(res.inserted_ids)

def extract_video_id(video_url):
    """YouTube URL'den video ID'sini ayıklar"""
    video_url = video_url.strip().replace('"', '')
    if "v=" in video_url:
        return video_url.split("v=")[1].split("&")[0]
    elif "youtu.be/" in video_url:
        return video_url.split("youtu.be/")[1].split("?")[0]
    else:
        raise ValueError("Geçersiz YouTube video linki")


def update_job_status(jobId, status):
    db = get_db()
    collection = db[COLLECTION_JOB]
    
    result = collection.update_one(
        {"jobId ":jobId},
        {
            "$set":{
                "status" : status
            }
        }
    )
    return result.modified_count