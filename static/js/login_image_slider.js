const images = [
    '/images/tanques.jpg',
    '/images/telecomunicacion.jpg',
    '/images/torres.jpg'
];

let current = 0;
const img = document.getElementById('login-img');

function fadeToNextImage() {
    img.style.opacity = 0;
    setTimeout(() => {
        current = (current + 1) % images.length;
        img.src = images[current];
        img.style.opacity = 1;
    }, 700); // match CSS transition duration
}

setInterval(fadeToNextImage, 3000);
