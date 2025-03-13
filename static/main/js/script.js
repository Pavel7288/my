document.addEventListener("DOMContentLoaded", function () {
    function typeText(element, text, speed = 50, callback = null) {
        let index = 0;
        element.innerHTML = ""; // Очищаем текст перед печатью
        element.style.visibility = "visible"; // Показываем элемент

        function type() {
            if (index < text.length) {
                element.innerHTML += text[index];
                index++;
                setTimeout(type, speed);
            } else if (callback) {
                setTimeout(callback, 300); // Пауза перед следующим элементом
            }
        }

        type();
    }

    const elements = document.querySelectorAll(".fade-text");

    let texts = []; // Сохраняем оригинальные тексты
    elements.forEach(el => {
        texts.push(el.innerText.trim()); // Сохраняем текст перед скрытием
        el.innerHTML = ""; // Очищаем контент
        el.style.visibility = "hidden"; // Скрываем перед началом
    });

    function processElements(index = 0) {
        if (index < elements.length) {
            const el = elements[index];
            el.style.visibility = "visible"; // Показываем перед печатью
            typeText(el, texts[index], 20, () => processElements(index + 1));
        }
    }

    processElements();
});