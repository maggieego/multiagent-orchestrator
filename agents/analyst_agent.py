from langchain_core.messages import HumanMessage
from state import TeamState
from config import get_llm

def analyst_node(state: TeamState) -> dict:
    data = state.get("research_data", "")
    
    try:
        # Intenta usar el LLM si hay una API Key válida
        llm = get_llm(temperature=0.0)
        prompt = f"Analiza cuantitativamente los siguientes datos y calcula métricas clave: {data}"
        response = llm.invoke([HumanMessage(content=prompt)])
        result_text = response.content
    except Exception as e:
        # Fallback a respuesta Mock si no hay credenciales o falla la API
        print(f"⚠️ [Analista] Usando modo de prueba (Mock): {e}")
        result_text = f"Métricas calculadas sobre [{data}]: Incremento proyectado de +42.5% en eficiencia."

    return {
        "messages": [HumanMessage(content=f"[ANALISTA]: {result_text}", name="Analista")],
        "analysis_data": result_text,
        "step_count": state.get("step_count", 0) + 1
    }