from googleapiclient.discovery import build
import os, time

print("youtube başladı")
API_KEY = os.getenv("YOUTUBE_API_KEY")  # Ortam değişkeninden API anahtarı al

if not API_KEY:
    raise ValueError("API anahtarı bulunamadı, .env dosyasını kontrol et!")

print(f"✅ API key bulundu: {API_KEY[:8]}********")

YOUTUBE = build("youtube", "v3", developerKey=API_KEY)



def extract_video_id(video_url):
    """YouTube URL'den video ID'sini ayıklar"""
    video_url = video_url.strip().replace('"', '')
    if "v=" in video_url:
        return video_url.split("v=")[1].split("&")[0]
    elif "youtu.be/" in video_url:
        return video_url.split("youtu.be/")[1].split("?")[0]
    else:
        raise ValueError("Geçersiz YouTube video linki")



def get_video_comments(video_url, max_comments=100, delay=1.0):
    """
    YouTube API'den yorumları sayfalama ile çeker.
    max_comments: maksimum yorum sayısı (ör. 10_000)
    delay: her sayfa arasında bekleme süresi (YouTube API limitleri için)
    """
    video_id = extract_video_id(video_url)
    comments = []
    next_page_token = None
    total_fetched = 0

    print(f" '{video_id}' için yorum çekme işlemi başladı...")

    while True:
        response = YOUTUBE.commentThreads().list(
            part="snippet",
            videoId=video_id,
            maxResults=100,  # YouTube'un izin verdiği maksimum
            pageToken=next_page_token
        ).execute()

        for item in response["items"]:
            yorum = item['snippet']['topLevelComment']['snippet']['textOriginal']
            yazar = item['snippet']['topLevelComment']['snippet']['authorDisplayName']
            like = item['snippet']['topLevelComment']['snippet']['likeCount']
            comments.append({
                'author': yazar,
                'text': yorum,
                'like_count':like
            })
            total_fetched += 1

            if total_fetched >= max_comments:
                print(f" {max_comments} yorum limitine ulaşıldı, durduruluyor.")
                return comments

        # Bir sonraki sayfa varsa devam et
        next_page_token = response.get("nextPageToken")
        if not next_page_token:
            print(" Tüm yorumlar çekildi.")
            break

        # API kotasını aşmamak için bekleme
        time.sleep(delay)

        print(f" {total_fetched} yorum çekildi... devam ediliyor.")

    print(f"Toplam {len(comments)} yorum başarıyla çekildi.")
    return comments

