#Se esgotarmos as tentativas sem acordo, o sistema aborta a operação de forma segura.
from src.graph.state import State

def escalar(state: State) -> dict:
    return {
        "resultado": f"{state['navio']['id']}: sem acordo após {state['rodada']} rodadas. "
                     "Escalar para o operador (nenhum comando enviado)."
    }

#Quando o laço de tentativas chega ao limite, este nó é acionado para gerar um aviso de que uma intervenção humana é necessária.