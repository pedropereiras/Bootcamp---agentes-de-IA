from langgraph.types import interrupt

from src.graph.state import State
from src.graph.tools import calcular_eta_horas, reserva_ok, velocidade_efetiva


def _recommendation_from_fleet(state: State) -> str:
    navios = state.get("frota", {}).get("navios", [])
    if not navios:
        return "Nenhum navio foi informado para análise."

    elegiveis = []
    bloqueados = []
    for navio in navios:
        if not reserva_ok.invoke(
            {
                "combustivel_t": navio["combustivel_t"],
                "reserva_t": navio["reserva_t"],
            }
        ):
            bloqueados.append(
                f"{navio['id']} (combustível {navio['combustivel_t']} t abaixo "
                f"da reserva de {navio['reserva_t']} t)"
            )
            continue

        velocidade = velocidade_efetiva.invoke(
            {
                "velocidade_kn": navio["velocidade_kn"],
                "em_tempestade": navio["em_tempestade"],
            }
        )
        eta = calcular_eta_horas.invoke(
            {"distancia_nm": navio["distancia_nm"], "velocidade_kn": velocidade}
        )
        elegiveis.append((navio["id"], eta))

    if elegiveis:
        menor_eta = min(eta for _, eta in elegiveis)
        vencedores = [nome for nome, eta in elegiveis if eta == menor_eta]
        vencedor_texto = ", ".join(vencedores)
        linhas = [
            f"{vencedor_texto} chega primeiro ({menor_eta:.2f} h).",
            "ETAs dos navios elegíveis: "
            + "; ".join(f"{nome}: {eta:.2f} h" for nome, eta in elegiveis)
            + ".",
        ]
    else:
        linhas = ["Nenhum navio elegível para a viagem."]

    if bloqueados:
        linhas.append("Navios bloqueados: " + "; ".join(bloqueados) + ".")
    else:
        linhas.append("Nenhum navio bloqueado.")

    return " ".join(linhas)


def human_review(state: State) -> dict:
    recomendacao = str(state["messages"][-1].content).strip()
    if not recomendacao:
        recomendacao = (
            "O modelo não retornou uma resposta textual; recomendação calculada "
            "com os dados da frota e as ferramentas locais. "
            + _recommendation_from_fleet(state)
        )
    decisao = interrupt({"recomendacao": recomendacao, "pergunta": "Aprovar a recomendação?"})
    return {
        "recomendacao": recomendacao,
        "aprovado": bool(decisao["aprovado"]),
        "nota_operador": decisao.get("nota", ""),
    }
