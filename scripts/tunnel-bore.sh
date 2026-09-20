#!/usr/bin/env bash
# Временный публичный адрес для предпросмотра: туннель bore (без страницы-предупреждения).
# Печатает ссылку вида http://bore.pub:PORT/about/. Использование: scripts/tunnel-bore.sh [порт]
set -euo pipefail
PORT="${1:-4321}"
BIN=/tmp/bore
LOG=/tmp/bore.log

if [ ! -x "$BIN" ]; then
  curl -sL -o /tmp/bore.tar.gz \
    https://github.com/ekzhang/bore/releases/download/v0.6.0/bore-v0.6.0-x86_64-unknown-linux-musl.tar.gz
  tar xzf /tmp/bore.tar.gz -C /tmp
fi

pkill -f "bore local" 2>/dev/null || true
sleep 1

nohup "$BIN" local "$PORT" --to bore.pub > "$LOG" 2>&1 &

for _ in $(seq 1 20); do
  REMOTE=$(grep -o "bore.pub:[0-9]*" "$LOG" | head -1 || true)
  [ -n "$REMOTE" ] && break
  sleep 1
done

if [ -z "${REMOTE:-}" ]; then
  echo "Не удалось получить ссылку, смотри $LOG" >&2
  exit 1
fi

echo "http://${REMOTE}/about/"
