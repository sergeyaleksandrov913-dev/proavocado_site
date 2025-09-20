// Инициализация карусели
document.addEventListener('DOMContentLoaded', function () {
    const swiper = new Swiper('.products-carousel', {
        loop: true,
        autoplay: {
            delay: 3000,
            disableOnInteraction: false,
        },
        speed: 1200,
        slidesPerView: 1,
        spaceBetween: 20,
        breakpoints: {
            640: { slidesPerView: 2 },
            1024: { slidesPerView: 4 },
        },
        pagination: {
            el: '.swiper-pagination',
            clickable: true,
        },
        navigation: {
            nextEl: '.swiper-button-next',
            prevEl: '.swiper-button-prev',
        },
    });
});

// Функция оформления заказа (заглушка)
function checkout() {
    alert('Переход к оплате... (интеграция с ЮKassa будет здесь)');
    // Здесь будет fetch на /create-payment/
}