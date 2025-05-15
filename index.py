import os
from io import BytesIO
import base64
from PIL import Image, UnidentifiedImageError
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/convert_png", methods=["POST"])
def convert_png():
    if 'file' not in request.files:
        return jsonify({"error": "No se envió ningún archivo"}), 400

    file = request.files['file']

    if not file.filename.lower().endswith('.png'):
        return jsonify({"error": "El archivo debe tener extensión .png"}), 400

    pdf_io = png_to_pdf(file.stream)

    if not pdf_io:
        return jsonify({"error": "Error al convertir el archivo"}), 500

    pdf_base64 = base64.b64encode(pdf_io.getvalue()).decode('utf-8')

    return jsonify({"file": pdf_base64})


def png_to_pdf(file_bytes: BytesIO) -> BytesIO | None:
    try:
        image = Image.open(file_bytes).convert("RGB")
        output_pdf = BytesIO()
        image.save(output_pdf, format="PDF")
        output_pdf.seek(0)
        return output_pdf
    except UnidentifiedImageError as e:
        print("Error indentificando la imagen: ", e)
    except Exception as e:
        print(f"Error inesperado: {e}")
    return None


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=True)
