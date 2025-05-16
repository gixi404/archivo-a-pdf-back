import os
from io import BytesIO
from flask import Flask, request, send_file, jsonify
from flask_cors import CORS
from PIL import Image, UnidentifiedImageError
from docx import Document
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from const import LOCALHOST, BACK_URL

app = Flask(__name__)
CORS(app, origins=[LOCALHOST, BACK_URL], methods=["POST"])


@app.route("/", methods=["GET"])
def index():
    return jsonify({"message": "Bienvenido"}), 200


@app.route("/convert", methods=["POST"])
def convert():
    file = request.files.get("file")
    if not file:
        return error_res("No se envió ningún archivo", 400)

    filename = file.filename.lower()

    try:
        if filename.endswith((".png", ".jpg", ".jpeg", ".webp")):
            pdf_io = convert_image_to_pdf(file.stream)
        elif filename.endswith(".docx"):
            pdf_io = convert_docx_to_pdf(file.stream)
        else:
            return error_res("Formato no soportado", 400)

        return send_file(
            pdf_io,
            mimetype="application/pdf",
            as_attachment=True,
            download_name=f"{os.path.splitext(file.filename)[0]}.pdf"
        )
    except UnidentifiedImageError:
        return error_res("El archivo no es una imagen válida", 400)
    except Exception as e:
        print(f"[ERROR] Fallo inesperado: {e}")
        return error_res("Error interno al convertir el archivo", 500)


def convert_image_to_pdf(file_stream: BytesIO) -> BytesIO:
    image = Image.open(file_stream).convert("RGB")
    output_pdf = BytesIO()
    image.save(output_pdf, format="PDF")
    output_pdf.seek(0)
    return output_pdf


def convert_docx_to_pdf(file_stream: BytesIO) -> BytesIO:
    doc = Document(file_stream)
    output_pdf = BytesIO()
    c = canvas.Canvas(output_pdf, pagesize=A4)
    width, height = A4

    margin = 40
    y = height - margin
    line_height = 14

    for para in doc.paragraphs:
        text = para.text.strip()
        if not text:
            y -= line_height
            continue

        lines = split_text(text, width - 2 * margin, c)
        for line in lines:
            c.drawString(margin, y, line)
            y -= line_height
            if y < margin:
                c.showPage()
                y = height - margin

    c.save()
    output_pdf.seek(0)
    return output_pdf


def split_text(text, max_width, canvas_obj):
    """Divide el texto si supera el ancho máximo."""
    words = text.split()
    lines = []
    current = ""
    for word in words:
        test = f"{current} {word}".strip()
        if canvas_obj.stringWidth(test) <= max_width:
            current = test
        else:
            lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def error_res(message: str, status: int):
    return jsonify({"error": message}), status


if __name__ == "__main__":
    app.run(
        debug=True,
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000)),
    )
