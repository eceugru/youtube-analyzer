import pika
import os
import sys
import time
import json
from youtube_service import get_video_comments, extract_video_id
from sentiment_service import analiz_et
from db_service import save_comments, save_video_detail, update_job_status
from video_details import get_video_details


# Print'lerin hemen loglara düşmesini sağlar
sys.stdout.reconfigure(line_buffering=True)
os.environ["PYTHONUNBUFFERED"] = "1"

print("🐍 Worker başlatılıyor...")  # Başlangıç çıktısı
time.sleep(1)


RABBIT_HOST = os.getenv("RABBIT_HOST", "rabbitmq")
RABBIT_PORT = int(os.getenv("RABBIT_PORT", 5672))
RABBIT_USER = os.getenv("RABBIT_USER", "guest")
RABBIT_PASS = os.getenv("RABBIT_PASS", "guest")
QUEUE = os.getenv("QUEUE_NAME", "youtube.comment.link.q")

credentials = pika.PlainCredentials(RABBIT_USER, RABBIT_PASS)
for attempt in range(10):
    try:
        credentials = pika.PlainCredentials(RABBIT_USER, RABBIT_PASS)
        connection = pika.BlockingConnection(pika.ConnectionParameters(
            host=RABBIT_HOST,
            port=RABBIT_PORT,
            credentials=credentials
        ))
        print("✅ RabbitMQ bağlantısı başarılı!")
        break
    except pika.exceptions.AMQPConnectionError:
        print(f"⚠️ RabbitMQ bağlantısı başarısız, {attempt+1}. deneme...")
        time.sleep(5)
else:
    print("❌ RabbitMQ'ya bağlanılamadı, çıkılıyor.")
    exit(1)
    
    

channel = connection.channel()
channel.queue_declare(queue=QUEUE, durable=True)



def handle_message(ch, method, properties, body):
    print(f"Yeni video linki alındı: {body.decode('utf-8')}")
    try:
        # Burada python'na link gelmeli ve videoId'yi kendi bulmalı
        data = json.loads(body)
        jobId = data["jobId"]
        video_url = data["videoUrl"]
        print("⚠ try")

        # url bilgisi ile yorumları çekiyor
        comments  = get_video_comments(video_url, max_comments=1000000)

        # url'den videoId çıkartılıyor
        videoId = extract_video_id(video_url)

        print("👍" + videoId)

        analyzed = analiz_et(comments)

        save_comments(videoId, analyzed)

        print(f"✅ '{videoId}' için {len(analyzed)} yorum işlendi ve kaydedildi.")
        
        videoDetails = get_video_details(videoId)
        
        save_video_detail(videoId, videoDetails)
        
        
        #-----------------------------
        # Summarize service tetikleme
        #-----------------------------
        
        message = json.dumps({"videoId" : videoId, "jobId": jobId})
        
        channel.basic_publish(
            exchange="",
            routing_key="comment.summary.queue",
            body=message,
            properties=pika.BasicProperties(
                delivery_mode=2
            )
        )
        
        print("📤 comment.summary.queue kuyruğuna mesaj gönderildi")

        ch.basic_ack(delivery_tag=method.delivery_tag)

        
    except Exception as e:
        print(f"❌ İşlem 😁 hatası: {e}")
        # jobState = "FAILED"
        update_job_status(jobId, "FAILED")
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
    return

print(f" Kuyruk dinleniyor: {QUEUE}")
channel.basic_consume(queue=QUEUE, on_message_callback=handle_message, auto_ack=False)
channel.start_consuming()

print(" Worker başlatıldı, RabbitMQ bağlantısı kuruldu!")
