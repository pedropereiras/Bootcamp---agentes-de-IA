from typing import TypedDict


class State(TypedDict, total=False):
    ship_id: str
    navio: dict
    proposta: dict #agente vai salvar sua resposta
    revisao: dict #agente vai salvar sua resposta
    rodada: int
    resultado: str

#nó lê o estado, processa algo e injeta um novo dado 
#nesse estado. O nó seguinte recebe o estado atualizado.