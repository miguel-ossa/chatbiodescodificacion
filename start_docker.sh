#!/usr/bin/env bash

# Precalentar SSH (evita primer timeout)
ssh -o ConnectTimeout=10 -o BatchMode=yes mossa@192.168.1.90 'echo > /dev/null' || true

# Variables app
export FLYCTL_INSTALL="/Users/mossa/.fly"
export PATH="$FLYCTL_INSTALL/bin:$PATH"
export PATH="$HOME/.local/bin:$PATH"
export OLLAMA_HOST="http://localhost:11434"

# Build limpio + up detached
docker compose build --no-cache
docker compose up

echo "✅  ChatBiodescodificacion corriendo en http://192.168.1.90:7860"
echo "📊  Logs: docker compose logs -f"
echo "🛑  Parar: docker compose down"

