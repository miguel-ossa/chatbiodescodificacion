#!/usr/bin/env python
import warnings
import gradio as gr
from langdetect import detect
from chatbiodescodificacion.crew import Chatbiodescodificacion

from .utils import *

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

UI_TEXTS = {
    "es": {
        "title": "# 🧬 Chat de Biodescodificación",
        "subtitle": "📚 Diccionario cargado: 2096 entradas",
        "chat_label": "Conversación",
        "input_label": "Tu pregunta",
        "input_placeholder": "Ej: ¿Qué conflictos están relacionados con problemas digestivos?",
        "send": "Enviar",
        "clear": "Limpiar",
        "download": "Descargar respuesta en PDF",
        "file_label": "PDF generado",
        "examples_title": "### 💡 Preguntas de ejemplo",
        "examples": [
            "¿Qué es la biodescodificación?",
            "Desde hace 4 años tengo dolor en la articulación del dedo pulgar de las dos manos (he tenido que dejar de trabajar de masajista) y toda la vida he tenido hiperhidrosis en las manos, pies y axilas. Y de nacimiento escoliosis lumbar pronunciada y a los 27 años tuve ansiedad y ataques de pánico",
            "Sentido biológico de las alergias",
            "Eccema o picor en las pantorrillas, que luego desaparece y se traslada al dorso de la mano",
            "Dolor en la cadera que sube y baja de forma indistinta hacia el brazo derecho y dedo meñique o hacia la rodilla y dedos de los pies",
        ],
        "lang_label": "Idioma de interfaz",
    },
    "zh": {
        "title": "# 🧬 生物解码聊天",
        "subtitle": "📚 字典已加载：2096 条目",
        "chat_label": "对话",
        "input_label": "你的问题",
        "input_placeholder": "例：消化问题与哪些冲突相关？",
        "send": "发送",
        "clear": "清空",
        "download": "下载回复 PDF",
        "file_label": "生成的 PDF",
        "examples_title": "### 💡 示例问题",
        "examples": [
            "什么是生物解码？",
            "我4年来双手拇指关节疼痛（不得不放弃按摩师工作），一生手、脚和腋下多汗，天生腰椎侧弯严重，27岁时出现焦虑和惊恐发作",
            "过敏的生物学意义",
            "小腿胫骨湿疹或瘙痒，后来消失并转移到手背",
            "髋部疼痛不规则地向上或向下转移到右臂和小指，或向下到膝盖和脚趾"
        ],
        "lang_label": "界面语言"
    },
    "en": {
        "title": "# 🧬 Biodecoding Chat",
        "subtitle": "📚 Dictionary loaded: 2096 entries",
        "chat_label": "Conversation",
        "input_label": "Your question",
        "input_placeholder": "E.g.: What conflicts are related to digestive problems?",
        "send": "Send",
        "clear": "Clear",
        "download": "Download answer as PDF",
        "file_label": "Generated PDF",
        "examples_title": "### 💡 Example questions",
        "examples": [
            "What is biodecoding?",
            "For 4 years I have had pain in the thumb joint of both hands (I had to stop working as a masseur) and my whole life I have had hyperhidrosis in my hands, feet and armpits. I was born with pronounced lumbar scoliosis and at 27 I had anxiety and panic attacks.",
            "Biological meaning of allergies",
            "Eczema or itching on the calves that then disappears and moves to the back of the hand",
            "Pain in the hip that goes up and down indistinctly towards the right arm and little finger or towards the knee and toes",
        ],
        "lang_label": "Interface language",
    },
    "pt": {
        "title": "# 🧬 Chat de Biodescodificação",
        "subtitle": "📚 Dicionário carregado: 2096 entradas",
        "chat_label": "Conversa",
        "input_label": "Sua pergunta",
        "input_placeholder": "Ex.: Que conflitos estão relacionados com problemas digestivos?",
        "send": "Enviar",
        "clear": "Limpar",
        "download": "Baixar resposta em PDF",
        "file_label": "PDF gerado",
        "examples_title": "### 💡 Perguntas de exemplo",
        "examples": [
            "O que é biodescodificação?",
            "Há 4 anos tenho dor na articulação do polegar de ambas as mãos (tive que deixar de trabalhar como massagista) e a vida toda tive hiperidrose nas mãos, pés e axilas. Nasci com escoliose lombar acentuada e aos 27 anos tive ansiedade e ataques de pânico.",
            "Sentido biológico das alergias",
            "Eczema ou coceira nas panturrilhas que depois desaparece e se desloca para o dorso da mão",
            "Dor no quadril que sobe e desce de forma indistinta para o braço direito e dedo mínimo ou para o joelho e dedos dos pés",
        ],
        "lang_label": "Idioma da interface",
    },
    "fr": {
        "title": "# 🧬 Chat de Biodécodage",
        "subtitle": "📚 Dictionnaire chargé : 2096 entrées",
        "chat_label": "Conversation",
        "input_label": "Votre question",
        "input_placeholder": "Ex. : Quels conflits sont liés aux problèmes digestifs ?",
        "send": "Envoyer",
        "clear": "Effacer",
        "download": "Télécharger la réponse en PDF",
        "file_label": "PDF généré",
        "examples_title": "### 💡 Questions d’exemple",
        "examples": [
            "Qu’est‑ce que la biodécodage ?",
            "Depuis 4 ans, j’ai mal à l’articulation du pouce des deux mains (j’ai dû arrêter de travailler comme masseur) et j’ai toujours eu de l’hyperhidrose aux mains, aux pieds et aux aisselles. Je suis né avec une scoliose lombaire prononcée et à 27 ans j’ai eu de l’anxiété et des attaques de panique.",
            "Sens biologique des allergies",
            "Eczéma ou démangeaisons aux mollets qui disparaissent puis se déplacent sur le dos de la main",
            "Douleur à la hanche qui monte et descend indistinctement vers le bras droit et l’auriculaire ou vers le genou et les orteils",
        ],
        "lang_label": "Langue de l’interface",
    },
    "de": {
        "title": "# 🧬 Biodekodierungs-Chat",
        "subtitle": "📚 Wörterbuch geladen: 2096 Einträge",
        "chat_label": "Konversation",
        "input_label": "Deine Frage",
        "input_placeholder": "Z. B.: Welche Konflikte stehen mit Verdauungsproblemen in Zusammenhang?",
        "send": "Senden",
        "clear": "Löschen",
        "download": "Antwort als PDF herunterladen",
        "file_label": "Erstelltes PDF",
        "examples_title": "### 💡 Beispielfragen",
        "examples": [
            "Was ist Biodekodierung?",
            "Seit 4 Jahren habe ich Schmerzen im Daumengelenk beider Hände (ich musste aufhören, als Masseur zu arbeiten) und hatte mein ganzes Leben lang Hyperhidrose an Händen, Füßen und Achseln. Ich wurde mit ausgeprägter Lendenwirbelskoliose geboren und hatte mit 27 Angstzustände und Panikattacken.",
            "Biologischer Sinn von Allergien",
            "Ekzem oder Juckreiz an den Waden, das dann verschwindet und auf den Handrücken wandert",
            "Schmerzen in der Hüfte, die unbestimmt in den rechten Arm und den kleinen Finger oder ins Knie und in die Zehen ausstrahlen",
        ],
        "lang_label": "Interface-Sprache",
    },
}

