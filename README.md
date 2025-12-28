# 🎥 YouTube Feedback Intelligence System

YouTube videolarına ait yorumları ve video transkriptlerini analiz ederek  
içerik üreticilerine **somut, veriye dayalı geri bildirimler** sunan uçtan uca bir analiz ve öneri sistemidir.

Bu proje, bitirme projesi kapsamında **gerçek dünya problemini** çözmeye odaklanarak geliştirilmiştir.

---

## 🚀 Projenin Amacı

İçerik üreticileri genellikle:
- Binlerce yorumu tek tek okuyamaz,
- İzleyici duygusunu net biçimde ölçemez,
- Videolarının hangi konularda eksik kaldığını fark edemez.

Bu sistem:
- Yorumları analiz eder,
- Uzun yorum listelerini özetler,
- Video transkriptlerini benzer videolarla karşılaştırır,
- Ve **iyileştirme önerileri üretir**.

---

## 🧠 Sistem Neler Yapıyor?

- 📊 **Yorum Duygu Analizi**
  - Pozitif / Negatif / Nötr sınıflandırma

- 📝 **Otomatik Yorum Özetleme**
  - Yüzlerce yorumu ana fikir haline getirir

- 🎙 **Video Transkript Çıkarma**
  - Videonun sesi metne dönüştürülür

- 🔍 **Benzer Video Karşılaştırması**
  - İçerikte eksik veya zayıf işlenen konular tespit edilir

- 💡 **İçerik Öneri Sistemi**
  - Analiz sonuçlarına göre geliştiriciye öneriler sunulur

- 📈 **Dashboard**
  - Tüm sonuçlar kullanıcı dostu bir arayüzde gösterilir

---

## 🛠 Kullanılan Teknolojiler

### Backend
- Java Spring Boot
- RESTful API

### Frontend
- HTML, CSS, JavaScript

### Veritabanı
- MongoDB (NoSQL)

### NLP & AI
- Duygu Analizi:  
  - NLTK VADER  
  - TextBlob  
  - BERT (Hugging Face)

- Yorum Özetleme:  
  - TextRank  
  - LLaMA 3 (Hybrid yaklaşım)

- Transkript Çıkarma:  
  - OpenAI Whisper

- Video Karşılaştırma:  
  - TF-IDF  
  - Cosine Similarity  
  - Sentence-BERT

---

## 🧩 Sistem Mimarisi (Özet)

1. Kullanıcı video linkini girer  
2. Yorumlar ve transkriptler otomatik çekilir  
3. NLP servisleri analizleri gerçekleştirir  
4. Sonuçlar MongoDB’de saklanır  
5. Dashboard üzerinden görselleştirilir  

---

## 📌 Beklenen Çıktılar

- Yorumların duygu dağılımı
- Otomatik oluşturulmuş yorum özeti
- Benzer videolarla içerik karşılaştırması
- İçerik geliştirme önerileri
- MongoDB’de saklanan analiz verileri

---

## 👤 Kullanıcı Senaryosu

1. Kullanıcı video linkini girer  
2. Sistem yorumları otomatik çeker  
3. Yorumlar analiz edilir ve özetlenir  
4. Video transkripti oluşturulur  
5. Benzer videolarla kıyaslama yapılır  
6. Kullanıcıya geliştirme önerileri sunulur  

