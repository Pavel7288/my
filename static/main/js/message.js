document.addEventListener("DOMContentLoaded", function () {
    const messages = document.querySelectorAll(".alert-message");
    messages.forEach(message => {
        setTimeout(() => {
            message.classList.add("hide-message");
            setTimeout(() => message.remove(), 1000); // Удаляем элемент после анимации
        }, 5000);
    });
});