# Registrar la fuente al inicio
registrar_fuente_unicode()

crew_runner = Chatbiodescodificacion()

def get_texts(lang: str):
    if lang == "auto":
        return UI_TEXTS["es"]
    return UI_TEXTS.get(lang, UI_TEXTS["es"])

def detectar_idioma(texto: str) -> str:
    try:
        lang = detect(texto)
    except Exception:
        lang = "es"
    return lang

def limpiar_fn():
    return (
        [],                     # chat
        "",                     # last_answer
        False,                  # descarga_activa
        gr.update(interactive=False),  # deshabilitar botón descarga
        gr.update(visible=False),      # ocultar archivo
    )

def descargar_pdf_fn(last_answer: str):
    if not last_answer:
        return gr.File(visible=False)
    pdf_path = generar_pdf_con_pandoc(last_answer)
    return gr.File(value=pdf_path, visible=True)

def chat_fn(message, history, last_answer):
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

    # Lógica de idioma: auto = detectar, si no usar el seleccionado

    user_lang = detectar_idioma(message)

    result = crew_runner.kickoff_search(
        message,
        user_lang=user_lang,
        session_history=session_history
    )

    full = result.get("final_output") or result.get("results") or ""

    # NORMALIZAR INMEDIATAMENTE DESPUÉS DE OBTENER EL RESULTADO
    full = normalizar_simbolos_global(full)

    # Añadimos los dos mensajes al history
    history = history + [
        {"role": "user", "content": message},
        {"role": "assistant", "content": full},
    ]

    # actualizamos last_answer con la última respuesta
    last_answer = full

    descarga_activa = bool(full)
    return (
        "",
        history,
        last_answer,
        descarga_activa,
        gr.update(interactive=descarga_activa),
    )

