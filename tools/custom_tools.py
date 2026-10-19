import math
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_core.tools import tool

# ==========================================
# 1. HERRAMIENTAS DEL INVESTIGADOR
# ==========================================
search_tool = DuckDuckGoSearchRun()

@tool
def internal_knowledge_retriever(query: str) -> str:
    """Consulta la base de conocimientos interna sobre arquitectura de agentes y LangGraph."""
    return f"Resultado interno para '{query}': LangGraph soporta patrones jerárquicos (Supervisor-Workers) y ReAct loops."

investigador_tools = [search_tool, internal_knowledge_retriever]


# ==========================================
# 2. HERRAMIENTAS DEL ANALISTA
# ==========================================
@tool
def calculator_tool(expression: str) -> str:
    """Evalúa expresiones matemáticas o estadísticas simples (ej. '100 * 1.425')."""
    try:
        allowed_names = {"math": math, "abs": abs, "round": round}
        code = compile(expression, "<string>", "eval")
        for name in code.co_names:
            if name not in allowed_names:
                raise NameError(f"Uso no permitido de '{name}'")
        result = eval(code, {"__builtins__": {}}, allowed_names)
        return f"Resultado del cálculo: {result}"
    except Exception as e:
        return f"Error en la evaluación: {str(e)}"

@tool
def text_stats_tool(text: str) -> str:
    """Analiza métricas de texto: conteo de palabras, caracteres y densidad."""
    words = text.split()
    return f"Estadísticas -> Palabras: {len(words)}, Caracteres: {len(text)}"

analista_tools = [calculator_tool, text_stats_tool]