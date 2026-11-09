from langchain_core.prompts import ChatPromptTemplate

CLASSIFY_PROMPT = ChatPromptTemplate.from_messages(
    [
        ("system", "Classifique a pergunta em: primeiro_a_chegar (qual navio chega primeiro ao porto), regras (regras de navegação, velocidade, tempestade ou combustível) ou fora_escopo (qualquer outro assunto)."),
        ("human", "{pergunta}"),
    ]
)
