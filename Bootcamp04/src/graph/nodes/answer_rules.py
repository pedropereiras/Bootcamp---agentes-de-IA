from src.graph.prompts.rules_prompt import RULES_PROMPT #armazena o prompt de regras que será usado para gerar respostas do modelo de linguagem.
from src.graph.state import State #representa o estado da conversa com o grafo de agentes.
from src.utils.llm_adapter import get_llm #obtem o modelo de linguagem (LLM) configurado para o grafo de agentes.


def answer_rules(state: State) -> dict: #gerar uma resposta apropriada usando o prompt de regras e o modelo de linguagem configurado.
    resposta = (RULES_PROMPT | get_llm()).invoke({"pergunta": state["pergunta"]}) #combina regras de instrução com o modelo de IA, envia a pergunta do usuário e devolve a resposta gerada.
    return {"resultado": str(resposta.content)} #retorna um dicionário com a resposta gerada pelo modelo de linguagem, convertida para string. A chave "resultado" é usada para armazenar a resposta final que será exibida ao usuário.

#pega a pergunta do usuário, aplica as regras de negócio, envia para a 
# IA gerar o texto final e guarda esse texto puro no campo resultado do sistema.