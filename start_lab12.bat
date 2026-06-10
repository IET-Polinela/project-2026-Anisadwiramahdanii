@echo off
cd /d C:\Users\x280\Documents\iet_24782037_2026

start "Lab 12 Backend - Django 8000" cmd /k "cd /d C:\Users\x280\Documents\iet_24782037_2026 && .venv\Scripts\python.exe server_smartcity\manage.py runserver 127.0.0.1:8000"
start "Lab 12 Frontend - SPA 5000" cmd /k "cd /d C:\Users\x280\Documents\iet_24782037_2026\smartcity_citizen_spa_npm && C:\Users\x280\Documents\iet_24782037_2026\.venv\Scripts\python.exe -m http.server 5000 --bind 127.0.0.1"

echo Lab 12 server sedang dinyalakan.
echo Frontend: http://127.0.0.1:5000/index.html
echo Backend : http://127.0.0.1:8000
pause
