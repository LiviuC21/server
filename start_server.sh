#!/bin/bash
cd /home/phablet/server

# 1. Oprim tot ce e vechi
pkill -f filebrowser

# 2. Pornim serviciile
nohup ./filebrowser -r /home/phablet/Downloads -p 8081 > /dev/null 2>&1 &
nohup python3 telecomanda.py > /dev/null 2>&1 &
nohup python3 downloader.py > /dev/null 2>&1 &

# 3. Modificăm index.html (Schimbăm statusul și afișăm butonul)
sed -i 's/SERVER OFFLINE/SERVER ONLINE/g' index.html
sed -i 's/🔴/🟢/g' index.html
sed -i 's/display: none;/display: block;/g' index.html

# 4. Push pe GitHub
git add index.html
git commit -m "Server Online cu buton de acces"
git push origin main
