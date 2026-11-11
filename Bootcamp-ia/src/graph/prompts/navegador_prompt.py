
from typing import Literal #previne alucinação
from pydantic import BaseModel, model_validator
from langchain_core.prompts import ChatPromptTemplate

class Proposta(BaseModel):
    acao: Literal["SET_SPEED", "NO_ACTION"]
    velocidade_kn: float | None = None
    motivo: str
#mudou aqui
    @model_validator(mode="after")
    def validar_velocidade(self):
        # NO_ACTION não pode ter velocidade atrelada
        if self.acao == "NO_ACTION":
            if self.velocidade_kn is not None:
                raise ValueError("NO_ACTION não deve informar velocidade")
            return self

        # SET_SPEED obrigatoriamente precisa de uma velocidade
        if self.velocidade_kn is None:
            raise ValueError("SET_SPEED exige uma velocidade")

        velocidade = self.velocidade_kn
        
        # Limites físicos do navio
        if not 0 <= velocidade <= 18:
            raise ValueError("A velocidade deve estar entre 0 e 18 nós")
            
        # Regra 4: Aceleração/Desaceleração apenas em passos de 0.5
        if abs(velocidade * 2 - round(velocidade * 2)) > 1e-8:
            raise ValueError("A velocidade deve avançar em passos de 0,5 nó")

        return self

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

# define o prompt do navegador e a estrutura de saída esperada (Proposta) para o LLM.