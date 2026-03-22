from langgraph.graph import StateGraph, END
from typing import TypedDict

from agents.vision_agent import vision_agent
from agents.structure_agent import structure_agent
from agents.reasoning_agent import reasoning_agent
from agents.accessibility_agent import accessibility_agent

from openai import OpenAI
from config import OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY)


class GraphState(TypedDict):
    image_path: str
    description: str
    structured: str
    reasoning: str
    final_output: str
    question: str
    chat_answer: str
    user_decision: str  # confirm / reject / skip


# -------------------- NODES --------------------

def vision_node(state):
    return {
        "description": vision_agent(state["image_path"]),
        "user_decision": ""  # reset decision every time
    }


def hitl_node(state):
    return state


def structure_node(state):
    return {"structured": structure_agent(state["description"])}


def reasoning_node(state):
    return {"reasoning": reasoning_agent(state["structured"])}


def accessibility_node(state):
    return {"final_output": accessibility_agent(state["reasoning"])}


def chat_node(state):
    prompt = f"""
You are a STEM tutor helping a visually impaired student.

Full Context:
Description: {state['description']}
Structured Data: {state['structured']}
Reasoning: {state['reasoning']}
Final Explanation: {state['final_output']}

User Question:
{state['question']}

Answer deeply and clearly.
"""

    response = client.responses.create(
        model="gpt-4o-mini",
        input=prompt
    )

    return {
        "chat_answer": response.output[0].content[0].text
    }


# -------------------- ROUTERS --------------------

def entry_router(state):
    # Resume case (after decision)
    if state.get("user_decision"):
        if state["user_decision"] == "reject":
            return "vision_step"   # 🔥 LOOP BACK
        return "structure_step"

    # Chat flow
    if state.get("question"):
        return "chat_step"

    return "vision_step"


def hitl_router(state):
    decision = state.get("user_decision")

    if decision in ["confirm", "skip"]:
        return "structure_step"

    if decision == "reject":
        return "vision_step"  # 🔥 LOOP BACK

    return END


# -------------------- GRAPH --------------------

def build_graph():
    graph = StateGraph(GraphState)

    graph.add_node("vision_step", vision_node)
    graph.add_node("hitl_step", hitl_node)
    graph.add_node("structure_step", structure_node)
    graph.add_node("reasoning_step", reasoning_node)
    graph.add_node("accessibility_step", accessibility_node)
    graph.add_node("chat_step", chat_node)

    # Entry routing
    graph.set_conditional_entry_point(entry_router)

    # Flow
    graph.add_edge("vision_step", "hitl_step")

    # HITL decision routing
    graph.add_conditional_edges("hitl_step", hitl_router)

    # Main pipeline
    graph.add_edge("structure_step", "reasoning_step")
    graph.add_edge("reasoning_step", "accessibility_step")

    # End points
    graph.add_edge("accessibility_step", END)
    graph.add_edge("chat_step", END)

    return graph.compile()