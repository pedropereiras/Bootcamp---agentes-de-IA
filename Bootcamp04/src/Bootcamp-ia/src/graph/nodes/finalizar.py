#se o revisor aprovar, essa é a nova etapa
from src.graph.state import State

def finalizar(state: State) -> dict:
    p, navio = state["proposta"], state["navio"]
    
    if p["acao"] == "NO_ACTION":
        return {"resultado": f"{navio['id']}: nenhuma ação necessária"}
        
    return {
        "resultado": f"{navio['id']}: SET_SPEED {p['velocidade_kn']} nós "
                     f"(aprovado na rodada {state['rodada']})"
    }