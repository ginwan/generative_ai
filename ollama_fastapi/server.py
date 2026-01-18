from fastapi import FastAPI, Body
from ollama import Client

app = FastAPI()
client = Client(
    host="http://localhost:11434",
)


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/contact")
def read_contact():
    return {"Contact": "This is the contact page"}


@app.post("/chat")
def Chat(message: str = Body(..., description="The Message")):
    response = client.chat(
        model="gemma:2b",
        messages=[
            {"role": "user", "content": message}
        ]
    )
    return {"response": response.message.content}


# @app.get("/items/{item_id}")
# def read_item(item_id: int, q: Union[str, None] = None):
#     return {"item_id": item_id, "q": q}
