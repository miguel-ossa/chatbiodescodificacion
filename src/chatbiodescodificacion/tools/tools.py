"""
Tools for the BioDescDiccionario CrewAI agents
"""

from crewai.tools import BaseTool
from typing import List, Dict, Any
import os
import json
import unicodedata
from chatbiodescodificacion.config import ENTRADAS_JSON

def normalize(text: str) -> str:
    """Pasa a minúsculas y elimina tildes/diacríticos."""
    text = text.lower()
    text = unicodedata.normalize("NFD", text)
    return "".join(c for c in text if unicodedata.category(c) != "Mn")


class TextAnalyzerTool(BaseTool):
    """Analiza el texto para extraer términos clave y contexto para las queries"""
    name: str = "Text Analyzer"
    description: str = "Analyzes text to extract key terms, context, and intent for biodescodification queries"

    def _run(self, query: str) -> str:
        # Simple text analysis - in a real implementation this would use NLP libraries
        return f"Analyzed query: '{query}' - Extracted key terms and context"

class BiodescodificationThesaurusTool(BaseTool):
    """Provee sinónimos y términos relacionados para los conceptos en biodescodificación"""
    name: str = "Biodescodification Thesaurus"
    description: str = "Provides synonyms and related terms for biodescodification concepts"

    def _run(self, query: str) -> str:
        # In a real implementation, this would access a thesaurus database
        return f"Synonyms and related terms for: '{query}'"

class DictionarySearchTool(BaseTool):
    """Busca entradas en el diccionario JSON"""
    name: str = "dictionary_search"
    description: str = "Busca entradas en el diccionario JSON procesado por el campo 'termino'."

    def _run(self, query: str) -> str:
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        json_path = os.path.join(base_dir, ENTRADAS_JSON)

        with open(json_path, "r", encoding="utf-8") as f:
            entradas = json.load(f)

        q = normalize(query.strip())
        resultados_exactos = []
        resultados_parciales = []
        resultados_contexto = []

        for entrada in entradas:
            termino_norm = normalize(str(entrada.get("termino", "")))

            if termino_norm == q:
                resultados_exactos.append(entrada)
                continue

            if q in termino_norm:
                resultados_parciales.append(entrada)
                continue

            texto_contexto = normalize(" ".join([
                str(entrada.get("definicion", "")),
                str(entrada.get("tecnico", "")),
                str(entrada.get("sentido_biologico", "")),
                str(entrada.get("conflicto", "")),
                " ".join(entrada.get("referencias_cruzadas", [])),
            ]))

            if q in texto_contexto:
                resultados_contexto.append(entrada)

        resultados = resultados_exactos + resultados_parciales + resultados_contexto
        resultados = resultados[:5]

        if not resultados:
            return "No se encontraron entradas relevantes en el diccionario para esta consulta."

        partes = []
        for entrada in resultados:
            partes.append(
                f"Entrada: {entrada.get('termino','(sin título)')}\n"
                f"Definición: {entrada.get('definicion','')}\n"
                f"Técnico: {entrada.get('tecnico','')}\n"
                f"Sentido biológico: {entrada.get('sentido_biologico','')}\n"
                f"Conflicto: {entrada.get('conflicto','')}\n"
                f"Referencias cruzadas: {', '.join(entrada.get('referencias_cruzadas', []))}\n"
                "----"
            )

        return "\n\n".join(partes)

class VectorDatabaseTool(BaseTool):
    """Ejecuta búsquedas semánticas usando vector embeddings"""
    name: str = "Vector Database Search"
    description: str = "Performs semantic similarity searches using vector embeddings"

    def _run(self, query: str) -> str:
        return f"Vector search for: '{query}'"

class FuzzyMatcherTool(BaseTool):
    """Coteja entradas con ligeras variaciones o typos"""
    name: str = "Fuzzy Matcher"
    description: str = "Matches entries with slight variations or typos"

    def _run(self, query: str) -> str:
        return f"Fuzzy matching for: '{query}'"

