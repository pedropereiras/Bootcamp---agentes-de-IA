from langgraph.graph import END, START, StateGraph

from src.graph.nodes.escalar import escalar
from src.graph.nodes.finalizar import finalizar
from src.graph.nodes.navegador import navegador
from src.graph.nodes.receive import receive
from src.graph.nodes.revisor import revisor
from src.graph.routing import route_after_review
from src.graph.state import State

def build_graph():
    graph = StateGraph(State)
    
    # 1. Registrando os "atores" (Nós)
    graph.add_node("receive", receive)
    graph.add_node("navegador", navegador)
    graph.add_node("revisor", revisor)
    graph.add_node("finalizar", finalizar)
    graph.add_node("escalar", escalar)

    # 2. Desenhando os caminhos estáticos
    graph.add_edge(START, "receive")
    graph.add_edge("receive", "navegador")
    graph.add_edge("navegador", "revisor")
    
    # 3. Desenhando a encruzilhada condicional
    graph.add_conditional_edges(
        "revisor",
        route_after_review,
        {
            "aprovado": "finalizar", 
            "tentar_de_novo": "navegador", 
            "esgotado": "escalar"
        },
    )
    
    # 4. Finalizando os fluxos
    graph.add_edge("finalizar", END)
    graph.add_edge("escalar", END)
    
    return graph.compile()