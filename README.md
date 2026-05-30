# 🧬 ChatBiodescodificación

AI-powered chat to decode the biological meaning behind physical symptoms using biodecoding — a multi-agent CrewAI system over a 2096-entry knowledge base.

**ChatBiodescodificación** is an interactive AI chat that interprets physical symptoms through the lens of biodecoding (biopsychology). It uses a CrewAI multi-agent pipeline — query analysis, dictionary search, semantic scoring, context management, and quality validation — running over a 2096-entry biodecoding thesaurus.

## Tech Stack

- **CrewAI** — multi-agent orchestration (7 specialized agents)
- **Gradio** — web UI with i18n (ES, EN, FR, DE, PT, ZH)
- **Ollama / Cloud LLMs** — configurable LLM backend (local or remote)
- **Docker** — one-command self-hosted deployment

## Quick Start

```bash
# Docker (recommended)
./start_docker.sh

# Or local
python -m chatbiodescodificacion.main
```

UI available at `http://localhost:7860`.

## Funcionalidades del Chat de Biodescodificación

### Funcionalidades Principales

#### 1. Consulta de Síntomas y Condiciones de Salud
- **Búsqueda de síntomas**: Puedes preguntar sobre cualquier síntoma o condición física que estés experimentando
- **Análisis de patrones**: El sistema interpreta tu consulta para encontrar conexiones biológicas relevantes
- **Consultas específicas**: Puedes hacer preguntas como "¿Qué conflictos están relacionados con problemas digestivos?" o "Sentido biológico de las alergias"

#### 2. Exploración del Diccionario de Biodescodificación
- **Acceso a 2096 entradas**: El diccionario contiene una amplia base de conocimiento sobre biodescodificación
- **Búsqueda por término**: Encuentra información sobre cualquier término biológico o concepto
- **Relaciones cruzadas**: Descubre conexiones entre diferentes conceptos y síntomas

#### 3. Respuestas Detalladas y Personalizadas
- **Explicaciones biológicas**: Cada respuesta incluye el sentido biológico detrás de los síntomas
- **Conflictos emocionales**: Se relacionan los síntomas con posibles conflictos emocionales subyacentes
- **Contexto completo**: Se proporciona información contextual sobre cada concepto

#### 4. Interfaz Intuitiva
- **Chat conversacional**: Interfaz de chat simple y fácil de usar
- **Historial de conversación**: Mantiene el contexto de la conversación
- **Limpieza de historial**: Opción para comenzar una nueva conversación
- **Cambio de idioma**: Interfaz traducida al español (es), chino (zh), portugués (pt), inglés (en), francés (fr) y alemán (de)
- **Consulta en cualquier idioma**: Puedes hacer consultas en cualquier otro idioma

## Ejemplos de Consultas
- "Desde hace 4 años tengo dolor en la articulación del dedo pulgar de las dos manos..."
- "Dolor en la cadera que sube y baja de forma indistinta hacia el brazo derecho..."
- "Eccema o picor en las pantorrillas, que luego desaparece y se traslada al dorso de la mano"
- "Tengo vértigo cuando subo a sitios altos"

## Beneficios para el Usuario
- **Entendimiento profundo**: Comprende el significado biológico detrás de tus síntomas
- **Conexión emocional**: Descubre posibles conflictos emocionales relacionados
- **Acceso rápido**: Información disponible de forma inmediata y fácil de entender
- **Herramienta educativa**: Aprende sobre biodescodificación de manera interactiva

## ¿Qué puedes hacer con esta aplicación?
1. Consultar cualquier síntoma o condición de salud
2. Explorar conceptos biológicos del método de biodescodificación
3. Entender las conexiones entre síntomas y conflictos emocionales
4. Obtener explicaciones detalladas basadas en una base de conocimiento extensa
5. Descargar un archivo PDF con el resultado de tu consulta

Ideal para personas interesadas en biodescodificación, terapeutas, profesionales de la salud y cualquier persona que desee comprender mejor el significado biológico de sus síntomas.
