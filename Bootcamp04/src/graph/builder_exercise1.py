from langgraph.graph import END, START, StateGraph

from src.graph.nodes.decide import decide
from src.graph.nodes.format_output import format_output
from src.graph.nodes.receive import receive_simple
from src.graph.state import State


def build_graph():
    graph = StateGraph(State)
    graph.add_node("receive", receive_simple)
    graph.add_node("decide", decide)
    graph.add_node("format_output", format_output)
    graph.add_edge(START, "receive")
    graph.add_edge("receive", "decide")
    graph.add_edge("decide", "format_output")
    graph.add_edge("format_output", END)
    return graph.compile()
