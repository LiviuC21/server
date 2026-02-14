#!/bin/bash
cd /home/phablet/server

# 1. Curățăm orice proces vechi sau blocat
pkill -f filebrowser
sleep 1

# 2. Pornim FileBrowser
# Am adăugat '-d filebrowser.db' pentru a folosi baza de date locală corectă
nohup ./filebrowser -d /home/phablet/server/filebrowser.db -r /home/phablet/Downloads -p 8081 -a 0.0.0.0 > fb.log 2>&1 &

# 3. Verificăm dacă a pornit cu adevărat
sleep 2
if pgrep -x "filebrowser" > /dev/null
then
    echo "✅ FileBrowser a pornit cu succes pe portul 8081!"
else
    echo "❌ Eroare: FileBrowser nu a putut porni. Verifică fb.log"
fi
