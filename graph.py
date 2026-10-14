from typing import Literal
from pydantic import BaseModel, Field
from langchain_core.messages import SystemMessage, HumanMessage
from langgraph.graph import StateGraph, START, END

from state import TeamState
from config import get_llm
from agents.research_agent import research_node
from agents.analyst_agent import analyst_node

# Esquema para forzar al LLM a elegir una opción válida
class RouterSchema(BaseModel):
    next_step: Literal["Investigador", "Analista", "FINISH"] = Field(
        description="El próximo agente que debe actuar o FINISH si la tarea está completada con ambos aportes."
    )
    reasoning: str = Field(description="Explicación breve de por qué se toma esta decisión.")

def supervisor_node(state: TeamState) -> dict:
    """Nodo Supervisor: Determina la ruta del flujo basándose en el estado actual y un límite de pasos."""
    step_count = state.get("step_count", 0)
    
    # 🛑 Prevención de "Supervisor Infinito"
    if step_count >= 5:
        return {"next_agent": "FINISH"}

    llm = get_llm(temperature=0.0)

    # Evaluación directa por lógica de estado para máxima robustez
    has_research = bool(state.get("research_data"))
    has_analysis = bool(state.get("analysis_data"))

    if not has_research:
        next_step = "Investigador"
    elif not has_analysis:
        next_step = "Analista"
    else:
        next_step = "FINISH"

    return {"next_agent": next_step}


def route_decision(state: TeamState) -> str:
    """Función de arista condicional que lee el estado y retorna el nombre del nodo objetivo."""
    return state["next_agent"]


def build_graph() -> StateGraph:
    """Construye y compila el grafo jerárquico."""
    builder = StateGraph(TeamState)

    # 1. Agregar Nodos
    builder.add_node("Supervisor", supervisor_node)
    builder.add_node("Investigador", research_node)
    builder.add_node("Analista", analyst_node)

    # 2. Definir Punto de Entrada
    builder.set_entry_point("Supervisor")

    # 3. Aristas Condicionales desde el Supervisor
    builder.add_conditional_edges(
        "Supervisor",
        route_decision,
        {
            "Investigador": "Investigador",
            "Analista": "Analista",
            "FINISH": END
        }
    )

    # 4. Retorno de los especialistas al Supervisor
    builder.add_edge("Investigador", "Supervisor")
    builder.add_edge("Analista", "Supervisor")

    return builder.compile()