#!/usr/bin/env bash
set -e

# Precalentar SSH (evita primer timeout)
ssh -o ConnectTimeout=10 -o BatchMode=yes mossa@192.168.1.90 'echo > /dev/null' || true

# Variables app
export FLYCTL_INSTALL="/Users/mossa/.fly"
export PATH="$FLYCTL_INSTALL/bin:$PATH"
export PATH="$HOME/.local/bin:$PATH"
# export OLLAMA_HOST="http://localhost:11434"

echo
echo "!! Deseas limpiar recursos de Docker (docker system prune -af y docker volume prune -f)?"
echo "   Esto borrara contenedores parados, imagenes sin usar, redes huerfanas y volumenes no utilizados."
echo -n "   Pulsa 'y' en 10 segundos para proceder, o cualquier otra tecla/espera para saltar: "

ANSWER=""
# lee 1 caracter, sin Enter, con timeout de 10s
if read -r -n 1 -t 10 ANSWER; then
  echo    # salto de linea despues de la tecla
else
  echo    # timeout, solo salto de linea
  ANSWER=""
fi

if [ "$ANSWER" = "y" ]; then
  echo
  echo "Limpiando recursos de Docker..."
  docker system prune -af
  docker volume prune -f
  echo
else
  echo "Limpieza de Docker omitida."
  echo
fi

# Build limpio + up
docker compose build --no-cache
docker compose up

echo "ChatBiodescodificacion corriendo en http://192.168.1.90:7860"
echo "Logs: docker compose logs -f"
echo "Parar: docker compose down"

