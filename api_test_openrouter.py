# Demasiado lento

import requests
import json
import os
from dotenv import load_dotenv

load_dotenv(override=True)

api_key = os.getenv("OPENROUTER_API_KEY")
if not api_key:
    raise ValueError("OPENROUTER_API_KEY no encontrada en .env")

response = requests.post(
    url="https://openrouter.ai/api/v1/chat/completions",
    headers={
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",  # Recomendado
        # "HTTP-Referer": "https://tu-sitio.com",  # Opcional para rankings
        # "X-Title": "Tu App"  # Opcional
    },
    json={  # Usa json= en lugar de data=json.dumps() para simplicidad
        "model": "gpt-oss-120b",
        "messages": [
            {"role": "user", "content": "What is the meaning of life?"}
        ]
    }
)

if response.status_code == 200:
    data = response.json()  # Parsea JSON automáticamente
    content = data['choices'][0]['message']['content']
    print(content)  # Solo el texto limpio de la respuesta
else:
    print(f"Error: {response.status_code} - {response.text}")
