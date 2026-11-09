from typing import Literal 
from pydantic import BaseModel #usada para criar modelos de dados com validação e serialização automática.
from src.graph.prompts.classify_prompt import CLASSIFY_PROMPT 
from src.graph.state import State #serve para importar a classe State q representa o estado da conversa com o grafo de agentes.
from src.utils.llm_adapter import get_llm #retorna a LLM configurada para o grafo de agentes.


class Intencao(BaseModel): #usada para representar a intenção da pergunta do usuário. 
    intent: Literal["primeiro_a_chegar", "regras", "fora_escopo"] #define os valores possíveis para a intenção da pergunta do usuário. A intenção pode ser "primeiro_a_chegar", "regras" ou "fora_escopo". O uso de Literal garante que apenas esses valores sejam aceitos, fornecendo validação automática e documentação clara para a intenção da pergunta.


def classify(state: State) -> dict: #classifica a intenção da pergunta do usuário com base no estado atual da conversa. Recebe um objeto state do tipo State e retorna um dicionário contendo a intenção classificada.
    chain = CLASSIFY_PROMPT | get_llm().with_structured_output(Intencao) 
    return {"intent": chain.invoke({"pergunta": state["pergunta"]}).intent}

#BaseModel cria modelo de dados estruturados

#.with_structured_output(Intencao): Força a IA a não responder 
# em texto livre, mas sim entregar o resultado estritamente 
# formatado conforme a classe Intencao. Isso impede que a IA 
# invente categorias inexistentes.

#O código lê o que o usuário perguntou, passa para a IA 
# classificar dentro de um "menu de opções" fixo (Intencao) 
# e salva essa categoria no sistema para decidir o próximo passo.