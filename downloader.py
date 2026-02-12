from flask import Flask, request, send_file
from flask_cors import CORS
import subprocess
import os
import time

app = Flask(__name__)
CORS(app)

DOWNLOAD_PATH = "/home/phablet/Downloads/Muzica"
os.makedirs(DOWNLOAD_PATH, exist_ok=True)

@app.route('/download', methods=['GET'])
def download():
    url = request.args.get('url')
    format_type = request.args.get('format')
    
    if not url: return "Lipseste link-ul!", 400

    timestamp = int(time.time())
    output_temp = f"{DOWNLOAD_PATH}/dl_{timestamp}.%(ext)s"

    if format_type == 'mp3':
        cmd = ["/home/phablet/miniforge3/envs/muzica/bin/yt-dlp","-x","--audio-format","mp3", "-o", output_temp, url]
    else:
        cmd = ["yt-dlp", "-f", "mp4", "-o", output_temp, url]

    try:
        subprocess.run(cmd, check=True)
        for f in os.listdir(DOWNLOAD_PATH):
            if f.startswith(f"dl_{timestamp}"):
                return send_file(os.path.join(DOWNLOAD_PATH, f), as_attachment=True)
        return "Eroare: Fisier negasit", 404
    except Exception as e:
        return f"Eroare: {str(e)}", 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9001)
