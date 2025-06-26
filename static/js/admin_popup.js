// admin_popup.js

document.addEventListener('DOMContentLoaded', function() {
    const popupBg = document.getElementById('popup-bg');
    const popupForm = document.getElementById('popup-form');
    const popupId = document.getElementById('popup-id');
    const closeBtn = document.getElementById('close-popup');
    const responderBtns = document.querySelectorAll('.responder-btn');

    responderBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            const id = this.getAttribute('data-id');
            popupId.value = id;
            popupBg.classList.add('active');
        });
    });

    closeBtn.addEventListener('click', function() {
        popupBg.classList.remove('active');
        popupForm.reset();
    });

    // Cerrar popup al hacer click fuera del formulario
    popupBg.addEventListener('click', function(e) {
        if (e.target === popupBg) {
            popupBg.classList.remove('active');
            popupForm.reset();
        }
    });
});
