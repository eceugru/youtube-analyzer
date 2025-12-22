from pymongo import MongoClient
import os

# -----------------------------
# MongoDB Ayarları
# -----------------------------
MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = "YouTube_feedback_intelligence"
COLLECTION_NAME = "video-transcrpt"
COLLECTION_NAME_LLM = "video-comparison"
COLLECTION_JOB = "analysis-job"

# -----------------------------
# Bağlantı
# -----------------------------

def get_db():
    client = MongoClient(MONGO_URI)
    return client[DB_NAME]



import re

def extract_video_id(url: str) -> str:
    """
    Normal YouTube + Shorts linklerinden video ID çıkarır.
    Örnek:
      https://www.youtube.com/watch?v=abcd1234
      https://youtu.be/abcd1234
      https://www.youtube.com/shorts/abcd1234
    """

    # 1) Normal watch linki
    match = re.search(r"v=([A-Za-z0-9_-]{11})", url)
    if match:
        return match.group(1)

    # 2) youtu.be kısaltılmış link
    match = re.search(r"youtu\.be/([A-Za-z0-9_-]{11})", url)
    if match:
        return match.group(1)

    # 3) YouTube Shorts linki
    match = re.search(r"youtube\.com/shorts/([A-Za-z0-9_-]{11})", url)
    if match:
        return match.group(1)

    raise ValueError("Geçersiz YouTube video linki")




def save_videos_transcript(videoId, transcript):
    db = get_db()
    collection = db[COLLECTION_NAME]
    result = []
    result.append({
        "videoId": videoId,
        "videoTranscript": transcript
    })
    res = collection.insert_many(result)
    return result

def get_video_transcript(videoId):
    db = get_db()
    collection = db[COLLECTION_NAME]
    result = collection.find({"videoId" : videoId})
    return 


def update_job_status(jobId, status):
    db = get_db()
    collection = db[COLLECTION_JOB]
    
    result = collection.update_one(
        {"jobId":jobId},
        {
            "$set":{
                "status" : status
            }
        }
    )
    return result.modified_count