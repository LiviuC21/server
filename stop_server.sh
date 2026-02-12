#!/bin/bash
cd /home/phablet/server

# Oprim tot
pkill -f filebrowser
pkill -f telecomanda.py
pkill -f downloader.py

# Schimbam statusul in index.html inapoi pe rosu
sed -i 's/SERVER ONLINE/SERVER OFFLINE/g' index.html
sed -i 's/background: #2ecc71/background: #c0392b/g' index.html
sed -i 's/🟢/🔴/g' index.html

# Trimitem pe GitHub
git add index.html
git commit -m "Server oprit"
git push origin main

echo "🛑 Serverul a fost oprit."
