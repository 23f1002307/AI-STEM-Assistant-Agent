from langgraph.graph import StateGraph
from typing import TypedDict

from agents.vision_agent import vision_agent
from agents.structure_agent import structure_agent
from agents.reasoning_agent import reasoning_agent
from agents.accessibility_agent import accessibility_agent

class GraphState(TypedDict):
    image_path: str
    description: str
    structured: str
    reasoning: str
    final_output: str


def vision_node(state):
    return {"description": vision_agent(state["image_path"])}


def structure_node(state):
    return {"structured": structure_agent(state["description"])}


def reasoning_node(state):
    return {"reasoning": reasoning_agent(state["structured"])}


def accessibility_node(state):
    return {"final_output": accessibility_agent(state["reasoning"])}


def build_graph():
    graph = StateGraph(GraphState)

    graph.add_node("vision_step", vision_node)
    graph.add_node("structure_step", structure_node)
    graph.add_node("reasoning_step", reasoning_node)
    graph.add_node("accessibility_step", accessibility_node)

    graph.set_entry_point("vision_step")

    graph.add_edge("vision_step", "structure_step")
    graph.add_edge("structure_step", "reasoning_step")
    graph.add_edge("reasoning_step", "accessibility_step")

    graph.set_finish_point("accessibility_step")

    return graph.compile()