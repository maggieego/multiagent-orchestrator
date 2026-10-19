from typing import Literal
from pydantic import BaseModel, Field
from langchain_core.messages import HumanMessage
from langgraph.graph import StateGraph, START, END

from state import TeamState
from config import get_llm
from agents.research_agent import research_node
from agents.analyst_agent import analyst_node

# 1. Esquema estricto con Literal para forzar la salida estructurada
class RouterSchema(BaseModel):
    next_step: Literal["Investigador", "Analista", "FINISH"] = Field(
        description="El próximo agente que debe actuar ('Investigador', 'Analista') o 'FINISH' si la tarea está completada con ambos aportes."
    )
    reasoning: str = Field(description="Explicación breve de por qué se toma esta decisión.")

def supervisor_node(state: TeamState) -> dict:
    """Nodo Supervisor: Utiliza with_structured_output y RouterSchema para decidir el flujo de forma inteligente."""
    step_count = state.get("step_count", 0)
    
    # 🛑 Prevención de "Supervisor Infinito" por límite de pasos
    if step_count >= 5:
        return {
            "supervisor_decision": RouterSchema(
                next_step="FINISH",
                reasoning="Límite máximo de iteraciones alcanzado (seguridad contra bucles)."
            ),
            "next_agent": "FINISH"
        }

    llm = get_llm(temperature=0.0)

    # Estado actual de los artefactos en el flujo
    has_research = bool(state.get("research_data"))
    has_analysis = bool(state.get("analysis_data"))

    prompt = (
        "Eres el Supervisor Jerárquico de un sistema multi-agente.\n"
        f"Estado actual de la tarea:\n"
        f"- Investigación completada: {has_research}\n"
        f"- Análisis completado: {has_analysis}\n\n"
        "Reglas de decisión:\n"
        "1. Si no hay investigación, tu next_step debe ser 'Investigador'.\n"
        "2. Si hay investigación pero falta análisis, tu next_step debe ser 'Analista'.\n"
        "3. Si ambos están completos, tu next_step debe ser 'FINISH'."
    )

    try:
        # Vinculación de salida estructurada solicitada por el docente
        structured_llm = llm.with_structured_output(RouterSchema)
        decision: RouterSchema = structured_llm.invoke([HumanMessage(content=prompt)])
    except Exception as e:
        # Fallback determinístico seguro si no hay credenciales activas o falla la API
        print(f"⚠️ [Supervisor] Usando fallback por error de API: {e}")
        if not has_research:
            next_step = "Investigador"
        elif not has_analysis:
            next_step = "Analista"
        else:
            next_step = "FINISH"
            
        decision = RouterSchema(
            next_step=next_step,
            reasoning=f"Fallback determinístico aplicado por excepción: {e}"
        )

    # Retornamos tanto la decisión estructurada como la variable de ruteo
    return {
        "supervisor_decision": decision,
        "next_agent": decision.next_step
    }


def route_decision(state: TeamState) -> str:
    """Función de arista condicional que lee la decisión tipada del estado."""
    # Si por alguna razón el estado guarda el objeto Pydantic o el string directo:
    decision = state.get("supervisor_decision")
    if hasattr(decision, "next_step"):
        return decision.next_step
    return state.get("next_agent", "FINISH")


def build_graph() -> StateGraph:
    """Construye y compila el grafo jerárquico."""
    builder = StateGraph(TeamState)

    # 1. Agregar Nodos
    builder.add_node("Supervisor", supervisor_node)
    builder.add_node("Investigador", research_node)
    builder.add_node("Analista", analyst_node)

    # 2. Definir Punto de Entrada
    builder.set_entry_point("Supervisor")

    # 3. Aristas Condicionales desde el Supervisor usando el enrutador tipado
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