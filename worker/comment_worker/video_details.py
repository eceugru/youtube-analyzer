import requests
import os

API_KEY = os.getenv("YOUTUBE_API_KEY")

if not API_KEY:
    raise ValueError("API anahtarı bulunamadı, .env dosyasını kontrol et!")

url = 'https://www.googleapis.com/youtube/v3/videos'

print(f"✅ API key bulundu: {API_KEY[:8]}********")


video_detail = []

def get_video_details( video_id):
    params_1 = {
        'part': 'snippet',
        'id' : video_id,
        'key': API_KEY
    }

    params_2 = {
        'part': 'statistics',
        'id': video_id,
        'key': API_KEY
    }

    r_2 = requests.get(url, params_2)
    data_2 = r_2.json()


    r_1 = requests.get(url,params_1)
    data = r_1.json()

    video_detail.append({
        'channelTitle': data['items'][0]['snippet']['channelTitle'],
        'title': data['items'][0]['snippet']['title'],
        'viewCount': data_2['items'][0]['statistics']['viewCount'],
        'likeCount':data_2['items'][0]['statistics']['likeCount']
    })

    return video_detail

