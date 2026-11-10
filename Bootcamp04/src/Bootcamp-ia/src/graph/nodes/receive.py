import json
from pathlib import Path
from src.graph.state import State

# Ajuste o caminho conforme a estrutura da sua pasta raiz
ARQUIVO = Path(__file__).resolve().parents[3] / "dados" / "situacao_tempestade.json"

def receive(state: State) -> dict:
    # Carrega o navio pelo ship_id recebido no estado inicial
    navios = json.loads(ARQUIVO.read_text(encoding="utf-8"))["navios"]
    navio = next(n for n in navios if n["id"] == state["ship_id"])
    
    # Retornamos apenas os fragmentos que atualizam o estado
    return {"navio": navio, "rodada": 0, "revisao": {}}