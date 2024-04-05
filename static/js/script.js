const login_form = document.querySelector(".wrapperLogin")
const registrationForm = document.querySelector(".wrapperRegistration")
const loginFormBtns = document.querySelectorAll(".loginShow")
const bannerContent = document.querySelector(".bannerintroContent")

const loginNow = document.querySelector(".loginNow");
const registerNow = document.querySelector(".registerNow");

loginFormBtns.forEach(element => {
    element.addEventListener('click', showForm)
});

registerNow.addEventListener("click", showRegisterForm)
loginNow.addEventListener("click", showForm)
function showForm() {
    login_form.style.display = "block";
    registrationForm.style.display = "none";
    bannerContent.style.display = "none";
}

function showRegisterForm() {
    login_form.style.display = "none";
    registrationForm.style.display = "block";
}