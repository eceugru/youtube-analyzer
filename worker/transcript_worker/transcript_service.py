import yt_dlp
import whisper
import os
from db_service import get_video_transcript, extract_video_id

output_path = "/app/downloads"
cookiesFiles = "/app/cookies.txt"

_whisper_model = None


# --------------------------------------------------
# Whisper modelini 1 kez yükle
# --------------------------------------------------
def load_model_once():
    global _whisper_model
    if _whisper_model is None:
        print("🔊 Whisper modeli yükleniyor...")
        _whisper_model = whisper.load_model("small")
    return _whisper_model


# --------------------------------------------------
# Videodan mp3 indirme
# --------------------------------------------------
def download_audio_as_mp3(url):
    ydl_opts = {
        "format": "140/251/bestaudio/best",
        "outtmpl": f"{output_path}/%(title)s.%(ext)s",
        "cookiefile": cookiesFiles,
        "http_headers": {"User-Agent": "Mozilla/5.0"},
        "extractor_args": {"youtube": {"player_client": ["android"]}},
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192",
        }],
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        fileName = ydl.prepare_filename(info)

    base = os.path.splitext(fileName)[0]
    return base + ".mp3"


# --------------------------------------------------
# Whisper çıktı formatını güvenle çöz
# --------------------------------------------------
def extract_text_from_whisper(result):
    # Whisper bazen string döndürür → direkt dön
    if isinstance(result, str):
        return result

    # Dict ise "text" anahtarı olabilir
    if isinstance(result, dict):
        if "text" in result:
            return result["text"]
        # Bazı sürümlerde alt yapıda 'segments' var
        if "segments" in result:
            return " ".join(seg.get("text", "") for seg in result["segments"])

    # Hiçbiri değilse → tanınmıyor
    raise ValueError(f"Whisper bilinmeyen çıktı formatı: {type(result)}")


# --------------------------------------------------
# Ana transcript çıkarıcı
# --------------------------------------------------
def process_video(url):
    video_id = extract_video_id(url)

    # Eğer DB’de varsa direkt dön (şimdilik pasif)
    existing = False  # get_video_transcript(video_id)
    if existing:
        print(f"📌 {video_id} için transcript ZATEN var → DB’den döndürüldü")
        return existing

    # İndir
    print(f"⬇️ {video_id} indiriliyor...")
    mp3_path = download_audio_as_mp3(url)

    # Transcribe et
    print(f"🎧 {video_id} transcribe ediliyor...")
    model = load_model_once()
    result = model.transcribe(mp3_path)

# Whisper bazen dict, bazen string döndürebiliyor.
    if isinstance(result, dict):
        text = result.get("text", "")
    else:
    # result zaten string ise direkt kullan
        text = str(result)

    return text



# --------------------------------------------------
# İki videoyu karşılaştırmak için
# --------------------------------------------------
def process_videos(urlA, urlB):
    transcriptA = process_video(urlA)
    transcriptB = process_video(urlB)

    return {
        "videoA": {
            "videoId": extract_video_id(urlA),
            "transcript": transcriptA
        },
        "videoB": {
            "videoId": extract_video_id(urlB),
            "transcript": transcriptB
        }
    }


# --------------------------------------------------
# Test
# --------------------------------------------------
if __name__ == "__main__":
    urlA = "https://www.youtube.com/watch?v=0luMwmnvRuQ"
    #urlB = "https://www.youtube.com/watch?v=LXwGSHZXbKs"

    #resultA = process_videos(urlA, urlB)
    
    resultA = process_video(urlA)

    print("\n----- TRANSCRIPT A -----\n")
    print(resultA)
