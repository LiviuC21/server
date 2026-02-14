from flask import Flask, request
from flask_cors import CORS
import subprocess
import os
from PIL import Image

app = Flask(__name__)
CORS(app) # Permite comunicarea intre GitHub si Tableta

# 1. Configurare foldere pentru organizare
BASE_PATH = "/home/phablet/Downloads"
FOLDERS = {
    "images": os.path.join(BASE_PATH, "JPG_TO_PDF"),
    "ocr": os.path.join(BASE_PATH, "OCR"),
    "word": os.path.join(BASE_PATH, "PDF_TO_WORD")
}

# Cream folderele daca nu exista deja
for path in FOLDERS.values():
    os.makedirs(path, exist_ok=True)

@app.route('/')
def home():
    return "Server Telecomanda (Port 9000) - Sistem PDF & Control Online", 200

# --- FUNCTII VECHI (Control Server) ---

@app.route('/start')
def start_server():
    # Pastram functia de pornire a downloader-ului
    subprocess.Popen(['bash', '/home/phablet/server/start_server.sh'])
    return "Comanda de pornire trimisa!", 200

@app.route('/stop')
def stop_server():
    # Pastram functia de oprire
    subprocess.Popen(['bash', '/home/phablet/server/stop_server.sh'])
    return "Comanda de oprire trimisa!", 200

# --- FUNCTII NOI (iLovePDF Privat) ---

@app.route('/convert-images', methods=['POST'])
def convert_images():
    if 'files' not in request.files:
        return "Eroare: Niciun fisier selectat", 400
    
    files = request.files.getlist("files")
    image_list = []
    
    try:
        for file in files:
            img = Image.open(file)
            # Convertim in RGB (necesar pentru salvarea in PDF)
            if img.mode != 'RGB':
                img = img.convert('RGB')
            image_list.append(img)
        
        if image_list:
            # Cream un nume unic bazat pe numarul de poze
            output_name = f"conversie_{len(image_list)}_imagini.pdf"
            output_path = os.path.join(FOLDERS["images"], output_name)
            
            # Salvare: Prima imagine e baza, restul sunt atasate
            image_list[0].save(output_path, save_all=True, append_images=image_list[1:])
            return f"Succes! PDF-ul a fost creat in folderul JPG_TO_PDF", 200
            
    except Exception as e:
        return f"Eroare procesare: {str(e)}", 500

@app.route('/ocr-scan', methods=['POST'])
def ocr_scan():
    # Placeholder pentru pasul urmator cu EasyOCR
    return "Functia OCR este in curs de configurare pe tableta.", 200

if __name__ == '__main__':
    # Asculta pe portul 9000
    app.run(host='0.0.0.0', port=9000)
