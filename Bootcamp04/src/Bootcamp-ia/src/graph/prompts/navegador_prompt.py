from typing import Literal #previne alucinação
from pydantic import BaseModel
from langchain_core.prompts import ChatPromptTemplate

class Proposta(BaseModel):
    acao: Literal["SET_SPEED", "NO_ACTION"]
    velocidade_kn: float | None = None
    motivo: str

NAVEGADOR_PROMPT = ChatPromptTemplate.from_messages([
    (
        "system",
        "Você é o agente de navegação. Em tempestade, proponha SET_SPEED reduzindo "
        "1 nó da velocidade atual. Sem tempestade, proponha NO_ACTION. "
        "Velocidades válidas: de 0 a 18 nós, em passos de 0,5. "
        "Se houver feedback do revisor, corrija a proposta de acordo com ele."
    ),
    ("human", "Navio: {navio}\nFeedback do revisor (pode estar vazio): {feedback}"),
])