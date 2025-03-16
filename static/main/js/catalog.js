document.addEventListener("DOMContentLoaded", function () {
    const select = document.getElementById("categorySelect");
    const products = document.querySelectorAll(".product-card");

    // Обработчик события для изменения категории
    select.addEventListener("change", function () {
        let category = this.value;

        // Фильтрация товаров по выбранной категории
        products.forEach(product => {
            if (category === "all" || product.getAttribute("data-category") === category) {
                product.style.display = "block"; // Показываем товар
            } else {
                product.style.display = "none"; // Скрываем товар
            }
        });
    });
});
