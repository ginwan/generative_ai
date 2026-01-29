# pip install -U pymongo langgraph langgraph-checkpoint-mongodb
from dotenv import load_dotenv

from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.mongodb import MongoDBSaver

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
    # print(f"\n\nInside chatbot: {state}")
    return {"messages": [response]}


# Create the graph
graph_builder = StateGraph(State)

# Add a node by specifying its name and the associated function or callable object
# register the node
graph_builder.add_node("chatbot", chatbot)

# Now create add edges
graph_builder.add_edge(START, "chatbot")
graph_builder.add_edge("chatbot", END)

# Flow look like this
# (START) -> chatbot -> (END)

# Graph is ready
# this simple graph
graph = graph_builder.compile()

# this graph with checkpointer


def compile_graph_with_checkpointer(checkpointer):
    graph = graph_builder.compile(checkpointer=checkpointer)
    return graph


MONGODB_URI = "mongodb://admin:admin@localhost:27017"

with MongoDBSaver.from_conn_string(MONGODB_URI) as checkpointer:
    graph_with_checkpointer = compile_graph_with_checkpointer(
        checkpointer=checkpointer)

    config = {
        "configurable": {
            "thread_id": "ginwan"
        }
    }
    # You have to pass initial state in invoke
    for chunk in graph_with_checkpointer.stream(
        State(messages=["what is my name?"]),
        config,
        stream_mode="values"
    ):
        chunk["messages"][-1].pretty_print()

    # print(f"\n\nUpdated State: {updated_state}")

# checkpointer ("ginwan") ==> "Hey, my name is Ginwan Elgasim"
