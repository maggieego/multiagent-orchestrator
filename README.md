# Orquestador Multi-Agente Jerárquico de Análisis e Investigación

Este proyecto implementa una arquitectura **Multi-Agente Jerárquica** con un nodo **Supervisor** central que coordina las tareas entre especialistas en **Investigación** y **Análisis Cómputo**.

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

Se seleccionó una **Topología Jerárquica (Hub-and-Spoke / Supervisor-Workers)** por los siguientes motivos de arquitectura de software:

1. **Desacoplamiento y Especialización Estricta:** 
   Cada agente especialista (`Investigador` y `Analista`) opera como una unidad con responsabilidad única (SRP). El investigador se enfoca exclusivamente en consumir herramientas externas y recolectar datos, mientras que el analista procesa esa información sin preocuparse por la fase de recolección.
2. **Control Centralizado y Validación:** 
   Al hacer que todas las aristas de retorno pasen obligatoriamente por el **Supervisor**, nos aseguramos de que haya un nodo de validación en cada iteración. El supervisor evalúa el grado de suficiencia de la respuesta antes de dar paso al siguiente especialista o dar por finalizada la tarea (`FINISH`).
3. **Escalabilidad:** 
   Esta topología permite agregar nuevos agentes especialistas (por ejemplo, un *Agente Redactor* o un *Agente de Validación de Código*) simplemente agregando el nodo al grafo y añadiendo la opción de ruteo en la arista condicional del Supervisor, sin romper la lógica existente.

---

## 🔀 Manejo de Conflictos y Prevención de Bucles

Para prevenir errores comunes en sistemas multi-agente, se implementaron dos estrategias clave:

### 1. Prevención del "Supervisor Infinito" (Bucles Eternos)
* **Contador de Pasos (`step_count`):** El estado compartido `TeamState` mantiene un contador de iteraciones. Si el grafo alcanza un límite prudencial de ejecuciones (`step_count >= 5`), la arista condicional fuerza la salida directa hacia `FINISH` independientemente de la respuesta del modelo, evitando costos excesivos en la API o bloqueos infinitos.
* **Criterio de Suficiencia Estricto:** El prompt del Supervisor valida explícitamente los campos del estado (`research_data` y `analysis_data`). Si ambos campos están presentes, el ruteador devuelve `FINISH` de forma inmediata.

### 2. Aislamiento de Estado y Contaminación de Contexto
* En lugar de pasar todo el historial de metadatos a todos los nodos, utilizamos campos dedicados en `TeamState` para almacenar únicamente los artefactos de salida de cada especialista (`research_data` y `analysis_data`).
* Cada agente especialista recibe solo la instrucción específica que necesita para operar, reduciendo la latencia y la confusión del modelo (*context clutter*).