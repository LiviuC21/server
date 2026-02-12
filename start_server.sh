[200~#!/bin/bash
cd /home/phablet/server

# 1. Oprim doar FileBrowser-ul vechi (NU atingem telecomanda!)
pkill -f filebrowser

# 2. Pornim FileBrowser folosind setările care au mers manual
# Am pus '-p 8081' clar și '-a 0.0.0.0' ca să poată fi văzut de Tailscale
nohup ./filebrowser -r /home/phablet/Downloads -p 8081 -a 0.0.0.0 > fb.log 2>&1 &

# 3. Așteptăm 2 secunde să se așeze procesul
sleep 2

# 4. Modificăm pagina de GitHub să apară ONLINE și butonul de acces
# Folosim 'sed' ca să fim siguri că nu stricăm restul codului HTML
sed -i 's/SERVER OFFLINE/SERVER ONLINE/g' index.html
sed -i 's/🔴/🟢/g' index.html
sed -i 's/display: none/display: block/g' index.html

# 5. Trimitem update-ul pe GitHub
git add index.html
git commit -m "Server Online - Pornit de la distanta"
git push origin main

echo "✅ Serverul a pornit și statusul a fost trimis pe GitHub!"
