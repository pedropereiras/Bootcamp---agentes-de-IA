from src.graph.state import State #representa o estado da conversa com o grafo de agentes.
from src.graph.tools import TOOLS #armazenar as ferramentas disponíveis para o grafo de agentes.
from src.utils.llm_adapter import get_llm #obtem o modelo de linguagem (LLM) configurado para o grafo de agentes.


MAX_TENTATIVAS = 3


def analyze(state: State) -> dict: #função que recebe um objeto state e retorna um dicionário.responsável por analisar o estado atual da conversa com o grafo de agentes e gerar uma resposta apropriada usando o modelo de linguagem configurado.
    llm = get_llm().bind_tools(TOOLS)
    for tentativa in range(1, MAX_TENTATIVAS + 1):
        try:
            return {"messages": [llm.invoke(state["messages"])]} #retorna um dicionário com a lista de mensagens geradas pelo modelo de linguagem.
        except Exception as erro:
            # A Groq devolve 400 "tool_use_failed" quando o modelo gera uma chamada de
            # ferramenta malformada. Isso é intermitente, então tentamos de novo.
            if "tool_use_failed" not in str(erro) or tentativa == MAX_TENTATIVAS:
                raise

#def analyze(state: State) -> dict: - analisa os dados recebidos 
#get_llm chama a função que devolve o modelo de linguagem configurado para o grafo de agentes.
#.bind_tools(TOOLS) - vincula as ferramentas disponíveis para o grafo de agentes ao modelo de linguagem.
#.invoke(state["messages"]) - invoca o modelo de linguagem com as mensagens do estado atual da conversa, gerando uma resposta apropriada.

#Pega as mensagens da conversa, envia para a IA e devolve a resposta dela para atualizar o histórico.