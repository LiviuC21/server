from flask import Flask, request
from flask_cors import CORS
import os, subprocess, cv2
import numpy as np
from PIL import Image
from pdf2docx import Converter
import pytesseract

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

# RUTA DE STATUS (Pentru becul verde de pe site)
@app.route('/')
def home():
    return "Server Online", 200

@app.route('/convert-images', methods=['POST'])
def images_pdf():
    files = request.files.getlist("files")
    imgs = [Image.open(f).convert('RGB') for f in files]
    out = os.path.join(FOLDERS["img"], f"doc_{len(imgs)}_pagini.pdf")
    imgs[0].save(out, save_all=True, append_images=imgs[1:])
    return "✅ PDF Creat!"

@app.route('/pdf-to-word', methods=['POST'])
def pdf_word():
    try:
        f = request.files.getlist("files")[0]
        pdf_p = os.path.join(FOLDERS["word"], "temp.pdf")
        docx_p = os.path.join(FOLDERS["word"], f.filename.replace(".pdf", ".docx"))
        f.save(pdf_p)
        cv = Converter(pdf_p)
        cv.convert(docx_p)
        cv.close()
        return "✅ PDF transformat!"
    except Exception as e: return f"❌ Eroare: {str(e)}"

@app.route('/word-to-pdf', methods=['POST'])
def word_pdf():
    try:
        f = request.files.getlist("files")[0]
        p = os.path.join(FOLDERS["topdf"], f.filename)
        f.save(p)
        # Folosim LibreOffice Headless
        subprocess.run(['libreoffice', '--headless', '--convert-to', 'pdf', '--outdir', FOLDERS["topdf"], p], check=True)
        return "✅ Word convertit profesional!"
    except Exception as e: return f"❌ Eroare: {str(e)}"

@app.route('/ocr-scan', methods=['POST'])
def ocr_scan():
    try:
        f = request.files.getlist("files")[0]
        p = os.path.join(FOLDERS["ocr"], f.filename)
        f.save(p)
        
        # PROCESARE OCHELARI (OpenCV)
        img = cv2.imread(p)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        processed = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
        
        temp_p = os.path.join(FOLDERS["ocr"], "temp_clean.png")
        cv2.imwrite(temp_p, processed)

        text = pytesseract.image_to_string(Image.open(temp_p), lang='ron+eng')
        txt_p = os.path.join(FOLDERS["ocr"], f.filename.split('.')[0] + ".txt")
        with open(txt_p, "w", encoding="utf-8") as out: out.write(text)
        return "✅ Scanare îmbunătățită terminată!"
    except Exception as e: return f"❌ Eroare OCR: {str(e)}"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9000)
