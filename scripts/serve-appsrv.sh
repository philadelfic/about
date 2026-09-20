#!/usr/bin/env bash
# Публикует собранный сайт на appsrv: http://192.168.3.111:3040/about/
# (контейнер about-preview на хостовом docker; порт 3040).
# Использование: scripts/serve-appsrv.sh
set -euo pipefail
cd "$(dirname "$0")/.."

PORT="${PORT:-3040}"
NAME="${NAME:-about-preview}"

npm run build

rm -rf /tmp/preview
mkdir -p /tmp/preview
cp -r dist /tmp/preview/about
cat > /tmp/preview/Dockerfile <<'EOF'
FROM nginx:alpine
COPY about /usr/share/nginx/html/about
EOF

docker build -q -t about-preview:latest /tmp/preview >/dev/null
docker rm -f "$NAME" >/dev/null 2>&1 || true
docker run -d --name "$NAME" --restart unless-stopped -p "${PORT}:80" about-preview:latest >/dev/null

echo "Опубликовано: http://192.168.3.111:${PORT}/about/"
