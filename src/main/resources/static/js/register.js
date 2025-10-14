const themeToggle = document.getElementById("themeToggle");
const body = document.body;
const savedTheme = localStorage.getItem("theme");
if (savedTheme === "light") {
    body.classList.add("light");
    themeToggle.textContent = "☀️";
}
themeToggle.addEventListener("click", () => {
    body.classList.toggle("light");
    const isLight = body.classList.contains("light");
    themeToggle.textContent = isLight ? "☀️" : "🌙";
    localStorage.setItem("theme", isLight ? "light" : "dark");
});



const apiurl = "http://localhost:8080/api/users"

async function addUser(){
    event.preventDefault(); // sayfanın yenilenmesini engeller

    const firstName = document.getElementById("firstName").value;
    const lastName = document.getElementById("lastName").value;
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;

    const response = await fetch ("http://localhost:8080/api/users/signUp" ,{
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({firstName, lastName, email, password})
    })

    if (response.ok) {
        console.log("Kullanıcı başarıyla eklendi!");
    } else {
        console.error("Bir hata oluştu:", response.status);
    }
};

// for sign in button
document.getElementById("signIn").addEventListener("click", () => {
    window.location.href = "/login.html";
});

// for sign up button
document.getElementById("signUp").addEventListener("click", () => {
    window.location.href = "/register.html";
});

// for logo button
document.getElementById("logo").addEventListener("click", () => {
    window.location.href = "/index.html";
});

document.getElementById("signnI").addEventListener("click", () =>{
    window.location.href ="/login.html";
});
