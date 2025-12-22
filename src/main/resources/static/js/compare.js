const startBtn = document.getElementById("startCompare");
const loader = document.getElementById("loader");
const resultDiv = document.getElementById("result");
const resultText = document.getElementById("comparisonText");

let intervalId = null;

startBtn.addEventListener("click", async () => {
    const urlA = document.getElementById("urlA").value;
    const urlB = document.getElementById("urlB").value;

    if (!urlA || !urlB) {
        alert("İki video linkini giriniz");
        return;
    }

    loader.style.display = "block";

    const res = await fetch("http://localhost:8080/api/compare/start", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ urlA, urlB })
    });

    const data = await res.json();
    const jobId = data.jobId;

    intervalId = setInterval(() => checkStatus(jobId), 3000);
});

async function checkStatus(jobId) {
    const res = await fetch(`http://localhost:8080/api/jobs/${jobId}`);
    const job = await res.json();

    if (job.status === "DONE") {
        clearInterval(intervalId);
        loadResult(jobId);
    }

    if (job.status === "FAILED") {
        clearInterval(intervalId);
        loader.innerText = "Karşılaştırma başarısız oldu";
    }
}

async function loadResult(jobId) {
    loader.style.display = "none";
    resultDiv.style.display = "block";

    // burada comparison sonucu MongoDB’den dönen endpoint olacak
    const res = await fetch(`http://localhost:8080/api/compare/results/${jobId}`);
    const data = await res.json();

    resultText.textContent = data.why_videoB_more_engaging;
}
