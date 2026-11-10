from pydantic import BaseModel
from langchain_core.prompts import ChatPromptTemplate

class Revisao(BaseModel):
    aprovado: bool
    motivo: str

REVISOR_PROMPT = ChatPromptTemplate.from_messages([
    (
        "system",
        "Você é o agente de segurança e revisa propostas de navegação. Regras:\n"
        "- Tempestade na rota direta: velocidade máxima de 12 nós.\n"
        "- Tempestade na rota protegida: velocidade máxima de 15 nós.\n"
        "- Sem tempestade: a ação correta é NO_ACTION.\n"
        "Aprove só se a proposta respeitar as regras. Se rejeitar, diga o limite correto "
        "no motivo."
    ),
    ("human", "Navio: {navio}\nProposta a revisar: {proposta}"),
])