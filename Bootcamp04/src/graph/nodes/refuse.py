from src.graph.state import State


def refuse(state: State) -> dict:
    return {"resultado": "Pergunta fora do escopo (navios, portos e regras de operação)."}
    
