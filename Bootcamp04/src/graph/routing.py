from src.graph.state import State


def route_by_intent(state: State) -> str:
    return state["intent"]
