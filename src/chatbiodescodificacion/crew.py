from crewai import Agent, Task, Crew, Process
from crewai.project import CrewBase, agent, task, crew
from crewai import LLM
from dotenv import load_dotenv

from .utils import *

# Import the tools to make them available
from .tools.tools import (
    TextAnalyzerTool,
    BiodescodificationThesaurusTool,
    DictionarySearchTool,
    RankingAlgorithmTool,
    SemanticScoringTool,
    ContextAnalyzerTool,
    ThesaurusTool,
    WordEmbeddingTool,
    DomainVocabularyTool,
    MemoryRetrievalTool,
    ConversationTrackerTool,
    PersonalizationTool,
    ConsistencyCheckerTool,
    AccuracyValidatorTool,
    QualityAssuranceTool
)

load_dotenv(override=True)
# Get the Ollama host from environment
OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")

# Create a custom function to get the LLM with Ollama settings
def get_ollama_llm():
    print("OLLAMA_HOST =", OLLAMA_HOST)
    return LLM(
        model="gpt-oss:120b-cloud",        # el nombre del modelo en Ollama
        base_url=f"{OLLAMA_HOST}/v1",  # endpoint OpenAI-compatible de Ollama
        api_key="ollama",          # valor dummy, Ollama no lo valida
        provider="openai",         # o explícitamente "openai" para la API-compatible
        # o bien: provider="custom" en versiones nuevas, según docs
    )

default_llm = "gpt-oss:120b-cloud"

# usa un directorio seguro dentro del contenedor
os.environ["CREWAI_STORAGE_PATH"] = "/tmp/.crewai"


def strip_large_json_blocks(text: str, max_len: int = 8000) -> str:
    # elimina bloques ```json``` demasiado largos
    def repl(match):
        block = match.group(0)
        if len(block) > max_len:
            return "```json\n{...bloque JSON omitido por ser demasiado largo...}\n```"
        return block

    return re.sub(r"```json[\s\S]*?```", repl, text)


@CrewBase
class Chatbiodescodificacion():
    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    @agent
    def query_analyzer(self) -> Agent:
        return Agent(
            config=self.agents_config['query_analyzer'],
            tools=[TextAnalyzerTool(), BiodescodificationThesaurusTool()],
            llm=get_ollama_llm()
        )

    @agent
    def dictionary_navigator(self) -> Agent:
        return Agent(
            config=self.agents_config['dictionary_navigator'],
            #tools=[DictionarySearchTool(), VectorDatabaseTool(), FuzzyMatcherTool()]
            tools=[DictionarySearchTool()],
            llm=get_ollama_llm()
        )

    @agent
    def relevance_scorer(self) -> Agent:
        return Agent(
            config=self.agents_config['relevance_scorer'],
            tools=[RankingAlgorithmTool(), SemanticScoringTool(), ContextAnalyzerTool()],
            llm=get_ollama_llm()
        )

    @agent
    def synonym_expander(self) -> Agent:
        return Agent(
            config=self.agents_config['synonym_expander'],
            tools=[ThesaurusTool(), WordEmbeddingTool(), DomainVocabularyTool()],
            llm=get_ollama_llm()
        )

    @agent
    def context_manager(self) -> Agent:
        return Agent(
            config=self.agents_config['context_manager'],
            tools=[MemoryRetrievalTool(), ConversationTrackerTool(), PersonalizationTool()],
            llm=get_ollama_llm()
        )

    @agent
    def validator(self) -> Agent:
        return Agent(
            config=self.agents_config['validator'],
            tools=[ConsistencyCheckerTool(), AccuracyValidatorTool(), QualityAssuranceTool()],
            llm=get_ollama_llm()
        )

    @agent
    def explainer(self) -> Agent:
        return Agent(
            config=self.agents_config['explainer'],
            tools=[],  # de momento no necesita tools extra
            llm=get_ollama_llm()
        )

    @agent
    def markdown_validator(self) -> Agent:
        return Agent(
            config=self.agents_config['markdown_validator'],
            tools=[],  # de momento no necesita tools extra
            llm=get_ollama_llm()
        )

    @task
    def analyze_query_task(self) -> Task:
        return Task(config=self.tasks_config['analyze_query'])

    @task
    def search_dictionary_task(self) -> Task:
        return Task(config=self.tasks_config['search_dictionary'])

    @task
    def markdown_validate_task(self) -> Task:
        return Task(config=self.tasks_config['markdown_validate'])

    # @task
    # def score_relevance_task(self) -> Task:
    #     return Task(config=self.tasks_config['score_relevance'])
    #
    # @task
    # def expand_query_task(self) -> Task:
    #     return Task(config=self.tasks_config['expand_query'])
    #
    # @task
    # def adapt_context_task(self) -> Task:
    #     return Task(config=self.tasks_config['adapt_context'])
    #
    # @task
    # def validate_results_task(self) -> Task:
    #     return Task(config=self.tasks_config['validate_results'])

    @task
    def generate_answer_task(self) -> Task:
        return Task(config=self.tasks_config['generate_answer'])

    @crew
    def crew(self) -> Crew:
        """Creates the BioDescDiccionario search enhancement crew"""
        return Crew(
            agents=[
                self.query_analyzer(),
                self.dictionary_navigator(),
                self.relevance_scorer(),
                self.synonym_expander(),
                self.context_manager(),
                self.validator(),
                self.explainer(),
                self.markdown_validator(),
            ],
            tasks=[
                self.analyze_query_task(),
                self.search_dictionary_task(),
                # self.score_relevance_task(),
                # self.expand_query_task(),
                # self.adapt_context_task(),
                # self.validate_results_task(),
                self.generate_answer_task(),
                self.markdown_validate_task(),
            ],
            process=Process.sequential,
            verbose=True,
            #planning=True,
            #planning_llm=default_llm
        )

    def kickoff_search(self, query: str,  user_lang: str, session_history: list = None, ) -> dict:
        """
        Execute the search enhancement crew with the given query

        Args:
            query (str): The user's search query
            session_history (list): Previous queries in the session

        Returns:
            dict: Enhanced search results
        """
        # Prepare inputs for the crew
        inputs = {
            "query": query,
            "user_lang": user_lang,
            "session_history": session_history or [],
        }

        # Execute the crew
        result = self.crew().kickoff(inputs=inputs)
        raw = result.raw
        cleaned = strip_large_json_blocks(raw)
        cleaned = normalizar_simbolos_global(cleaned)
        cleaned = limpiar_viñetas_huerfanas(cleaned)
        # Parse and return results
        try:
            # The result is a CrewResult object, we need to extract the final output
            return {
                "query": query,
                "session_history": session_history,
                "results": result.raw,
                "final_output": cleaned
            }
        except Exception as e:
            return {
                "query": query,
                "session_history": session_history,
                "error": str(e),
                "results": result.raw if 'result' in locals() else "No results"
            }

# Test that we can at least import this
if __name__ == "__main__":
    print("Testing basic import...")
    try:
        crew = Chatbiodescodificacion()
        print("Import successful!")
    except Exception as e:
        print(f"Import failed: {e}")