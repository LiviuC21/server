from flask import Flask
import subprocess
import os

app = Flask(__name__)

@app.route('/start')
def start_server():
    # Ruleaza scriptul de pornire pe care l-ai refacut deja
    subprocess.Popen(['bash', '/home/phablet/server/start_server.sh'])
    return "Comanda de pornire a fost trimisa catre tableta!"

@app.route('/stop')
def stop_server():
    # Ruleaza scriptul de oprire
    subprocess.Popen(['bash', '/home/phablet/server/stop_server.sh'])
    return "Comanda de oprire a fost trimisa catre tableta!"

if __name__ == '__main__':
    # Asculta pe portul 9000 pentru GitHub
    app.run(host='0.0.0.0', port=9000)
