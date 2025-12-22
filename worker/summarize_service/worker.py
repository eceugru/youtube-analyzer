import pika
import os
import sys
import time
import json
from db_service import get_comments, save_summary, update_job_status
from summarize_service import summarize_comments


# Print'lerin hemen loglara düşmesini sağlar
sys.stdout.reconfigure(line_buffering=True)
os.environ["PYTHONUNBUFFERED"] = "1"

print("🐍 Summarize Worker başlatılıyor...")  # Başlangıç çıktısı
time.sleep(1)


RABBIT_HOST = os.getenv("RABBIT_HOST", "rabbitmq")
QUEUE = "comment.summary.queue"

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host=RABBIT_HOST)
)

channel = connection.channel()
channel.queue_declare(queue=QUEUE, durable=True)


def handle_message(ch, method, properties, body):
    print(f"Yeni video linki alındı: {body.decode('utf-8')}")
    video_url = body.decode('utf-8')
    try:
        print("⚠ try")

        data = json.loads(body)
        videoId = data["videoId"]
        jobId = data["jobId"]
        

        # Database'den yorumların çekilmesi
        commentList = [c["text_en"] for c in get_comments(videoId) if "text_en" in c]
        
        #Yorum özetleme
        videoCommentsSummary = summarize_comments(commentList)
        
        #Özetin kaydedilmesi (Sadece özet alanı alınıyor)
        save_summary(videoId, videoCommentsSummary["summary"])  
        
        # jobState = "DONE"
        update_job_status(jobId, "DONE")
    
        
        ch.basic_ack(delivery_tag=method.delivery_tag)
        
        print("📤 comment.summary.queue kuyruğuna mesaj gönderildi")
        
    except Exception as e:
        print(f"❌ İşlem 😁 hatası: {e}")
        # jobState = "FAILED"
        update_job_status(jobId, "FAILED")
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
    return

print(f" Kuyruk dinleniyor: {QUEUE}")
channel.basic_consume(queue=QUEUE, on_message_callback=handle_message)
channel.start_consuming()

print(" Worker başlatıldı, RabbitMQ bağlantısı kuruldu!")
