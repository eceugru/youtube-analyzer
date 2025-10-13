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