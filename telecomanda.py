from flask import Flask, request
from flask_cors import CORS
import os
import subprocess
from PIL import Image
from pdf2docx import Converter
import pytesseract

app = Flask(__name__)
CORS(app)

# Structura folderelor pe care am creat-o
BASE = "/home/phablet/Downloads"
FOLDERS = {
    "img": os.path.join(BASE, "JPG_TO_PDF"),
    "word": os.path.join(BASE, "PDF_TO_WORD"),
    "topdf": os.path.join(BASE, "WORD_TO_PDF"),
    "ocr": os.path.join(BASE, "OCR")
}

# Ne asigurăm că toate sertarele sunt create pe tabletă
for p in FOLDERS.values(): 
    os.makedirs(p, exist_ok=True)

@app.route('/')
def home():
    return "Server Telecomanda (Port 9000) - Toate uneltele sunt active!", 200

# 1. IMAGINI ➔ PDF (Pillow)
@app.route('/convert-images', methods=['POST'])
def images_pdf():
    try:
        files = request.files.getlist("files")
        imgs = [Image.open(f).convert('RGB') for f in files]
        out = os.path.join(FOLDERS["img"], f"conversie_{len(imgs)}_pagini.pdf")
        imgs[0].save(out, save_all=True, append_images=imgs[1:])
        return "✅ PDF creat în folderul JPG_TO_PDF!", 200
    except Exception as e:
        return f"❌ Eroare Imagini: {str(e)}", 500

# 2. PDF ➔ WORD (pdf2docx)
@app.route('/pdf-to-word', methods=['POST'])
def pdf_word():
    try:
        f = request.files.getlist("files")[0]
        pdf_p = os.path.join(FOLDERS["word"], "temp_upload.pdf")
        docx_p = os.path.join(FOLDERS["word"], f.filename.replace(".pdf", ".docx"))
        f.save(pdf_p)
        
        cv = Converter(pdf_p)
        cv.convert(docx_p)
        cv.close()
        return f"✅ Word creat în PDF_TO_WORD: {f.filename.replace('.pdf', '.docx')}", 200
    except Exception as e:
        return f"❌ Eroare PDF to Word: {str(e)}", 500

# 3. WORD ➔ PDF (LibreOffice Headless) - ACEASTA ESTE NOUA ADĂUGARE
@app.route('/word-to-pdf', methods=['POST'])
def word_pdf():
    try:
        f = request.files.getlist("files")[0]
        p = os.path.join(FOLDERS["topdf"], f.filename)
        f.save(p)
        
        # Lansăm comanda LibreOffice în fundal
        subprocess.run([
            'libreoffice', '--headless', 
            '--convert-to', 'pdf', 
            '--outdir', FOLDERS["topdf"], 
            p
        ], check=True)
        
        return "✅ Word convertit profesional în PDF!", 200
    except Exception as e:
        return f"❌ Eroare LibreOffice: {str(e)}", 500

# 4. SCANNER AI / OCR (Tesseract)
@app.route('/ocr-scan', methods=['POST'])
def ocr_scan():
    try:
        f = request.files.getlist("files")[0]
        p = os.path.join(FOLDERS["ocr"], f.filename)
        f.save(p)
        
        # Tesseract extrage textul folosind dicționarele română și engleză
        text = pytesseract.image_to_string(Image.open(p), lang='ron+eng')
        
        txt_path = os.path.join(FOLDERS["ocr"], f.filename.split('.')[0] + ".txt")
        with open(txt_path, "w", encoding="utf-8") as out:
            out.write(text)
            
        return "✅ Text extras în folderul OCR!", 200
    except Exception as e:
        return f"❌ Eroare OCR: {str(e)}", 500

if __name__ == '__main__':
    # Rulăm pe portul 9000, așa cum am setat în index.html
    app.run(host='0.0.0.0', port=9000)
