from typing import TypedDict, Annotated, Optional, List
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages
from pydantic import BaseModel, Field, Literal

# Importamos o redefinimos el esquema del enrutador para el tipado estricto
class RouterSchema(BaseModel):
    next_step: Literal["Investigador", "Analista", "FINISH"] = Field(
        description="El próximo agente que debe actuar ('Investigador', 'Analista') o 'FINISH' si la tarea está completada."
    )
    reasoning: str = Field(description="Explicación breve de por qué se toma esta decisión de ruteo.")


class TeamState(TypedDict):
    # Historial de conversación
    messages: Annotated[List[BaseMessage], add_messages]
    
    # Decisión estructurada del Supervisor (reemplaza al antiguo next_agent plano)
    supervisor_decision: Optional[RouterSchema]
    
    # Resultados específicos de cada especialista para aislamiento de contexto
    research_data: Optional[str]
    analysis_data: Optional[str]
    
    # Contador de iteraciones para evitar el "Supervisor Infinito"
    step_count: int