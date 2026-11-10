import json
from src.graph.prompts.revisor_prompt import REVISOR_PROMPT, Revisao
from src.graph.state import State
from src.utils.llm_adapter import get_llm

def revisor(state: State) -> dict:
    p = state["proposta"]
    
    # REGRA DE OURO: O revisor não recebe o 'motivo' do navegador.
    # Ocultamos a justificativa para que ele julgue apenas a ação matemática.
    proposta_sem_motivo = {"acao": p["acao"], "velocidade_kn": p["velocidade_kn"]}
    
    chain = REVISOR_PROMPT | get_llm().with_structured_output(Revisao)
    
    revisao = chain.invoke({
        "navio": json.dumps(state["navio"], ensure_ascii=False),
        "proposta": json.dumps(proposta_sem_motivo),
    })
    
    return {"revisao": revisao.model_dump()}

#separa os agentes para controlar o fluxo de inf.