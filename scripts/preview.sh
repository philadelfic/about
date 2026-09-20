#!/usr/bin/env bash
# Собирает сайт и поднимает предпросмотр на порту 4321 без host-проверок,
# чтобы страница открывалась и напрямую, и через туннель (serveo/cloudflared).
set -euo pipefail
cd "$(dirname "$0")/.."

npm run build

rm -rf /tmp/preview
mkdir -p /tmp/preview
cp -r dist /tmp/preview/about

pkill -f "http.server 4321" 2>/dev/null || true
sleep 1
nohup python3 -m http.server 4321 --bind 0.0.0.0 --directory /tmp/preview >/tmp/httpd.log 2>&1 &

sleep 1
echo "Предпросмотр: http://localhost:4321/about/"
