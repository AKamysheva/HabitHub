// Скрипт для мобильного меню
document.addEventListener('DOMContentLoaded', function () {
    const header = document.querySelector('header');
    const burgerMenu = document.createElement('div');
    burgerMenu.className = 'burger-menu';
    burgerMenu.innerHTML = '<span></span><span></span><span></span>';
    header.insertBefore(burgerMenu, header.querySelector('.header_first'));

    burgerMenu.addEventListener('click', function () {
        document.body.classList.toggle('menu-active');
    });
});
