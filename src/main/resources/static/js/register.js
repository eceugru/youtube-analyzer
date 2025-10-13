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
    const FirstName = document.getElementById("firstName").value;
    const LastName = document.getElementById("lastName").value;
    const EmailAddress = document.getElementById("emailAddress").value;
    const Password = document.getElementById("password").value;

    await fetch ("http://localhost:8080/api/users/login" ,{
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({FirstName, LastName, EmailAddress, Password})
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
})