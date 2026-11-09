Semana 1, exercício 1 (introdutório): qual navio chega primeiro?
Quando: meio da semana (segunda e terça). Tema: LangChain e LangGraph, parte 1. Dados: dados/frota_simples.json.

O desafio, em poucas palavras
No desafio final, cada grupo controla uma frota de 4 navios que saem do Porto Alfa rumo a portos diferentes. Os agentes do grupo precisam tomar decisões a cada instante: quem acelera, quem reduz, quem chega primeiro.

Neste exercício você vai construir a menor peça possível desse sistema: um agente que recebe a lista de navios e responde qual deles chega primeiro ao seu porto. Ainda sem regras especiais, sem ferramentas e sem condicionais. O objetivo é montar o esqueleto do projeto e rodar o seu primeiro grafo LangGraph.

O que você vai aprender
Criar a estrutura de pastas do projeto (src/app, src/graph, src/utils).
Criar o LLM por um adaptador (llm_adapter).
Escrever um prompt (primeiro de uma linha, depois melhorado).
Montar um grafo de 3 nós sem condicional: receber, decidir e formatar.
Perceber um limite importante: LLM não é calculadora.
A regra do problema
O tempo de viagem de um navio é:

ETA (horas) = distância (milhas náuticas) / velocidade (nós)
Quem tiver o menor ETA chega primeiro. Os dados:

Navio	Destino	Distância (nm)	Velocidade (nós)
S1-FAROL	Porto Norte	700	14
S2-MARE	Porto Leste	760	16
S3-CORAL	Porto Sul	680	12
S4-ATLAS	Porto Oeste	820	14
Repare que o navio com a menor distância (S3-CORAL) não é o que chega primeiro: a velocidade também conta.

Passo a passo
Passo 1: criar o projeto
Siga a seção "Estrutura de pastas do projeto" do README: crie as pastas, o ambiente virtual e o .env. Copie dados/frota_simples.json para a pasta dados/ do seu projeto.

Instale as dependências:

pip install langgraph langchain langchain-openai python-dotenv pydantic langfuse
Passo 2: o adaptador do LLM
Em src/utils/llm_adapter.py, crie a função get_llm(). Ela lê o provedor e o modelo das variáveis de ambiente e devolve um modelo de chat. Nenhum outro arquivo deve importar o provedor diretamente.

Passo 3: o cliente Langfuse (opcional por enquanto)
Em src/utils/langfuse_client.py, crie run_config(). Ela devolve a configuração de execução do LangGraph com o handler do Langfuse, se as chaves existirem; caso contrário, devolve uma configuração vazia. Assim o projeto funciona com ou sem Langfuse.

Passo 4: o estado
Em src/graph/state.py, defina o estado com quatro campos: pergunta, frota, resposta_llm e resultado.

Passo 5: os três nós
Cada nó é um arquivo em src/graph/nodes/. Um nó recebe o estado e devolve só os campos que alterou.

Nó	Tipo	O que faz
receive	código	lê dados/frota_simples.json e coloca em frota
decide	LLM	envia o prompt com a frota e guarda a resposta em resposta_llm
format_output	código	monta o texto final em resultado
Passo 6: o prompt de uma linha
Em src/graph/prompts/choose_ship.py, comece com um prompt de uma única linha:

Qual navio chega primeiro ao porto? Frota: {frota}
Passo 7: montar o grafo
Em src/graph/builder.py, ligue os nós em linha reta: START → receive → decide → format_output → END.

Passo 8: executar
Em src/app/main.py, peça uma pergunta ao usuário, rode o grafo e imprima o resultado.

python -m src.app.main
Passo 9: melhorar o prompt
Rode 5 vezes o prompt de uma linha e anote: o modelo acertou o navio? Acertou o ETA? Depois troque pelo prompt melhorado (com papel e a fórmula do ETA) e rode mais 5 vezes. Compare.

Resultado esperado
Para os dados acima, a resposta correta é:

Navio	ETA (horas)
S2-MARE	47,50
S1-FAROL	50,00
S3-CORAL	56,67
S4-ATLAS	58,57
Saída do programa (o texto pode variar):

Pergunta: Qual navio chega primeiro ao porto?
Resposta: O navio que chega primeiro é o S2-MARE, com ETA de 47,5 horas.
Como verificar
 A estrutura de pastas está igual à do README.
 get_llm() é o único lugar que cria o modelo.
 O grafo tem exatamente 3 nós e nenhuma aresta condicional.
 O prompt está em prompts/, não dentro do nó.
 O programa roda sem o Langfuse configurado.
 Você registrou os acertos dos 10 testes (5 com cada prompt).
Para pensar
O que mudou entre o prompt de uma linha e o melhorado? Quantos acertos a mais?
Em alguma execução o modelo errou a conta? Por que acha que isso acontece?
Se a frota tivesse 40 navios, esse desenho ainda seria confiável? O que você faria diferente?
A pergunta 2 é a ponte para o exercício 2: dar ao agente ferramentas para calcular e condicionais para decidir o caminho.

Desafio extra (opcional)
Use saída estruturada (with_structured_output) para o modelo devolver {"navio": "...", "eta_horas": 0.0} em vez de texto livre.
Crie uma interface simples em src/app (por exemplo, Streamlit) com um campo de pergunta e um botão.
Como resolver (gabarito do instrutor)
Ideia geral
Um grafo LangGraph é um conjunto de nós (funções) que leem e escrevem num estado compartilhado. As arestas definem a ordem. Aqui a ordem é fixa: receber, decidir, formatar. O LLM aparece em um único nó.


