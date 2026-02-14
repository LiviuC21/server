from flask import Flask, request
from flask_cors import CORS
import subprocess
import os

app = Flask(__name__)
CORS(app)

DOWNLOAD_PATH = "/home/phablet/Downloads/Muzica"
os.makedirs(DOWNLOAD_PATH, exist_ok=True)

@app.route('/download', methods=['GET'])
def download():
    url = request.args.get('url')
    format_type = request.args.get('format')
    
    if not url: return "Lipseste link-ul!", 400

    # Calea către yt-dlp din mediul tău conda
    yt_path = "/home/phablet/miniforge3/envs/muzica/bin/yt-dlp"
    output_template = f"{DOWNLOAD_PATH}/%(title)s.%(ext)s"

    if format_type == 'mp3':
        cmd = [yt_path, "-x", "--audio-format", "mp3", "-o", output_template, url]
    else:
        cmd = [yt_path, "-f", "mp4", "-o", output_template, url]

    try:
        subprocess.run(cmd, check=True)
        return "✅ Melodia a fost descărcată cu succes pe server în folderul Muzica!", 200
    except Exception as e:
        return f"❌ Eroare la descărcare: {str(e)}", 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9001)
