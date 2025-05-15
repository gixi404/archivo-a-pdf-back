from flask import Flask, request, send_file, jsonify
from PIL import Image, UnidentifiedImageError
from io import BytesIO

app = Flask(__name__)


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

    return send_file(
        pdf_io,
        mimetype='application/pdf',
        as_attachment=True,
        download_name='output.pdf'
    )


if __name__ == "__main__":
    app.run(debug=True)
