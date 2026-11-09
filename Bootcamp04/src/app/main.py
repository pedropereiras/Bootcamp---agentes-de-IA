from langgraph.types import Command  #cria comandos que podem ser enviados para o grafo de agentes.
from src.graph.builder import build_graph #construe o grafo de agentes.

def main() -> None: #função principal que executa o fluxo de interação com o grafo de agentes.
    graph = build_graph() #criar o grafo de agentes e armazena o resultado na variável graph.
    config = {"configurable": {"thread_id": "semana-1"}} #cria as configurações da conversa
    pergunta = input("Pergunta: ").strip() or "Qual navio chega primeiro ao porto?"
    saida = graph.invoke({"pergunta": pergunta}, config) #envia a pergunta do usuário para o grafo de agentes e armazena a resposta na variável saida. 
    if "__interrupt__" in saida: #aqui o assistente entra em ação. .invoke envia a pergunta para o grafo de agentes e recebe a resposta. Se a resposta contiver a chave "__interrupt__", significa que o agente precisa de aprovação do usuário antes de continuar.
        pedido = saida["__interrupt__"][0].value #armazena o pedido de aprovação do agente na variável pedido.
        print("Recomendação do agente:\n", pedido["recomendacao"]) #exibe a recomendação do agente para o usuário.
        aprovado = input("Aprovar? (s/n): ").strip().lower() == "s" 
        nota = input("Nota (opcional): ").strip()
        saida = graph.invoke(Command(resume={"aprovado": aprovado, "nota": nota}), config) #se o usuário aprovar ou não a recomendação do agente, o grafo de agentes é chamado novamente com a resposta do usuário. A função Command é usada para criar um comando que resume a interação com o agente, incluindo se a recomendação foi aprovada e qualquer nota adicional fornecida pelo usuário.
    print(saida["resultado"]) #exibe o resultado final da interação com o grafo de agentes.

if __name__ == "__main__": 
    main()


#build_graph cria o fluxo de trabalho e as regras da Ia. define o passo a passo exato que o grafo de agentes deve seguir para processar a pergunta do usuário e gerar uma resposta apropriada. Ele define os nós do grafo, as conexões entre eles e as regras que governam o fluxo de informações.
#graph.invoke executa o fluxo de IA, passando os dados de entrada e processa.
