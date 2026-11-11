#lê o veredito do Revisor e decide para qual nó o estado deve ir.
from src.graph.state import State

MAX_RODADAS = 2

def route_after_review(state: State) -> str:
    # 1. Se o revisor aprovou, o fluxo segue para o sucesso.
    if state["revisao"]["aprovado"]:
        return "aprovado"
        
    # 2. Se rejeitou, mas ainda temos rodadas sobrando, voltamos ao navegador.
    if state["rodada"] < MAX_RODADAS:
        return "tentar_de_novo"
        
    # 3. Se rejeitou e as tentativas acabaram, abortamos.
    return "esgotado"