from flask import Flask, request
from flask_cors import CORS
import subprocess
import os

app = Flask(__name__)
CORS(app)

# Calea unde se salvează fișierele
DOWNLOAD_PATH = "/home/phablet/Downloads/Muzica"
os.makedirs(DOWNLOAD_PATH, exist_ok=True)

@app.route('/download', methods=['GET'])
def download():
    url = request.args.get('url')
    format_type = request.args.get('format')
    
    if not url: return "Lipsește link-ul!", 400

    # Calea către yt-dlp din mediul tău conda
    yt_path = "/home/phablet/miniforge3/envs/muzica/bin/yt-dlp"
    output_template = f"{DOWNLOAD_PATH}/%(title)s.%(ext)s"

    if format_type == 'mp3':
        cmd = [yt_path, "-x", "--audio-format", "mp3", "-o", output_template, url]
    else:
        # Pentru MP4 descărcăm cel mai bun format video disponibil
        cmd = [yt_path, "-f", "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best", "-o", output_template, url]

    try:
        subprocess.run(cmd, check=True)
        tip = "Melodia" if format_type == 'mp3' else "Videoclipul"
        return f"✅ {tip} a fost descărcat(ă) cu succes pe server în folderul Muzica!", 200
    except Exception as e:
        return f"❌ Eroare la descărcare YouTube: {str(e)}", 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9001)
