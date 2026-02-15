#!/usr/bin/env python
import warnings
import json

from chatbiodescodificacion.crew import Chatbiodescodificacion

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

crew_runner = Chatbiodescodificacion()

def pretty_result(result: dict) -> str:
    safe = {
        "query": result.get("query"),
        "status": "error" if result.get("error") else "ok",
    }

    if result.get("error"):
        safe["error"] = result["error"]
    else:
        full = result.get("final_output") or result.get("results") or ""
        # sin cortar:
        safe["answer"] = full

    return json.dumps(safe, ensure_ascii=False, indent=2)


def chat_fn(message, history):
    session_history = []
    last_user = None
    for m in history:
        if m["role"] == "user":
            last_user = m["content"]
        elif m["role"] == "assistant" and last_user is not None:
            session_history.append({"user": last_user, "assistant": m["content"]})
            last_user = None

    result = crew_runner.kickoff_search(message, session_history=session_history)

    # Texto largo, tal cual lo generó el crew
    full = result.get("final_output") or result.get("results") or ""

    return [
        {"role": "user", "content": message},
        {"role": "assistant", "content": full},   # <- sin JSON alrededor
    ]

# 'query': 'Desde hace 4 años tengo dolor en la  articulación del dedo pulgar de las dos manos (he tenido que dejar de trabajar de masajista) y toda la vida he tenido hiperhidrosis en las manos, pies y axilas. Y de nacimiento escoliosis lumbar pronunciada y a los 27 años tuve ansiedad y ataques de pánico.'
# 'query': 'dolor en la cadera que sube y baja de forma indistinta hacia el brazo derecho y dedo meñique o hacia la rodilla y dedos de los pies'
#'query': 'eccema o picor en las pantorrillas, que luego desaparece y se traslada al dorso de la mano'
# 'query': 'tengo vértigo cuando subo a sitios altos'

def run():
    import gradio as gr

    demo = gr.ChatInterface(
        fn=chat_fn,
        title="Chat Biodescodificación",
        description="Haz preguntas sobre síntomas desde el enfoque de biodescodificación.",
    )
    demo.launch(share=True)

if __name__ == "__main__":
    import gradio as gr

    demo = gr.ChatInterface(
        fn=chat_fn,
        title="Chat Biodescodificación",
        description="Haz preguntas sobre síntomas desde el enfoque de biodescodificación.",
    )
    demo.launch()
