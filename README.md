# Orquestador Multi-Agente Jerárquico de Análisis e Investigación

Este proyecto implementa una arquitectura **Multi-Agente Jerárquica** con un nodo **Supervisor** central que coordina las tareas entre especialistas en **Investigación** y **Análisis Cómputo**, utilizando **LangGraph** y ejecución autónoma mediante patrones **ReAct**.

## Diagrama Mermaid del Grafo

```mermaid
graph TD
    START([Inicio]) --> Supervisor
    
    Supervisor -->|Decisión: Investigador| Investigador
    Supervisor -->|Decisión: Analista| Analista
    Supervisor -->|Decisión: FINISH| END([Fin])
    
    Investigador -->|Retorno con datos| Supervisor
    Analista -->|Retorno con análisis| Supervisor

![Diagrama del Grafo Jerárquico](./graph_diagram.png)


## Justificación de la Topología Elegida

Se seleccionó una **Topología Jerárquica (Hub-and-Spoke / Supervisor-Workers)** por los siguientes motivos de arquitectura de software y requerimientos técnicos del sistema:

1. **Desacoplamiento y Especialización Estricta con Herramientas Exclusivas:** 
   Cada agente especialista (`Investigador` y `Analista`) opera como una unidad con responsabilidad única (SRP) y cuenta con un ciclo autónomo ReAct (`create_react_agent`):
   * **Investigador:** Configurado exclusivamente con herramientas de búsqueda web (`DuckDuckGoSearchRun`) y recuperación de conocimiento interno para recolectar datos crudos y certeros desde el exterior.
   * **Analista:** Configurado exclusivamente con herramientas de cómputo y procesamiento (`calculator_tool`, `text_stats_tool`) para transformar, calcular o evaluar métricas sobre la información ya recolectada, sin realizar tareas de búsqueda web.

2. **Control Centralizado y Enrutamiento Estructurado Tipado:** 
   El **Supervisor** centraliza las decisiones de delegación eliminando comparaciones de texto plano frágiles o propensas a errores. Utiliza **salida estructurada forzada con Pydantic (`with_structured_output` y `Literal`)**, garantizando que las transiciones entre nodos sean estrictamente tipadas, deterministas y validadas en tiempo de ejecución.

3. **Escalabilidad y Extensibilidad del Sistema:** 
   Esta topología permite escalar el proyecto de manera modular y limpia. Agregar un nuevo especialista (por ejemplo, un agente de validación o redacción) solo requiere definir sus herramientas particulares, sumarlo como nodo al grafo y extender las opciones permitidas en el esquema `Literal` del supervisor, sin alterar la lógica de los agentes existentes.