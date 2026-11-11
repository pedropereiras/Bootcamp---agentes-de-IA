import json
from src.graph.prompts.revisor_prompt import REVISOR_PROMPT, Revisao
from src.graph.state import State
from src.utils.llm_adapter import get_llm

def revisor(state: State) -> dict: 
    navio = state["navio"]
    p = state["proposta"]
    
    # O revisor não recebe o 'motivo' do navegador.
    proposta_sem_motivo = {"acao": p["acao"], "velocidade_kn": p["velocidade_kn"]}
    
    chain = REVISOR_PROMPT | get_llm().with_structured_output(Revisao)
    
    revisao = chain.invoke({
        "navio": json.dumps(navio, ensure_ascii=False), 
        "proposta": json.dumps(proposta_sem_motivo),
    })
    
    clima = navio.get("clima", "").lower() #tempestade
    rota = navio.get("rota", "").lower() #direta, protegida
    acao = p["acao"] #set_speed, no_action
    velocidade = p.get("velocidade_kn") #nos
    
    erro_deterministico = None #resposta do revisor, caso haja violação de regra
    
    if clima == "tempestade":
        if acao != "SET_SPEED":
            erro_deterministico = "Regra violada: Em tempestade, a ação obrigatória é SET_SPEED."
        elif rota == "direta" and (velocidade is None or velocidade > 12):
            erro_deterministico = "Regra violada: Em tempestade na rota direta, a velocidade máxima é 12 nós."
        elif rota == "protegida" and (velocidade is None or velocidade > 15):
            erro_deterministico = "Regra violada: Em tempestade na rota protegida, a velocidade máxima é 15 nós."
        elif rota not in ["direta", "protegida"]:
            erro_deterministico = f"Regra violada: Rota '{rota}' é desconhecida. Proposta rejeitada de forma preventiva."
    else:
        if acao != "NO_ACTION":
            erro_deterministico = "Regra violada: Sem tempestade, a ação obrigatória é NO_ACTION."
            
    # Se a verificação rígida via código falhar, sobrepõe a decisão (potencialmente falha) do LLM
    if erro_deterministico:
        revisao.aprovado = False
        revisao.motivo = erro_deterministico
        
    return {"revisao": revisao.model_dump()}

# separa os agentes para controlar o fluxo de inf.

