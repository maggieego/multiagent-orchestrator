import asyncio
from langchain_core.messages import HumanMessage
from graph import build_graph

async def run_demo():
    app = build_graph()

    try:
        with open("graph_diagram.png", "wb") as f:
            f.write(app.get_graph().draw_mermaid_png())
        print("Diagrama 'graph_diagram.png' actualizado con éxito.")
    except Exception as e:
        pass  # Si falla el renderizado del diagrama, continúa normalmente
    
    query = "Necesito investigar la adopción de LangGraph en el mercado y calcular las métricas de rendimiento proyectadas."
    
    print("\n" + "="*80)
    print("🚀 INICIANDO ORQUESTADOR MULTI-AGENTE JERÁRQUICO")
    print(f"👤 Solicitud: {query}")
    print("="*80 + "\n")

    # Estado inicial alineado con TeamState (usando supervisor_decision y artefactos de dominio)
    initial_state = {
        "messages": [HumanMessage(content=query)],
        "supervisor_decision": None,
        "research_data": None,
        "analysis_data": None,
        "step_count": 0
    }

    # Ejecución asíncrona por pasos (astream)
    async for output in app.astream(initial_state):
        for node_name, state_update in output.items():
            print(f"📍 [NODO EJECUTADO]: {node_name}")
            
            # Mostramos la decisión estructurada del supervisor si está presente en el update
            if "supervisor_decision" in state_update and state_update["supervisor_decision"]:
                decision = state_update["supervisor_decision"]
                print(f"   🧠 Decisión del Supervisor (RouterSchema): Ruteo -> {decision.next_step}")
                print(f"      Razonamiento: {decision.reasoning}")
                
            if "research_data" in state_update and state_update["research_data"]:
                print(f"   🔎 Artefacto de Investigación: {state_update['research_data'][:120]}...")
                
            if "analysis_data" in state_update and state_update["analysis_data"]:
                print(f"   📊 Artefacto de Análisis: {state_update['analysis_data'][:120]}...")
                
            if "step_count" in state_update:
                print(f"   🔢 Contador de pasos: {state_update['step_count']}\n")

    print("="*80)
    print("✅ FLUJO FINALIZADO CORRECTAMENTE CON SALIDA ESTRUCTURADA")
    print("="*80)

if __name__ == "__main__":
    asyncio.run(run_demo())