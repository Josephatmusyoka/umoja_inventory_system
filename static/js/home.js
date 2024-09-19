document.addEventListener('DOMContentLoaded', () => {
    const hamburgerMenu = document.getElementById('hamburger-menu');
    const mainNav = document.getElementById('main-nav');

    hamburgerMenu.addEventListener('click', () => {
        mainNav.classList.toggle('active');
    });
});
document.querySelector('.menu-toggle').addEventListener('click', function() {
    document.querySelector('.main-nav').classList.toggle('active');
});
// JavaScript for Automatic Carousel Scrolling
const carousel = document.querySelector('.team-carousel-wrapper');
const cards = document.querySelectorAll('.team-card');
const cardCount = cards.length;
const cardWidth = cards[0].offsetWidth;
const visibleCards = 4;
let index = 0;

// Function to move carousel
function moveCarousel() {
    index++;
    if (index >= cardCount - visibleCards + 1) {
        index = 0;
    }
    carousel.style.transform = `translateX(-${index * cardWidth}px)`;
}

// Automatic carousel scrolling every 10 seconds
setInterval(moveCarousel, 10000);

// Button functionality
document.querySelector('.prev-btn').addEventListener('click', () => {
    index = (index > 0) ? index - 1 : cardCount - visibleCards;
    carousel.style.transform = `translateX(-${index * cardWidth}px)`;
});

document.querySelector('.next-btn').addEventListener('click', () => {
    index = (index < cardCount - visibleCards) ? index + 1 : 0;
    carousel.style.transform = `translateX(-${index * cardWidth}px)`;
});
