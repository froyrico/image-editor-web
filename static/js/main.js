document.addEventListener('DOMContentLoaded', function () {
    const imageInput = document.getElementById('image');
    const preview = document.createElement('img');
    preview.classList.add('w-full', 'h-auto', 'mb-4');
    
    imageInput.addEventListener('change', function (event) {
        const file = event.target.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = function (e) {
                preview.src = e.target.result;
                imageInput.parentElement.insertBefore(preview, imageInput.nextSibling);
            };
            reader.readAsDataURL(file);
        }
    });
});

document.getElementById('toggle-theme').addEventListener('click', function() {
    const body = document.body;
    const button = document.getElementById('toggle-theme');

    // Alternar las clases para el modo oscuro/claro
    body.classList.toggle('dark-mode');

    // Cambiar el texto y la clase del botón según el estado del modo
    if (body.classList.contains('dark-mode')) {
        button.textContent = 'Modo Claro';
        button.classList.remove('btn-secondary');
        button.classList.add('btn-light');
    } else {
        button.textContent = 'Modo Oscuro';
        button.classList.remove('btn-light');
        button.classList.add('btn-secondary');
    }
});

