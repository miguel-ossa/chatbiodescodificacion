import re
import os
import tempfile
import subprocess
import unicodedata
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

def registrar_fuente_unicode():
    """Registra una fuente TrueType que soporte caracteres Unicode"""
    try:
        # Intentar registrar DejaVuSans (fuente libre con soporte Unicode completo)
        # Primero verifica si existe en el sistema
        fuentes_comunes = [
            # Linux
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
            "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
            "/usr/share/fonts/truetype/ubuntu/Ubuntu-R.ttf",
            # macOS
            "/System/Library/Fonts/Supplemental/Arial Unicode.ttf",
            "/System/Library/Fonts/Helvetica.ttf",
            "/Library/Fonts/Arial.ttf",
            # Windows
            "C:\\Windows\\Fonts\\arial.ttf",
            "C:\\Windows\\Fonts\\segoeui.ttf",
            "C:\\Windows\\Fonts\\arialuni.ttf",
            "C:\\Windows\\Fonts\\times.ttf",
        ]

        fuente_registrada = False
        for ruta_fuente in fuentes_comunes:
            if os.path.exists(ruta_fuente):
                try:
                    pdfmetrics.registerFont(TTFont('UnicodeFont', ruta_fuente))
                    fuente_registrada = True
                    print(f"Fuente Unicode registrada: {ruta_fuente}")
                    break
                except:
                    continue

        if not fuente_registrada:
            # Fallback: usar la fuente por defecto pero con registro de codificación
            pdfmetrics.registerFont(pdfmetrics.Font('UnicodeFont', 'Helvetica', 'WinAnsiEncoding'))
            print("Usando Helvetica como fallback")

    except Exception as e:
        print(f"Error registrando fuente Unicode: {e}")
        pdfmetrics.registerFont(pdfmetrics.Font('UnicodeFont', 'Helvetica', 'WinAnsiEncoding'))

# helpers simples
def escape_html(texto: str) -> str:
    texto = texto.replace("&", "&amp;")
    texto = texto.replace("<", "&lt;")
    texto = texto.replace(">", "&gt;")
    return texto

def limpiar_caracteres_especiales(texto: str) -> str:
    if not texto:
        return texto

    # Eliminar selectores de variación (U+FE00 a U+FE0F)
    texto = re.sub(r'[\uFE00-\uFE0F]', '', texto)

    # Eliminar combinador keycap U+20E3 (el de las teclas 1️⃣, 2️⃣, etc.)
    texto = texto.replace('\u20E3', '')

    # Eliminar emojis básicos (bloques más comunes)
    texto = re.sub(r'[\U0001F300-\U0001FAFF]', '', texto)  # símbolos/emojis
    texto = re.sub(r'[\U00002700-\U000027BF]', '', texto)  # dingbats

    # Eliminar otros caracteres de control problemáticos
    texto = re.sub(r'[\u0000-\u0008\u000B\u000C\u000E-\u001F\u007F]', '', texto)

    # Eliminar caracteres de formato Unicode
    texto = re.sub(r'[\u2000-\u200F\u2028-\u202F\u205F-\u206F]', ' ', texto)

    # Normalizar espacios
    texto = re.sub(r' +', ' ', texto)

    return texto

