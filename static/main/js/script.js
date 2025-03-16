document.addEventListener("DOMContentLoaded", function () {
    function fadeInText(element, speed = 15) {
        const text = element.textContent;
        element.textContent = ""; // Очищаем оригинальный текст

        text.split("").forEach((char, index) => {
            const span = document.createElement("span");
            span.textContent = char;
            span.style.opacity = "0";
            element.appendChild(span);

            setTimeout(() => {
                span.style.opacity = "1";
            }, index * speed);
        });
    }

    // Обрабатываем все элементы с классом fade-text
    document.querySelectorAll(".fade-text").forEach((element, idx) => {
        element.style.visibility = "hidden"; // Делаем текст невидимым, но он остается на месте

        setTimeout(() => {
            element.style.visibility = "visible"; // Показываем элемент
            fadeInText(element);
        }, idx * 500); // Задержка между строками
    });
});