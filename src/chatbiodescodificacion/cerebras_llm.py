import os
from crewai import LLM

CEREBRAS_API_KEY = os.getenv("CEREBRAS_API_KEY")

if not CEREBRAS_API_KEY:
    raise ValueError("CEREBRAS_API_KEY no encontrada en .env")

cerebras_llm = LLM(
    model="gpt-oss-120b",
    api_key=CEREBRAS_API_KEY,
    base_url="https://api.cerebras.ai/v1",  # endpoint OpenAI-compatible de Cerebras
    # opcionalmente:
    temperature=0.2,
    top_p=1.0,
    max_tokens=1024,
)
