# !pip install cerebras-cloud-sdk
import os
from cerebras.cloud.sdk import Cerebras
from dotenv import load_dotenv

# gpt-oss-120b
# 30 requests/minute
# 60,000 tokens/minute
# 900 requests/hour
# 1,000,000 tokens/hour
# 14,400 requests/day
# 1,000,000 tokens/day

load_dotenv(override=True)

api_key = os.getenv("CEREBRAS_API_KEY")
if not api_key:
    raise ValueError("CEREBRAS_API_KEY no encontrada en .env")

client = Cerebras(
  api_key=os.environ.get("CEREBRAS_API_KEY")
)

completion = client.chat.completions.create(
  messages=[{"role":"user","content":"What is the meaning of life?"}],
  model="gpt-oss-120b",
  max_completion_tokens=1024,
  temperature=0.2,
  top_p=1,
  stream=False
)

print(completion.choices[0].message.content)