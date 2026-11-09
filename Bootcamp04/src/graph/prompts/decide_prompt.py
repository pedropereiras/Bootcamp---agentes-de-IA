from langchain_core.prompts import ChatPromptTemplate

PROMPT_UMA_LINHA = ChatPromptTemplate.from_messages(
    [("human", "Qual navio chega primeiro? Frota: {frota}")]
)

PROMPT_MELHORADO = ChatPromptTemplate.from_messages(
    [
        ("system", "Você é um assistente de operações portuárias. Calcule o ETA de cada navio como distância em milhas náuticas dividida pela velocidade em nós. Compare todos e informe o identificador do navio com menor ETA e o ETA em horas, com duas casas decimais. Não invente dados."),
        ("human", "Frota disponível:\n{frota}"),
    ]
)
