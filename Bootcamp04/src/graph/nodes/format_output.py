from src.graph.state import State


def format_output(state: State) -> dict:
    if state.get("resposta_llm"):
        return {"resultado": state["resposta_llm"]}
    nota = state.get("nota_operador", "")
    texto = f"APROVADO pelo operador.\n{state['recomendacao']}" if state.get("aprovado") else "REJEITADO pelo operador."
    if nota:
        texto += f"\nNota do operador: {nota}"
    return {"resultado": texto}
