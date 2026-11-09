import json
from pathlib import Path

from src.graph.state import State

ROOT = Path(__file__).resolve().parents[3]


def receive(state: State) -> dict:
    return {"frota": json.loads((ROOT / "dados" / "frota_tempestade.json").read_text(encoding="utf-8"))}


def receive_simple(state: State) -> dict:
    return {"frota": json.loads((ROOT / "dados" / "frota_simples.json").read_text(encoding="utf-8"))}
