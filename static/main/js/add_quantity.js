document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll('.cart-item').forEach(item => {
        const decrementBtn = item.querySelector('.decrement');
        const incrementBtn = item.querySelector('.increment');
        const input = item.querySelector('input[name="product_quantity"]');
        const priceEl = item.querySelector('.item-price');
        const unitPrice = parseFloat(priceEl.dataset.unitPrice); // Берём из атрибута

        function updatePrice() {
            let quantity = parseInt(input.value) || 0;
            priceEl.textContent = `${quantity * unitPrice}$`;
        }

        decrementBtn.addEventListener('click', () => {
            let val = parseInt(input.value) || 0;
            if (val > 1) {
                input.value = val - 1;
                updatePrice();
            }
        });

        incrementBtn.addEventListener('click', () => {
            let val = parseInt(input.value) || 0;
            input.value = val + 1;
            updatePrice();
        });
    });
});
