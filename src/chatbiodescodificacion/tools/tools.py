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
    name: str = "Text Analyzer"
    description: str = "Analyzes text to extract key terms, context, and intent for biodescodification queries"

    def _run(self, query: str) -> str:
        # Simple text analysis - in a real implementation this would use NLP libraries
        return f"Analyzed query: '{query}' - Extracted key terms and context"

class BiodescodificationThesaurusTool(BaseTool):
    name: str = "Biodescodification Thesaurus"
    description: str = "Provides synonyms and related terms for biodescodification concepts"

    def _run(self, query: str) -> str:
        # In a real implementation, this would access a thesaurus database
        return f"Synonyms and related terms for: '{query}'"

class DictionarySearchTool(BaseTool):
    name: str = "dictionary_search"
    description: str = "Busca entradas en el diccionario JSON procesado por el campo 'termino'."

    def _run(self, query: str) -> str:
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        json_path = os.path.join(base_dir, ENTRADAS_JSON)

        with open(json_path, "r", encoding="utf-8") as f:
            entradas = json.load(f)

        q = normalize(query.strip())
        resultados_exactos: List[Dict[str, Any]] = []
        resultados_parciales: List[Dict[str, Any]] = []
        resultados_contexto: List[Dict[str, Any]] = []

        for entrada in entradas:
            termino_norm = normalize(str(entrada.get("termino", "")))

            # 1) Coincidencia exacta en 'termino'
            if termino_norm == q:
                resultados_exactos.append(entrada)
                continue

            # 2) Coincidencia parcial en 'termino'
            if q in termino_norm:
                resultados_parciales.append(entrada)
                continue

            # 3) (Opcional) búsqueda laxa en otros campos
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
        # Devuelve texto formateado, no la lista cruda
        return json.dumps(resultados[:5], ensure_ascii=False)

class VectorDatabaseTool(BaseTool):
    name: str = "Vector Database Search"
    description: str = "Performs semantic similarity searches using vector embeddings"

    def _run(self, query: str) -> str:
        return f"Vector search for: '{query}'"

class FuzzyMatcherTool(BaseTool):
    name: str = "Fuzzy Matcher"
    description: str = "Matches entries with slight variations or typos"

    def _run(self, query: str) -> str:
        return f"Fuzzy matching for: '{query}'"

class RankingAlgorithmTool(BaseTool):
    name: str = "ranking_algorithm"
    description: str = "Ranks search results based on relevance factors"

    def _run(self, query: str, results: List[str]) -> List[str]:
        return results

class SemanticScoringTool(BaseTool):
    name: str = "semantic_scoring"
    description: str = "Scores results based on semantic similarity"

    def _run(self, query: str, results: List[str]) -> List[str]:
        # De momento, solo devuelve tal cual; luego añades lógica de ranking
        return results

class ContextAnalyzerTool(BaseTool):
    name: str = "context_analyzer"
    description: str = "Analyzes context for better result relevance"

    def _run(self, query: str, results: List[str]) -> str:
        return f"Context analysis for: '{query}'"

class ThesaurusTool(BaseTool):
    name: str = "Thesaurus"
    description: str = "Expands queries with synonyms and related terms"

    def _run(self, query: str) -> str:
        return f"Expanding query with synonyms: '{query}'"

class WordEmbeddingTool(BaseTool):
    name: str = "Word Embedding"
    description: str = "Uses word embeddings for semantic expansion"

    def _run(self, query: str) -> str:
        return f"Word embedding analysis for: '{query}'"

class DomainVocabularyTool(BaseTool):
    name: str = "Domain Vocabulary"
    description: str = "Provides domain-specific vocabulary expansion"

    def _run(self, query: str) -> str:
        return f"Domain vocabulary expansion for: '{query}'"

class MemoryRetrievalTool(BaseTool):
    name: str = "Memory Retrieval"
    description: str = "Retrieves session history and context"

    def _run(self, session_id: str) -> str:
        return f"Retrieving session history for: '{session_id}'"

class ConversationTrackerTool(BaseTool):
    name: str = "conversation_tracker"
    description: str = "Tracks conversation patterns and user preferences"

    def _run(self, session_history: List[str]) -> str:
        return f"Tracking conversation patterns: {len(session_history)} items"


class PersonalizationTool(BaseTool):
    name: str = "Personalization"
    description: str = "Adapts search based on user preferences and history"

    def _run(self, user_preferences: str) -> str:
        return f"Personalizing search based on: {user_preferences}"

class ConsistencyCheckerTool(BaseTool):
    name: str = "consistency_checker"
    description: str = "Checks consistency of search results"

    def _run(self, query: str, results: List[str]) -> List[str]:
        # De momento, solo devuelve tal cual; luego añades lógica de ranking
        return results

class AccuracyValidatorTool(BaseTool):
    name: str = "accuracy_validator"
    description: str = "Validates accuracy of search results"

    def _run(self, query: str, results: List[str]) -> List[str]:
        # De momento, solo devuelve tal cual; luego añades lógica de ranking
        return results

class QualityAssuranceTool(BaseTool):
    name: str = "quality_assurance"
    description: str = "Ensures overall quality of search results"

    def _run(self, query: str, results: List[str]) -> List[str]:
        # De momento, solo devuelve tal cual; luego añades lógica de ranking
        return results