#!/usr/bin/env python
import warnings
import gradio as gr
from chatbiodescodificacion.crew import Chatbiodescodificacion

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

crew_runner = Chatbiodescodificacion()


def chat_fn(message, history):
    """
    history: lista de dicts {"role": "...", "content": "..."} (formato messages).
    """
    # Construir session_history para el crew
    session_history = []
    last_user = None
    for m in history:
        if m["role"] == "user":
            last_user = m["content"]
        elif m["role"] == "assistant" and last_user is not None:
            session_history.append({"user": last_user, "assistant": m["content"]})
            last_user = None

    result = crew_runner.kickoff_search(message, session_history=session_history)
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


def crear_interfaz():
    with gr.Blocks(title="Chat Biodescodificación") as interfaz:
        gr.Markdown("# 🧬 Chat de Biodescodificación")

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
                "¿Conflictos emocionales del estómago?",
                "Sentido biológico de las alergias",
                "Emociones y problemas de piel",
                "¿Qué sentido biológico tiene el covid?",
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
    demo.launch(share=True)


if __name__ == "__main__":
    demo = crear_interfaz()
    demo.launch()
