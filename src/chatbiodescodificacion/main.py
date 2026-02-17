#!/usr/bin/env python
import warnings
import os
import gradio as gr
from langdetect import detect
from chatbiodescodificacion.crew import Chatbiodescodificacion

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

crew_runner = Chatbiodescodificacion()

def detectar_idioma(texto: str) -> str:
    try:
        lang = detect(texto)
    except Exception:
        lang = "es"
    return lang

def chat_fn(message, history):
    """
    history: lista de dicts {"role": "...", "content": "..."} (formato messages).
    """
    print("ENV OPENAI_API_BASE =", os.getenv("OPENAI_API_BASE"))
    print("ENV CREWAI_LLM_BASE_URL =", os.getenv("CREWAI_LLM_BASE_URL"))
    print("ENV OLLAMA_HOST =", os.getenv("OLLAMA_HOST"))

    # Construir session_history para el crew
    session_history = []
    last_user = None
    for m in history:
        if m["role"] == "user":
            last_user = m["content"]
        elif m["role"] == "assistant" and last_user is not None:
            session_history.append({"user": last_user, "assistant": m["content"]})
            last_user = None

    user_lang = detectar_idioma(message)

    result = crew_runner.kickoff_search(
        message,
        user_lang=user_lang,
        session_history=session_history
    )

    full = result.get("final_output") or result.get("results") or ""

    # Añadimos los dos mensajes al history
    history = history + [
        {"role": "user", "content": message},
        {"role": "assistant", "content": full},
    ]

    # Devolvemos: limpiar textbox + nuevo history
    return "", history


def limpiar_fn():
    return []  # history vacío


# 'query': 'Desde hace 4 años tengo dolor en la  articulación del dedo pulgar de las dos manos (he tenido que dejar de trabajar de masajista) y toda la vida he tenido hiperhidrosis en las manos, pies y axilas. Y de nacimiento escoliosis lumbar pronunciada y a los 27 años tuve ansiedad y ataques de pánico.'
# 'query': 'dolor en la cadera que sube y baja de forma indistinta hacia el brazo derecho y dedo meñique o hacia la rodilla y dedos de los pies'
#'query': 'eccema o picor en las pantorrillas, que luego desaparece y se traslada al dorso de la mano'
# 'query': 'tengo vértigo cuando subo a sitios altos'


def crear_interfaz():
    with gr.Blocks(title="Chat Biodescodificación") as interfaz:
        gr.Markdown("# 🧬 Chat de Biodescodificación")
        gr.Markdown(f"📚 Diccionario cargado: 2096 entradas")

        chat = gr.Chatbot(
            label="Conversación",
            height=400,
            # en tu versión ya está en modo messages por defecto
        )

        mensaje = gr.Textbox(
            label="Tu pregunta",
            placeholder="Ej: ¿Qué conflictos están relacionados con problemas digestivos?",
            scale=4,
        )

        with gr.Row():
            boton_enviar = gr.Button("Enviar", variant="primary", scale=1)
            boton_limpiar = gr.Button("Limpiar", variant="secondary", scale=1)

        gr.Markdown("### 💡 Preguntas de ejemplo")
        gr.Examples(
            examples=[
                "¿Qué es la biodescodificación?",
                "Desde hace 4 años tengo dolor en la  articulación del dedo pulgar de las dos manos (he tenido que dejar de trabajar de masajista) y toda la vida he tenido hiperhidrosis en las manos, pies y axilas. Y de nacimiento escoliosis lumbar pronunciada y a los 27 años tuve ansiedad y ataques de pánico",
                "Sentido biológico de las alergias",
                "Eccema o picor en las pantorrillas, que luego desaparece y se traslada al dorso de la mano",
                "Dolor en la cadera que sube y baja de forma indistinta hacia el brazo derecho y dedo meñique o hacia la rodilla y dedos de los pies",
            ],
            inputs=mensaje,
        )

        boton_enviar.click(
            fn=chat_fn,
            inputs=[mensaje, chat],
            outputs=[mensaje, chat],
        )

        mensaje.submit(
            fn=chat_fn,
            inputs=[mensaje, chat],
            outputs=[mensaje, chat],
        )

        boton_limpiar.click(
            fn=limpiar_fn,
            outputs=chat,
        )

    return interfaz


def run():
    demo = crear_interfaz()
    demo.launch(server_name="0.0.0.0", server_port=7860, share=True)


if __name__ == "__main__":
    demo = crear_interfaz()
    demo.launch(server_name="0.0.0.0", server_port=7860, share=True)
