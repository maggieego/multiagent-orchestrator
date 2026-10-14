from typing import Dict, Any
from langchain_core.tools import tool

# Base de datos simulada de métricas de mercado/tecnología
MOCK_METRICS_DB: Dict[str, Dict[str, Any]] = {
    "langgraph": {
        "adopcion_empresarion": "84%",
        "consultas_mensuales": 1200000,
        "satisfaccion_devs": "92%",
        "errores_frecuentes": ["Supervisor infinito", "Límites de recursión no manejados"]
    },
    "sistemas_multiagente": {
        "crecimiento_anual": "145%",
        "casos_uso_principales": ["Atención al cliente", "Análisis financiero", "Investigación autónoma"],
        "eficiencia_vs_monolitico": "+38%"
    }
}

@tool
def buscar_informacion_mercado(tema: str) -> str:
    """
    Busca métricas, datos estadísticos e información relevante sobre un tema de tecnología o mercado.
    
    Args:
        tema (str): El tema o tecnología a consultar (ej. 'langgraph', 'sistemas_multiagente').
    """
    key = tema.lower().replace(" ", "_")
    if key in MOCK_METRICS_DB:
        return f"Resultados para '{tema}': {MOCK_METRICS_DB[key]}"
    return f"Se encontraron datos generales sobre {tema}: 'Alta demanda en proyectos de IA en 2026, con foco en arquitectura ReAct y orquestación jerárquica'."

@tool
def calcular_metricas_rendimiento(datos_numericos: str) -> str:
    """
    Procesa un texto o lista de datos numéricos para calcular promedios, porcentajes de incremento y resúmenes cuantitativos.
    
    Args:
        datos_numericos (str): Texto que contiene datos o valores cuantitativos a analizar.
    """
    return f"Análisis Cómputo/Estadístico completado sobre [{datos_numericos}]: Promedio de crecimiento proyectado: +42.5%, Nivel de confianza: 95%."