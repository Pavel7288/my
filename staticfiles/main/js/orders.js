document.addEventListener('DOMContentLoaded', function () {
    const deliverySelect = document.getElementById('id_requires_delivery');
    const deliveryAddressField = document.getElementById('delivery_address_field');

    // Обработчик изменения выбора способа доставки
    deliverySelect.addEventListener('change', function () {
        if (deliverySelect.value === '1') {
            // Если выбрана доставка, показываем поле для ввода адреса
            deliveryAddressField.classList.remove('hidden');
        } else {
            // Если выбрано самовывоз, скрываем поле для ввода адреса
            deliveryAddressField.classList.add('hidden');
        }
    });

    // Изначально проверим, если доставка была выбрана
    if (deliverySelect.value === '1') {
        deliveryAddressField.classList.remove('hidden');
    } else {
        deliveryAddressField.classList.add('hidden');
    }
});
