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
})

document.getElementById("signpu").addEventListener("click", () =>{
    window.location.href = "/register.html"
})

async function loginUser(){
    event.preventDefault();

    const email = document.getElementById("email").value
    const password = document.getElementById("password").value
    const rememberMe = document.getElementById("rememberMe").checked

    const response = await fetch("http://localhost:8080/api/users/signIn",{
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({email, password})
    });

    if(response.ok){
        const user = await response.json();

        //kullanıcı bilgileri
        localStorage.setItem("user", JSON.stringify(user));
        if(rememberMe){
            localStorage.setItem("rememberMeEmail",email);
            localStorage.setItem("rememberMePassword", password);
            localStorage.setItem("rememberMe","true");
        }else{
            localStorage.removeItem("rememberMeEmail");
            localStorage.removeItem("rememberMePassword");
            localStorage.setItem("rememberMe","false");
        }

        //ana sayfaya yönlendir
        window.location.href="/index.html";
    }else{
        const message = await response.text();
        alert("Giriş başarısız: " + message);
    }
}

window.addEventListener("DOMContentLoaded", ()=>{
    const rememberMe = localStorage.getItem("rememberMe") === "true";
    const savedEmail = localStorage.getItem("rememberMeEmail");
    const savedPassword = localStorage.getItem("rememberMePassword");

    if(rememberMe && savedPassword && savedEmail){
        document.getElementById("email").value = savedEmail;
        document.getElementById("password").value = savedPassword;
    }
});

