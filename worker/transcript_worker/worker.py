import pika
import os
import sys
import time
import json
from transcript_service import process_video
from db_service import save_videos_transcript, extract_video_id, update_job_status


# Print'lerin hemen loglara düşmesini sağlar
sys.stdout.reconfigure(line_buffering=True)
os.environ["PYTHONUNBUFFERED"] = "1"

# Başlangıç çıktısı
print("🐍 Transcript Worker başlatılıyor...")  
time.sleep(1)

# Rabbitmq kuyruk bilgileri
RABBIT_HOST = os.getenv("RABBIT_HOST", "rabbitmq")
TRANSCRIPT_QUEUE = "youtube.transcript.compare.q"
COMPARE_QUEUE = "youtube.compare.q"

    
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host=RABBIT_HOST)
)
channel = connection.channel()
channel.queue_declare(queue=TRANSCRIPT_QUEUE, durable=True)
channel.queue_declare(queue=COMPARE_QUEUE, durable=True)


def handle_message(ch, method, properties, body):
     
    try:
        data = json.loads(body.decode())
        
        jobId = data["jobId"]
        urlA = data["urlA"]
        urlB = data["urlB"]
        
        print("📥 Transcript job alındı")
        print("A:", urlA)
        print("B:", urlB)
        
        # ---- Video A ----
        # url bilgisinden videoId çıkartma
        videoAId = extract_video_id(urlA)
        transcriptA = process_video(urlA)
        save_videos_transcript(videoAId, transcriptA)
        
        # ---- Video B ----
        # url bilgisinden videoId çıkartma
        videoBId = extract_video_id(urlB)
        transcriptB = process_video(urlB)
        save_videos_transcript(videoBId, transcriptB)
        
        print("✅ Transcriptler kaydedildi")
        
        
        # ---- Comparison worker'ı tetikle ----
        message = json.dumps({
            "jobId":jobId,
            "videoAId": videoAId,
            "videoBId" : videoBId
        })
        
        channel.basic_publish(
            exchange="",
            routing_key=COMPARE_QUEUE,
            body=message,
            properties=pika.BasicProperties(delivery_mode=3)
        )
        
        print("📤 Comparison kuyruğu tetiklendi")
        
        ch.basic_ack(delivery_tag=method.delivery_tag)
        
    except Exception as e:
        print(f"❌ Transcript Worker Hatası: {e}")
        
        update_job_status(jobId, "FAILED")
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
    return

print(f" Kuyruk dinleniyor: {TRANSCRIPT_QUEUE}")
channel.basic_consume(queue=TRANSCRIPT_QUEUE, on_message_callback=handle_message, auto_ack=False)
channel.start_consuming()
print(" Worker başlatıldı, RabbitMQ bağlantısı kuruldu!")

    