def normalizar_simbolos_global(texto: str) -> str:
    if not texto:
        return texto

    # Primero, limpiar selectores de variación y caracteres especiales
    texto = limpiar_caracteres_especiales(texto)

    reemplazos = {
        "■": "-",  # U+25A0 - BLACK SQUARE
        "▪": "-",  # U+25AA - BLACK SMALL SQUARE
        "□": "-",  # U+25A1 - WHITE SQUARE
        "▫": "-",  # U+25AB - WHITE SMALL SQUARE
        "–": "-",  # U+2013 - EN DASH
        "—": "-",  # U+2014 - EM DASH
        "·": "-",  # U+00B7 - MIDDLE DOT
        "•": "-",  # U+2022 - BULLET (por si acaso)
        "…": "...",  # U+2026 - HORIZONTAL ELLIPSIS
        "<br>•": "\n•",
        "<br>": "\n",
        "\u00a0": " ",  # NBSP
        "\u2028": " ",  # LINE SEPARATOR
        "\u2029": " ",  # PARAGRAPH SEPARATOR
        "\u202f": " ",  # NARROW NO-BREAK SPACE
        "\ufeff": "",  # ZERO WIDTH NO-BREAK SPACE (BOM)
    }

    for orig, dest in reemplazos.items():
        texto = texto.replace(orig, dest)

    # Rango geométrico completo: cualquier símbolo de caja/cuadrado/bullet → guion
    texto = re.sub(r"[\u25a0-\u25ff]", "-", texto)

    # También reemplazar otros caracteres de bloque
    texto = re.sub(r"[\u2580-\u259f]", "-", texto)  # Block Elements

    # Caracteres de flecha (opcional)
    texto = re.sub(r"[\u2190-\u21ff]", "-", texto)  # Arrows

    # Colapsar múltiples guiones
    texto = re.sub(r"-{2,}", "-", texto)

    # Eliminar espacios múltiples
    texto = re.sub(r" +", " ", texto)

    return texto

def slugify(text: str) -> str:
    text = unicodedata.normalize("NFKD", text)
    text = text.encode("ascii", "ignore").decode("ascii")
    text = re.sub(r"[^\w\s-]", "", text).strip().lower()
    return re.sub(r"[-\s]+", "_", text)


def ejemplos_markdown(examples: list[str]) -> str:
    # muestra solo las primeras palabras como hace Gradio
    lines = []
    for e in examples:
        if len(e) > 60:
            short = e[:57] + "..."
        else:
            short = e
        lines.append(f"- {short}")
    return "\n".join(lines)

def extraer_titulo_principal(texto: str) -> str | None:
    match = re.search(
        r"(?:#+\s*)?Entrada:\s*\*\*(.*?)\*\*",
        texto,
        re.IGNORECASE
    )
    if match:
        return match.group(1).strip()
    return None


def generar_pdf_con_pandoc(texto_markdown: str) -> str:
    # Normalizar solo lo mínimo necesario para el PDF
    texto_markdown = normalizar_simbolos_global(texto_markdown)

    # Intentar extraer título principal
    titulo = extraer_titulo_principal(texto_markdown)
    if titulo:
        # slug para el nombre de archivo
        filename = f"{slugify(titulo)}.pdf"
    else:
        filename = "respuesta_biodescodificacion.pdf"

    # Markdown temporal
    with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False, encoding='utf-8') as f:
        f.write(texto_markdown)
        md_path = f.name

    # Ruta final del PDF (en el mismo tmpdir)
    pdf_path = os.path.join(tempfile.gettempdir(), filename)

    # Opcional: pasar el título también a pandoc/LaTeX
    pandoc_cmd = [
        "pandoc",
        md_path,
        "-o", pdf_path,
        "--pdf-engine=xelatex",
        "-V", "mainfont=DejaVu Sans",
        "-V", "geometry:margin=2cm",
        "--highlight-style=tango",
    ]
    if titulo:
        pandoc_cmd.extend(["-V", f"title={titulo}"])

    subprocess.run(pandoc_cmd, check=True)

    return pdf_path

BULLET_ONLY = {"•", "-", "*", "·", "●", "○", "■", "▪", "▫"}

def limpiar_viñetas_huerfanas(text: str) -> str:
    if not text:
        return text

    lines = text.splitlines()
    cleaned = []

    for line in lines:
        stripped = line.strip()

        # 1) Línea completamente vacía o solo bullet
        if stripped == "" or stripped in BULLET_ONLY:
            # la dejamos pasar solo si es un salto entre párrafos;
            # si quieres borrarla siempre, simplemente `continue`
            cleaned.append("")  # o `continue` si quieres eliminarla del todo
            continue

        # 2) Líneas tipo "-   " (guion + espacios/no-break)
        if re.fullmatch(r"[-•*·●○■▪▫\s]+", stripped):
            cleaned.append("")
            continue

        cleaned.append(line)

    return "\n".join(cleaned)
