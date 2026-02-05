# Memory configuration Setup
from dotenv import load_dotenv
from mem0 import Memory
from openai import OpenAI
import json
import os


load_dotenv()

client = OpenAI()

OPEN_AI_API_KEY = os.getenv("OPENAI_API_KEY")

config = {
    "version": "v1.1",
    "embedder": {
        "provider": "openai",
        "config": {
            "api_key": OPEN_AI_API_KEY,
            "model": "text-embedding-3-small",
        }
    },
    "llm": {
        "provider": "openai",
        "config": {
            "api_key": OPEN_AI_API_KEY,
            "model": "gpt-4.1",
        }
    },
    "graph_store": {
        "provider": "neo4j",
        "config": {
            "url": "neo4j+s://83794e68.databases.neo4j.io",
            "username": "neo4j",
            "password": "Zft2fUpW31w5CPua-Lk441EIWev09V6pEbF0Ty-2xk0"
        }
    },
    "vector_store": {
        "provider": "qdrant",
        "config": {
            "host": "localhost",
            "port": 6333,
        }
    }
}

mem_client = Memory.from_config(config)

while True:
    user_query = input("Enter query >: ")

    # retrive the memory
    search_memory = mem_client.search(query=user_query, user_id="Ginwan")

    memories = [
        f"ID: {mem.get('id')}\nMemory: {mem.get("memory")}" for mem in search_memory.get("results")
    ]

    # print(f"Found memories: {memories}")

    SYSTEM_PROMPT = f"""
        Here is the context about the user:
        {json.dumps(memories)}
    """

    ai_response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_query}
        ]
    )

    print("🤖:", ai_response.choices[0].message.content)

    mem_client.add(
        user_id="Ginwan",
        messages=[
            {"role": "user", "content": user_query},
            {"role": "assistant",
                "content": ai_response.choices[0].message.content},
        ]
    )

    print("Memory saved ...")
