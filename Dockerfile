FROM python:3.13.7

ENV PYTHONUNBUFFERED=1
ENV GRADIO_SERVER_NAME="0.0.0.0"
ENV GRADIO_SERVER_PORT=7860

WORKDIR /app

COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# Copiar el contenido de src dentro de /app
COPY src/ .

EXPOSE 7860

CMD ["python", "-m", "chatbiodescodificacion.main"]