def crear_interfaz():
    with gr.Blocks(title="Chat Biodescodificación") as interfaz:
        current_lang = gr.State("auto")
        last_answer = gr.State("")
        descarga_activa = gr.State(False)

        title_md = gr.Markdown()
        subtitle_md = gr.Markdown()

        idioma = gr.Dropdown(
            label="Idioma de interfaz",
            choices=["auto", "es", "zh", "pt", "en", "fr", "de"],
            value="auto",
        )

        chat = gr.Chatbot(
            label="Conversación",
            height=400,
        )

        mensaje = gr.Textbox(
            label="Tu pregunta",
            placeholder="Ej: ¿Qué conflictos están relacionados con problemas digestivos?",
            scale=4,
        )

        with gr.Row():
            boton_enviar = gr.Button("Enviar", variant="primary", scale=1)
            boton_limpiar = gr.Button("Limpiar", variant="secondary", scale=1)

        with gr.Row():
            boton_descargar = gr.Button(
                "Descargar respuesta en PDF",
                variant="secondary",
                interactive=False  # ← deshabilitado inicialmente
            )
            archivo_pdf = gr.File(label="PDF generado", visible=False)

        examples_title = gr.Markdown("### 💡 Preguntas de ejemplo")
        examples_list = gr.Markdown()  # lista traducida

        # gr.Examples fijo, que proporciona los chips clicables (en español)
        gr.Examples(
            examples=UI_TEXTS["es"]["examples"],
            inputs=mensaje,
        )

        def actualizar_ui(lang):
            texts = get_texts(lang)
            return (
                texts["title"],  # title_md
                texts["subtitle"],  # subtitle_md
                gr.Dropdown(  # idioma
                    label=texts["lang_label"],
                    choices=["auto", "es", "zh", "pt", "en", "fr", "de"],
                    value=lang,
                ),
                gr.Textbox(  # mensaje
                    label=texts["input_label"],
                    placeholder=texts["input_placeholder"],
                    scale=4,
                ),
                gr.Button(  # boton_enviar
                    value=texts["send"],
                    variant="primary",
                    scale=1,
                ),
                gr.Button(  # boton_limpiar
                    value=texts["clear"],
                    variant="secondary",
                    scale=1,
                ),
                texts["examples_title"],  # examples_title
                ejemplos_markdown(texts["examples"]),  # examples_list (visible traducido)
                lang,  # current_lang
                gr.update(
                    value=texts["download"]
                ),
                gr.File(  # archivo_pdf (solo cambia el label)
                    label=texts["file_label"],
                    visible=False,
                ),
            )

        idioma.change(
            fn=actualizar_ui,
            inputs=[idioma],
            outputs=[
                title_md,
                subtitle_md,
                idioma,
                mensaje,
                boton_enviar,
                boton_limpiar,
                examples_title,
                examples_list,
                current_lang,
                boton_descargar,
                archivo_pdf,
            ],
        )

        interfaz.load(
            fn=actualizar_ui,
            inputs=[idioma],
            outputs=[
                title_md,
                subtitle_md,
                idioma,
                mensaje,
                boton_enviar,
                boton_limpiar,
                examples_title,
                examples_list,
                current_lang,
                boton_descargar,
                archivo_pdf,
            ],
        )

        boton_enviar.click(
            fn=chat_fn,
            inputs=[mensaje, chat, last_answer],
            outputs=[mensaje, chat, last_answer, descarga_activa, boton_descargar],
        )

        mensaje.submit(
            fn=chat_fn,
            inputs=[mensaje, chat, last_answer],
            outputs=[mensaje, chat, last_answer, descarga_activa, boton_descargar],
        )

        boton_limpiar.click(
            fn=limpiar_fn,
            outputs=[chat, last_answer, descarga_activa, boton_descargar, archivo_pdf],
        )

        boton_descargar.click(
            fn=descargar_pdf_fn,
            inputs=[last_answer],
            outputs=[archivo_pdf],
        )

    return interfaz

def run():
    demo = crear_interfaz()
    demo.launch(server_name="0.0.0.0", server_port=7860, share=True)

if __name__ == "__main__":
    demo = crear_interfaz()
    demo.launch(server_name="0.0.0.0", server_port=7860, share=True)
