// serviceden sonuç gelene kadar yapılan işlemler

const jobId = localStorage.getItem("jobId");

if(!jobId){
    alert("job bulunamadı");
    window.location.href = "/";
}

// ================================
// HTML ELEMENTLERİ
// ================================
const loadingDiv = document.getElementById("loading");
const resultDiv  = document.getElementById("results");

const summaryText     = document.getElementById("summaryText");
const positiveCountEl = document.getElementById("positiveCount");
const neutralCountEl  = document.getElementById("neutralCount");
const negativeCountEl = document.getElementById("negativeCount");
const commentsListEl  = document.getElementById("commentsList");

let intervalId = null;

async function checkJobStatus() {
    try{
        // Bu job bitti mi? / job ıd'si ile eşleşen job alır
        const response = await fetch(`http://localhost:8080/api/jobs/results/${jobId}`);

        if(!response.ok){
            console.error("Job status alınamadı");
            return;
        }
    
        const job = await response.json();

        // Eğer status RUNNİNG ise hiç bir şey olmaz fonksiyon bitter ve 3 saniye sonra tekrar sorulur ve loader dönmeye devam eder
        if(job.status == "DONE"){
            clearInterval(intervalId);
            loadResult();
        }

        if (job.status === "FAILED") {
            clearInterval(intervalId);
            loadingDiv.innerHTML = "<h2>Analiz başarısız oldu</h2>";
        }

    }catch (err){
        console.error("Job kontrol hatası:", err);
    }
    
    
}

// ================================
// SONUÇLARI ÇEK
// ================================

async function loadResult() {
    try {
        // Sonuçları getir ve ekrana bas
    
        // “Backend’den gelen cevabı al ve JavaScript nesnesine çevir.”
        const response = await fetch(`http://localhost:8080/api/results/${jobId}`);

        if(!response.ok){
            console.error("sonuç alınamadı.");
            return;
        }

        const data = await response.json();

        // Loader kapat, sonuç aç
        loadingDiv.style.display = "none";
        resultDiv.style.display  = "block";
        renderResult(data);
        
    } catch (error) {
        console.error("Sonuç yükleme hatası:", error);
    }
    

}



// ================================
// EKRANA BASMA
// ================================

function renderResult(data) {
    // Özet
    summaryText.textContent = data.summary || "Özet bulunamadı.";

    // Sentiment
    positiveCountEl.textContent = data.positiveCount ?? 0;
    negativeCountEl.textContent = data.negativeCount ?? 0;
    neutralCountEl.textContent = data.neutralCount ?? 0;

    const sentimentClass = comment.sentiment.toLowerCase();

    // Yorumlar
    commentsListEl.innerHTML="";
    data.comments.forEach(comment => {
        const div = document.createElement("div");
        div.className = "comment";

        div.innerHTML = `
            <strong>${comment.author}</strong>
            <p>${comment.text}</p>
            <small class="${sentimentClass}">
                 ${comment.sentiment}
            </small>
        `;

        commentsListEl.appendChild(div);
    });
}

// ================================
// POLLING BAŞLAT
// ================================
// checkJobStatus fonksiyonunu 3 saniyede bir çalıştırır
intervalId = setInterval(checkJobStatus, 3000);


// ================================
// KARŞILAŞTIRMA BUTTONU
// ================================

document.getElementById("goCompare").addEventListener("click", () => {
    window.location.href = "/compare.html";
});



