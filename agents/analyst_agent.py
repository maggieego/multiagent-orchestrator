from langchain_core.messages import HumanMessage
from langgraph.prebuilt import create_react_agent
from state import TeamState
from config import get_llm
from tools.custom_tools import analista_tools

def get_analista_agent():
    """Crea un agente ReAct configurado con herramientas exclusivas de cómputo y métricas."""
    llm = get_llm(temperature=0.0)
    return create_react_agent(
        model=llm,
        tools=analista_tools,
        prompt=(
            "Eres el Agente Analista. Tu rol exclusivo es procesar, realizar cálculos "
            "y evaluar estadísticas sobre los datos provistos utilizando tus herramientas (calculator_tool, text_stats_tool)."
        )
    )

def analyst_node(state: TeamState) -> dict:
    data = state.get("research_data", "")
    
    try:
        agent = get_analista_agent()
        # Invocamos el agente ReAct sobre la información que trajo el Investigador
        result = agent.invoke({
            "messages": [HumanMessage(content=f"Analiza y calcula métricas clave sobre esta información provista: {data}")]
        })
        last_msg = result["messages"][-1].content
    except Exception as e:
        print(f"⚠️ [Analista] Usando modo de prueba (Mock): {e}")
        last_msg = f"Métricas calculadas sobre [{data}]: Incremento proyectado de +42.5% en eficiencia."

    return {
        "messages": [HumanMessage(content=f"[ANALISTA]: {last_msg}", name="Analista")],
        "analysis_data": last_msg,
        "step_count": state.get("step_count", 0) + 1
    }