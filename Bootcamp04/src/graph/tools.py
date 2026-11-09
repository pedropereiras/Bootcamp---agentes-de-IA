from langchain_core.tools import tool

LIMITE_TEMPESTADE_KN = 12.0


@tool
def calcular_eta_horas(distancia_nm: float, velocidade_kn: float) -> float:
    """Calcula o ETA em horas dividindo a distância pela velocidade efetiva."""
    return round(distancia_nm / velocidade_kn, 2)


@tool
def velocidade_efetiva(velocidade_kn: float, em_tempestade: bool) -> float:
    """Aplica o limite de 12 nós quando o navio está em tempestade."""
    return min(velocidade_kn, LIMITE_TEMPESTADE_KN) if em_tempestade else velocidade_kn


@tool
def reserva_ok(combustivel_t: float, reserva_t: float) -> bool:
    """Retorna True se o combustível a bordo cobre a reserva mínima."""
    return combustivel_t >= reserva_t


TOOLS = [calcular_eta_horas, velocidade_efetiva, reserva_ok]
