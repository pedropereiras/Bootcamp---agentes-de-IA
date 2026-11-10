import json
from src.graph.prompts.navegador_prompt import NAVEGADOR_PROMPT, Proposta
from src.graph.state import State
from src.utils.llm_adapter import get_llm # Use a importação correspondente ao seu setup de LLM

def navegador(state: State) -> dict:
    revisao = state.get("revisao") or {}
    
    # Se é a primeira rodada ou se foi aprovado, o feedback fica em branco.
    # Caso contrário, injetamos o motivo da rejeição anterior.
    feedback = "" if revisao.get("aprovado", True) else revisao.get("motivo", "")
    
    chain = NAVEGADOR_PROMPT | get_llm().with_structured_output(Proposta)
    
    proposta = chain.invoke({
        "navio": json.dumps(state["navio"], ensure_ascii=False), 
        "feedback": feedback
    })
    
    # Atualiza o estado com a proposta e, crucialmente, avança o relógio do sistema
    return {
        "proposta": proposta.model_dump(), 
        "rodada": state.get("rodada", 0) + 1
    }