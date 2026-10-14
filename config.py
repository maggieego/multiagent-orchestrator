import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import BaseMessage, AIMessage
from langchain_core.outputs import ChatResult, ChatGeneration

load_dotenv()

class MockLLM(BaseChatModel):
    """LLM de prueba (Mock) que simula respuestas cuando no hay créditos de OpenAI."""
    
    def _generate(self, messages: list[BaseMessage], stop=None, run_manager=None, **kwargs) -> ChatResult:
        # Genera una respuesta simulada basada en el contexto del mensaje
        last_message = messages[-1].content if messages else ""
        
        if "investiga" in last_message.lower() or "mercado" in last_message.lower():
            text = "Análisis de mercado simulado: Crecimiento constante en adopción de orquestadores jerárquicos (2026)."
        elif "analiza" in last_message.lower() or "métricas" in last_message.lower():
            text = "Métricas calculadas: Eficiencia incrementada en +42.5% con margen de error del <2%."
        else:
            text = "Respuesta simulada correctamente por el modo Mock."
            
        message = AIMessage(content=text)
        generation = ChatGeneration(message=message)
        return ChatResult(generations=[generation])

    @property
    def _llm_type(self) -> str:
        return "mock"


def get_llm(temperature: float = 0.0):
    """
    Retorna la instancia de OpenAI.
    Si falta la API Key o falla el proveedor, devuelve un MockLLM transparente.
    """
    provider = os.getenv("LLM_PROVIDER", "openai").lower()
    api_key = os.getenv("OPENAI_API_KEY")

    if provider == "openai" and api_key:
        try:
            return ChatOpenAI(
                model="gpt-4o-mini",
                temperature=temperature,
                api_key=api_key,
                max_retries=1 # Evita esperas largas si la cuenta no tiene saldo
            )
        except Exception as e:
            print(f"⚠️ Error al inicializar OpenAI ({e}). Usando MockLLM como respaldo.")
            return MockLLM()
    
    # Si LLM_PROVIDER es 'mock' o no hay API Key de OpenAI
    print("ℹ️ Ejecutando en modo 'Mock' (Simulación sin consumo de API).")
    return MockLLM()