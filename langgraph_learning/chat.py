from dotenv import load_dotenv

from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain_openai import ChatOpenAI

load_dotenv()
# Create State => it is the first step of the langgraph


class State(TypedDict):
    # this message have a user query (user input or question or prompt)
    # Define messages (a list type, with the add_messages function used to append messages)
    messages: Annotated[list, add_messages]


# Define AI model
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

# Define a node ==> node is specific function to do a specific task


def chatbot(state: State):
    # state is a user message
    response = llm.invoke(state["messages"])
    print(f"\n\nInside chatbot: {state}")
    return {"messages": [response]}


def sample_node(state: State):
    # state is a user message
    print(f"\n\nInside sample_node: {state}")
    return {"messages": "This message from sample_node"}


# Create the graph
graph_builder = StateGraph(State)

# Add a node by specifying its name and the associated function or callable object
# register the node
graph_builder.add_node("chatbot", chatbot)
graph_builder.add_node("sample_node", sample_node)

# Now create add edges
graph_builder.add_edge(START, "chatbot")
graph_builder.add_edge("chatbot", "sample_node")
graph_builder.add_edge("sample_node", END)

# Flow look like this
# (START) -> chatbot -> sample_node -> (END)

# Graph is ready
graph = graph_builder.compile()

# You have to pass initial state in invoke
updated_state = graph.invoke(
    State(messages=["Hey, my name is Ginwan Elgasim"]))

print(f"\n\nUpdated State: {updated_state}")