src/utils/llm_adapter.py
import os

from dotenv import load_dotenv
from langchain.chat_models import init_chat_model

load_dotenv()


def get_llm(temperature: float = 0):
    return init_chat_model(
        model=os.environ["LLM_MODEL"],
        model_provider=os.environ["LLM_PROVIDER"],
        temperature=temperature,
    )
temperature=0 deixa as respostas mais estáveis, o que ajuda a comparar os 10 testes. O adaptador isola o provedor: para trocar de OpenAI para Azure, muda-se só o .env (e as variáveis do provedor).

src/utils/langfuse_client.py
import os


def get_langfuse_handler():
    if not (os.getenv("LANGFUSE_PUBLIC_KEY") and os.getenv("LANGFUSE_SECRET_KEY")):
        return None
    from langfuse.langchain import CallbackHandler

    return CallbackHandler()


def run_config(**extra) -> dict:
    handler = get_langfuse_handler()
    config = {"callbacks": [handler]} if handler else {}
    config.update(extra)
    return config


def flush() -> None:
    if os.getenv("LANGFUSE_PUBLIC_KEY") and os.getenv("LANGFUSE_SECRET_KEY"):
        from langfuse import get_client

        get_client().flush()
O import do Langfuse fica dentro das funções para o projeto rodar sem a biblioteca configurada. O Langfuse envia os traces em segundo plano: em scripts curtos, chame flush() no fim para não perder eventos. Na versão 2 do Langfuse, o import do handler é from langfuse.callback import CallbackHandler.

src/graph/state.py
from typing import TypedDict


class State(TypedDict, total=False):
    pergunta: str
    frota: dict
    resposta_llm: str
    resultado: str
total=False permite que o estado comece só com pergunta e seja preenchido pelos nós.

Nós
src/graph/nodes/receive.py:

import json
from pathlib import Path

from src.graph.state import State

ARQUIVO = Path(__file__).resolve().parents[3] / "dados" / "frota_simples.json"


def receive(state: State) -> dict:
    frota = json.loads(ARQUIVO.read_text(encoding="utf-8"))
    return {"frota": frota}
src/graph/prompts/choose_ship.py (versão de uma linha, o ponto de partida):

from langchain_core.prompts import ChatPromptTemplate

PROMPT_UMA_LINHA = ChatPromptTemplate.from_messages(
    [("human", "Qual navio chega primeiro ao porto? Frota: {frota}")]
)
Versão melhorada, para o passo 9:

PROMPT_MELHORADO = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "Você é um despachante de porto. O ETA em horas de cada navio é "
            "distancia_nm dividido por velocidade_kn. Chega primeiro quem tem o menor ETA. "
            "Responda com o id do navio e o ETA em horas.",
        ),
        ("human", "Frota: {frota}\n\nQual navio chega primeiro ao porto?"),
    ]
)
src/graph/nodes/decide.py:

import json

from src.graph.prompts.choose_ship import PROMPT_MELHORADO
from src.graph.state import State
from src.utils.llm_adapter import get_llm


def decide(state: State) -> dict:
    chain = PROMPT_MELHORADO | get_llm()
    resposta = chain.invoke({"frota": json.dumps(state["frota"], ensure_ascii=False)})
    return {"resposta_llm": resposta.content}
prompt | llm é uma chain do LangChain: a saída do prompt entra no modelo. Para comparar os dois prompts, troque PROMPT_MELHORADO por PROMPT_UMA_LINHA.

src/graph/nodes/format_output.py:

from src.graph.state import State


def format_output(state: State) -> dict:
    return {"resultado": f"Pergunta: {state['pergunta']}\nResposta: {state['resposta_llm']}"}
src/graph/builder.py
from langgraph.graph import END, START, StateGraph

from src.graph.nodes.decide import decide
from src.graph.nodes.format_output import format_output
from src.graph.nodes.receive import receive
from src.graph.state import State


def build_graph():
    graph = StateGraph(State)
    graph.add_node("receive", receive)
    graph.add_node("decide", decide)
    graph.add_node("format_output", format_output)

    graph.add_edge(START, "receive")
    graph.add_edge("receive", "decide")
    graph.add_edge("decide", "format_output")
    graph.add_edge("format_output", END)
    return graph.compile()
src/app/main.py
from src.graph.builder import build_graph
from src.utils.langfuse_client import flush, run_config


def main() -> None:
    graph = build_graph()
    pergunta = input("Pergunta: ").strip() or "Qual navio chega primeiro ao porto?"
    saida = graph.invoke({"pergunta": pergunta}, config=run_config())
    print(saida["resultado"])
    flush()


if __name__ == "__main__":
    main()
Para mostrar o desenho do grafo em aula: print(graph.get_graph().draw_mermaid()).

O que comentar com a turma
Prompt de uma linha: costuma funcionar com poucos navios, mas é frágil. O modelo pode "calcular de cabeça" e errar, sobretudo com mais navios ou números menos redondos.
Prompt melhorado: dar papel e fórmula melhora, mas não garante a conta. LLM prevê texto, não executa aritmética.
Ponte para o exercício 2: o certo é deixar o cálculo para uma ferramenta (código) e usar o LLM para decidir qual ferramenta chamar e como explicar o resultado. Também é preciso um desvio para perguntas que não são sobre chegada de navios.
Estado: mostre que cada nó devolve só o que mudou; o LangGraph faz o merge no estado.
Estrutura de pastas: ressalte que src/app não importa o provedor do LLM e que builder.py só liga nós.