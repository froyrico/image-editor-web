from flask import Flask, request, render_template, redirect, url_for
from PIL import Image, ImageOps, ImageFilter, ImageEnhance
import os
import uuid

app = Flask(__name__)

# Definir extensiones de archivo permitidas
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

# Función para verificar si el archivo tiene una extensión permitida
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Carpeta para almacenar imágenes temporalmente
UPLOAD_FOLDER = 'uploads/'
PROCESSED_FOLDER = 'static/images/processed/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Asegúrate de que las carpetas necesarias existen
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

if not os.path.exists(PROCESSED_FOLDER):
    os.makedirs(PROCESSED_FOLDER)

# Página principal que muestra el formulario de subida de imágenes
@app.route('/')
def index():
    return render_template('index.html')

# Ruta para manejar la subida y aplicación del filtro
@app.route('/upload', methods=['POST'])
def upload():
    # Verificar que haya un archivo en la solicitud
    if 'image' not in request.files:
        return "No se encontró la imagen", 400

    image_file = request.files['image']

    # Verificar si no hay nombre de archivo o el archivo no es permitido
    if image_file.filename == '':
        return "No se seleccionó ningún archivo", 400

    if not allowed_file(image_file.filename):
        return "Tipo de archivo no permitido. Solo se permiten archivos png, jpg, jpeg.", 400

    if image_file:
        # Generar un nombre único para la imagen
        filename = str(uuid.uuid4()) + ".png"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)

        # Guardar la imagen en la carpeta de uploads
        image_file.save(filepath)

        # Obtener los filtros seleccionados
        selected_filters = request.form.getlist('filters')

        # Procesar la imagen con los filtros seleccionados
        processed_image_path = apply_filters(filepath, selected_filters)

        # Obtener solo el nombre del archivo para renderizarlo en la plantilla
        processed_image_filename = os.path.basename(processed_image_path)

        # Renderizar result.html con la imagen procesada
        return render_template('result.html', processed_image_filename=processed_image_filename)

# Función para aplicar filtros a la imagen
def apply_filters(image_path, filters):
    image = Image.open(image_path)

    # Aplicar cada filtro seleccionado en orden
    for filter_type in filters:
        if filter_type == 'grayscale':
            image = image.convert('L')
        elif filter_type == 'sepia':
            if image.mode != 'RGB':
                image = image.convert('RGB')
            image = apply_sepia_filter(image)
        elif filter_type == 'invert':
            if image.mode != 'RGB':
                image = image.convert('RGB')
            image = ImageOps.invert(image)
        elif filter_type == 'blur':
            image = image.filter(ImageFilter.BLUR)
        elif filter_type == 'contour':
            image = image.filter(ImageFilter.CONTOUR)
        elif filter_type == 'brightness':
            if image.mode != 'RGB':
                image = image.convert('RGB')
            enhancer = ImageEnhance.Brightness(image)
            image = enhancer.enhance(1.5)
        elif filter_type == 'contrast':
            if image.mode != 'RGB':
                image = image.convert('RGB')
            enhancer = ImageEnhance.Contrast(image)
            image = enhancer.enhance(1.5)
        elif filter_type == 'sharpen':
            if image.mode != 'RGB':
                image = image.convert('RGB')
            enhancer = ImageEnhance.Sharpness(image)
            image = enhancer.enhance(2.0)
        elif filter_type == 'edge_enhance':
            image = image.filter(ImageFilter.EDGE_ENHANCE)

    # Guardar la imagen procesada en la carpeta de imágenes procesadas
    processed_image_path = os.path.join(PROCESSED_FOLDER, "processed_" + os.path.basename(image_path))
    image.save(processed_image_path)

    return processed_image_path

# Función para aplicar el filtro sepia
def apply_sepia_filter(image):
    if image.mode != 'RGB':
        image = image.convert('RGB')

    width, height = image.size
    pixels = image.load()

    for py in range(height):
        for px in range(width):
            r, g, b = image.getpixel((px, py))

            # Aplicar la transformación sepia
            tr = int(0.393 * r + 0.769 * g + 0.189 * b)
            tg = int(0.349 * r + 0.686 * g + 0.168 * b)
            tb = int(0.272 * r + 0.534 * g + 0.131 * b)

            tr = min(255, tr)
            tg = min(255, tg)
            tb = min(255, tb)

            pixels[px, py] = (tr, tg, tb)

    return image

# Iniciar el servidor Flask
if __name__ == "__main__":
    app.run(debug=True)
