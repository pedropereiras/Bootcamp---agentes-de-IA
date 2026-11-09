from langchain_core.prompts import ChatPromptTemplate

REGRAS = (
    "- Velocidade-alvo: de 0 a 18 nós, em passos de 0,5.\n"
    "- Em tempestade, o limite de velocidade é de 12 nós.\n"
    "- Navio com combustível abaixo da reserva mínima não pode zarpar.\n"
    "- ETA em horas = distância em nm dividida pela velocidade efetiva em nós."
)

RULES_PROMPT = ChatPromptTemplate.from_messages(
    [("system", "Responda de forma curta usando apenas estas regras:\n" + REGRAS), ("human", "{pergunta}")]
)