class RankingAlgorithmTool(BaseTool):
    """Puntúa resultados de búsqueda basándose en factores relevanes"""
    name: str = "ranking_algorithm"
    description: str = "Ranks search results based on relevance factors"

    def _run(self, query: str, results: List[str]) -> List[str]:
        return results

class SemanticScoringTool(BaseTool):
    """Puntúa resultados basados en similitud semántica"""
    name: str = "semantic_scoring"
    description: str = "Scores results based on semantic similarity"

    def _run(self, query: str, results: List[str]) -> List[str]:
        # De momento, solo devuelve tal cual; luego añades lógica de ranking
        return results

class ContextAnalyzerTool(BaseTool):
    """Analiza el contexto para una relevancia de resultados mejorada"""
    name: str = "context_analyzer"
    description: str = "Analyzes context for better result relevance"

    def _run(self, query: str, results: List[str]) -> str:
        return f"Context analysis for: '{query}'"

class ThesaurusTool(BaseTool):
    """Expande las queries con sinónimos y términos relacionados"""
    name: str = "Thesaurus"
    description: str = "Expands queries with synonyms and related terms"

    def _run(self, query: str) -> str:
        return f"Expanding query with synonyms: '{query}'"

class WordEmbeddingTool(BaseTool):
    """Usa word embeddings para expansión semántica"""
    name: str = "Word Embedding"
    description: str = "Uses word embeddings for semantic expansion"

    def _run(self, query: str) -> str:
        return f"Word embedding analysis for: '{query}'"

class DomainVocabularyTool(BaseTool):
    """Proporciona expansión de vocabulario de dominio específico"""
    name: str = "Domain Vocabulary"
    description: str = "Provides domain-specific vocabulary expansion"

    def _run(self, query: str) -> str:
        return f"Domain vocabulary expansion for: '{query}'"

class MemoryRetrievalTool(BaseTool):
    """Recupera la historia y el contexto de la sesión"""
    name: str = "Memory Retrieval"
    description: str = "Retrieves session history and context"

    def _run(self, session_id: str) -> str:
        return f"Retrieving session history for: '{session_id}'"

class ConversationTrackerTool(BaseTool):
    """Realiza un seguimiento de los patrones de conversación y las preferencias de los usuarios."""
    name: str = "conversation_tracker"
    description: str = "Tracks conversation patterns and user preferences"

    def _run(self, session_history: List[str]) -> str:
        return f"Tracking conversation patterns: {len(session_history)} items"


class PersonalizationTool(BaseTool):
    """Adapta búsquedas basadas en la preferencia y la historia del usuario"""
    name: str = "Personalization"
    description: str = "Adapts search based on user preferences and history"

    def _run(self, user_preferences: str) -> str:
        return f"Personalizing search based on: {user_preferences}"

class ConsistencyCheckerTool(BaseTool):
    """Cheque la consistencia de los resultados de la búsqueda"""
    name: str = "consistency_checker"
    description: str = "Checks consistency of search results"

    def _run(self, query: str, results: List[str]) -> List[str]:
        # De momento, solo devuelve tal cual; luego añades lógica de ranking
        return results

class AccuracyValidatorTool(BaseTool):
    """Valida la exactitud de los resultados de búsqueda"""
    name: str = "accuracy_validator"
    description: str = "Validates accuracy of search results"

    def _run(self, query: str, results: List[str]) -> List[str]:
        # De momento, solo devuelve tal cual; luego añades lógica de ranking
        return results

class QualityAssuranceTool(BaseTool):
    """Asegura la calidad general de los resultados de búsqueda"""
    name: str = "quality_assurance"
    description: str = "Ensures overall quality of search results"

    def _run(self, query: str, results: List[str]) -> List[str]:
        # De momento, solo devuelve tal cual; luego añades lógica de ranking
        return results