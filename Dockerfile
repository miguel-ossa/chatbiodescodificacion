FROM python:3.13.7

ENV PYTHONUNBUFFERED=1
ENV GRADIO_SERVER_NAME="0.0.0.0"
ENV GRADIO_SERVER_PORT=7860

WORKDIR /app

# 1) SO + pandoc + LaTeX (capa estable)
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        pandoc \
        texlive-latex-recommended \
        texlive-latex-extra \
        texlive-fonts-recommended \
        texlive-fonts-extra \
        texlive-xetex \
        lmodern && \
    rm -rf /var/lib/apt/lists/*

# 2) Python deps (capa estable mientras no cambie requirements)
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# 3) Código (capa volátil: se reconstruye rápido)
COPY src/ .

EXPOSE 7860
CMD ["python", "-m", "chatbiodescodificacion.main"]
