#!/usr/bin/env bash
# Поднимает временный публичный адрес для предпросмотра (SSH-туннель через serveo.net).
# Печатает ссылку; живёт до закрытия сессии. Использование: scripts/tunnel.sh [порт]
set -euo pipefail
PORT="${1:-4321}"
LOG=/tmp/serveo-tunnel.log

pkill -f "serveo.net" 2>/dev/null || true
sleep 1

nohup bash -c "ssh -tt -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null \
  -o ServerAliveInterval=30 -R 80:localhost:${PORT} serveo.net" > "$LOG" 2>&1 &

for _ in $(seq 1 20); do
  URL=$(grep -o "https://[a-z0-9.-]*serveousercontent.com" "$LOG" | head -1 || true)
  [ -n "$URL" ] && break
  sleep 1
done

if [ -z "${URL:-}" ]; then
  echo "Не удалось получить ссылку, смотри $LOG" >&2
  exit 1
fi

echo "$URL/about/"
