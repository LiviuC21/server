from flask import Flask, request
from flask_cors import CORS
import os
from PIL import Image
from pdf2docx import Converter

app = Flask(__name__)
CORS(app)

BASE = "/home/phablet/Downloads"
FOLDERS = {
    "img": os.path.join(BASE, "JPG_TO_PDF"),
    "word": os.path.join(BASE, "PDF_TO_WORD"),
    "topdf": os.path.join(BASE, "WORD_TO_PDF"),
    "ocr": os.path.join(BASE, "OCR")
}

for p in FOLDERS.values(): os.makedirs(p, exist_ok=True)

@app.route('/convert-images', methods=['POST'])
def images_pdf():
    files = request.files.getlist("files")
    imgs = [Image.open(f).convert('RGB') for f in files]
    out = os.path.join(FOLDERS["img"], f"doc_{len(imgs)}.pdf")
    imgs[0].save(out, save_all=True, append_images=imgs[1:])
    return "Imagine convertită!"

@app.route('/pdf-to-word', methods=['POST'])
def pdf_word():
    f = request.files.getlist("files")[0]
    pdf_p = os.path.join(FOLDERS["word"], "temp.pdf")
    docx_p = os.path.join(FOLDERS["word"], f.filename.replace(".pdf", ".docx"))
    f.save(pdf_p)
    cv = Converter(pdf_p)
    cv.convert(docx_p)
    cv.close()
    return "PDF transformat în Word!"

@app.route('/ocr-scan', methods=['POST'])
def ocr():
    return "OCR în curs de procesare (Pasul următor)..."

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9000)
