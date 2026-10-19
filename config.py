import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import BaseMessage, AIMessage
from langchain_core.outputs import ChatResult, ChatGeneration

load_dotenv()

class MockLLM(BaseChatModel):
    """LLM de prueba (Mock) robusto compatible con with_structured_output y ejecución offline."""
    
    structured_output_schema: object = None

    def with_structured_output(self, schema):
        """Permite que el Mock devuelva un esquema Pydantic estructurado (Literal) para el Supervisor."""
        new_mock = MockLLM()
        new_mock.structured_output_schema = schema
        return new_mock

    def _generate(self, messages: list[BaseMessage], stop=None, run_manager=None, **kwargs) -> ChatResult:
        # Si el LLM está actuando como Supervisor estructurado
        if self.structured_output_schema:
            has_research = any("Investigación" in str(m.content) or "research_data" in str(m.content) for m in messages)
            has_analysis = any("Análisis" in str(m.content) or "analysis_data" in str(m.content) for m in messages)
            
            # Lógica de ruteo determinística para el Mock del Supervisor
            if not has_research:
                decision = self.structured_output_schema(
                    next_step="Investigador",
                    reasoning="Falta recolectar datos iniciales de investigación."
                )
            elif not has_analysis:
                decision = self.structured_output_schema(
                    next_step="Analista",
                    reasoning="Datos de investigación listos; procede el análisis cuantitativo."
                )
            else:
                decision = self.structured_output_schema(
                    next_step="FINISH",
                    reasoning="Ambos aportes completados exitosamente."
                )
            # Retorna el objeto Pydantic convertido a JSON string para que el nodo lo procese
            text = decision.model_dump_json()
        else:
            # Respuestas estándar para los agentes especialistas (Investigador / Analista)
            last_message = messages[-1].content if messages else ""
            if "investiga" in last_message.lower() or "mercado" in last_message.lower():
                text = "Análisis de mercado simulado: Crecimiento constante en adopción de orquestadores jerárquicos ReAct (2026)."
            elif "analiza" in last_message.lower() or "métricas" in last_message.lower():
                text = "Métricas calculadas: Eficiencia incrementada en +42.5% con margen de error del <2%."
            else:
                text = "Respuesta simulada correctamente por el modo Mock."
            
        message = AIMessage(content=text)
        generation = ChatGeneration(message=message)
        return ChatResult(generations=[generation])

    @property
    def _llm_type(self) -> str:
        return "mock_structured"


def get_llm(temperature: float = 0.0):
    """
    Retorna la instancia de OpenAI.
    Si falta la API Key o falla el proveedor, devuelve un MockLLM inteligente y compatible.
    """
    provider = os.getenv("LLM_PROVIDER", "openai").lower()
    api_key = os.getenv("OPENAI_API_KEY")

    if provider == "openai" and api_key:
        try:
            return ChatOpenAI(
                model="gpt-4o-mini",
                temperature=temperature,
                api_key=api_key,
                max_retries=1
            )
        except Exception as e:
            print(f"⚠️ Error al inicializar OpenAI ({e}). Usando MockLLM como respaldo.")
            return MockLLM()
    
    print("ℹ️ Ejecutando en modo 'Mock' (Simulación estructurada sin consumo de API).")
    return MockLLM()