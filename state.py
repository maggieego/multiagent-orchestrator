from typing import TypedDict, Annotated, Optional, List
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages

class TeamState(TypedDict):
    # Historial de conversación
    messages: Annotated[List[BaseMessage], add_messages]
    
    # Próximo agente a intervenir
    next_agent: str
    
    # Resultados específicos de cada especialista
    research_data: Optional[str]
    analysis_data: Optional[str]
    
    # Contador de iteraciones para evitar el "Supervisor Infinito"
    step_count: int
    
    # Respuesta final condensada
    final_response: Optional[str]