# Conditional Edges
from dotenv import load_dotenv

from typing_extensions import TypedDict
from typing import Optional, Literal

from langgraph.graph import StateGraph, START, END
from openai import OpenAI


load_dotenv()

client = OpenAI()


class State(TypedDict):
    user_query: str
    llm_output: Optional[str]
    # check if the output is good
    is_good: Optional[bool]

# Define the node functions


def chatbot(state: State):
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "user", "content": state["user_query"]},
        ]
    )
    # llm output
    state["llm_output"] = response.choices[0].message.content
    return state


def evaluate_response(state: State) -> Literal["chatbot_gemini", "end_node"]:
    if False:
        return "end_node"
    return "chatbot_gemini"


def chatbot_gemini(state: State):
    response = client.chat.completions.create(
        model="gpt-4.1",
        messages=[
            {"role": "user", "content": state["user_query"]},
        ]
    )
    # llm output
    state["llm_output"] = response.choices[0].message.content
    return state


def end_node(state: State):
    return state


# Build Graph
graph_builder = StateGraph(State)


# register the node
graph_builder.add_node("chatbot", chatbot)
graph_builder.add_node("chatbot_gemini", chatbot_gemini)
graph_builder.add_node("end_node", end_node)

# add edges
graph_builder.add_edge(START, "chatbot")
graph_builder.add_conditional_edges("chatbot", evaluate_response)

graph_builder.add_edge("chatbot_gemini", "end_node")
graph_builder.add_edge("end_node", END)

graph = graph_builder.compile()

updated_state = graph.invoke(State({"user_query": "Hey, what is 2 + 2 ?"}))
print(f"Updated State: {updated_state}")
