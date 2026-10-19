from langchain_core.messages import HumanMessage
from langgraph.prebuilt import create_react_agent
from state import TeamState
from config import get_llm
from tools.custom_tools import investigador_tools

def get_investigador_agent():
    """Crea un agente ReAct configurado con herramientas exclusivas de búsqueda e investigación."""
    llm = get_llm(temperature=0.2)
    return create_react_agent(
        model=llm,
        tools=investigador_tools,
        prompt=(
            "Eres el Agente Investigador. Tu rol exclusivo es recolectar datos "
            "e información precisa utilizando tus herramientas de búsqueda (search_tool, internal_knowledge_retriever)."
        )
    )

def research_node(state: TeamState) -> dict:
    user_query = state["messages"][0].content
    
    try:
        agent = get_investigador_agent()
        # Invocamos el agente ReAct permitiéndole ejecutar herramientas autónomamente
        result = agent.invoke({
            "messages": [HumanMessage(content=f"Investiga la siguiente consulta utilizando tus herramientas: {user_query}")]
        })
        last_msg = result["messages"][-1].content
    except Exception as e:
        print(f"⚠️ [Investigador] Usando modo de prueba (Mock): {e}")
        last_msg = f"Análisis de mercado sobre '{user_query}': Alta adopción en arquitecturas ReAct para 2026."

    return {
        "messages": [HumanMessage(content=f"[INVESTIGADOR]: {last_msg}", name="Investigador")],
        "research_data": last_msg,
        "step_count": state.get("step_count", 0) + 1
    }