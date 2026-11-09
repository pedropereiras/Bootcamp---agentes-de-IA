import json

from src.graph.prompts.decide_prompt import PROMPT_MELHORADO, PROMPT_UMA_LINHA
from src.graph.state import State
from src.utils.llm_adapter import get_llm

PROMPT = PROMPT_MELHORADO
def decide(state: State) -> dict:
    resposta = (PROMPT | get_llm()).invoke(
        {"frota": json.dumps(state["frota"], ensure_ascii=False)}
    )
    return {"resposta_llm": str(resposta.content)}
