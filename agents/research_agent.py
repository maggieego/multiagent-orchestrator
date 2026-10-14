from langchain_core.messages import HumanMessage
from state import TeamState
from config import get_llm

def research_node(state: TeamState) -> dict:
    user_query = state["messages"][0].content
    
    try:
        # Intenta usar el LLM si hay una API Key válida
        llm = get_llm(temperature=0.2)
        prompt = f"Investiga brevemente el mercado para la siguiente consulta: {user_query}"
        response = llm.invoke([HumanMessage(content=prompt)])
        result_text = response.content
    except Exception as e:
        # Fallback a respuesta Mock si no hay credenciales o falla la API
        print(f"⚠️ [Investigador] Usando modo de prueba (Mock): {e}")
        result_text = f"Análisis de mercado sobre '{user_query}': Alta adopción en arquitecturas ReAct para 2026."

    return {
        "messages": [HumanMessage(content=f"[INVESTIGADOR]: {result_text}", name="Investigador")],
        "research_data": result_text,
        "step_count": state.get("step_count", 0) + 1
    }