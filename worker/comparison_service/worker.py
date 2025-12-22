import pika
import os
import sys
import time
import json

from comparison_service.db_service import (
    get_video_transcript,
    save_video_comparison,
    update_job_status
)

from comparison_service.preprocess import preprocess_transcript
from comparison_service.similarity_service import (
    compute_semantic_similarity,
    compute_tfidf_similarity,
    compute_keyword_overlap
)
from comparison_service.ollama_service import compare_with_llm


sys.stdout.reconfigure(line_buffering=True)
os.environ["PYTHONUNBUFFERED"] = "1"

print("🤖 Comparison Worker başlıyor...")
time.sleep(1)

# RabbitMQ ayarları
RABBIT_HOST = os.getenv("RABBIT_HOST", "rabbitmq")
QUEUE = "youtube.compare.q"



# RabbitMQ bağlan
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host=RABBIT_HOST)
)
channel = connection.channel()
channel.queue_declare(queue=QUEUE, durable=True)



# -------------------------
# MESAJ GELİNCE ÇALIŞAN KOD
# -------------------------
def handle_message(ch, method, properties, body):

    try:
        data = json.loads(body.decode())

        jobId = data["jobId"]
        videoAId = data["videoAId"]
        videoBId = data["videoBId"]

        print(f"📥 Video A ID: {videoAId}")
        print(f"📥 Video B ID: {videoBId}")

        # DB’den transcriptleri çek
        textA = get_video_transcript(videoAId)
        textB = get_video_transcript(videoBId)

        if not textA or not textB:
            raise ValueError("Transcript bulunamadı! Transcript worker çalışmamış olabilir.")

        # Preprocess
        preA = preprocess_transcript(textA)
        preB = preprocess_transcript(textB)

        # Sayısal benzerlik hesapları
        semantic = compute_semantic_similarity(preA, preB)
        tfidf = compute_tfidf_similarity(preA, preB)
        keyword = compute_keyword_overlap(preA, preB)

        print("🔢 Semantic:", semantic)
        print("📊 TF-IDF:", tfidf)
        print("🔑 Keyword:", keyword)

        # LLM analizi
        llm_result = compare_with_llm(preA, preB, semantic, tfidf, keyword)

        print("🧠 LLM Çıktısı:")
        print(llm_result)

        # DB’ye kaydet
        save_video_comparison(videoAId, videoBId, llm_result)
        
        update_job_status(jobId,"DONE")

        print("💾 Karşılaştırma kaydedildi.")

        ch.basic_ack(delivery_tag=method.delivery_tag)

    except Exception as e:
        print("Comparison Worker Hatası:", e)
        update_job_status(jobId, "FAILED")
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)


print(f"📡 Kuyruk dinleniyor: {QUEUE}")
channel.basic_consume(queue=QUEUE, on_message_callback=handle_message)
channel.start_consuming()
