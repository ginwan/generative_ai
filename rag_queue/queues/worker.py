# rq worker -w rq.worker.SimpleWorker for execute worker

from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from openai import OpenAI

load_dotenv()

openai_client = OpenAI()

# Vector Embedding for the chunks
embeddings_model = OpenAIEmbeddings(
    model="text-embedding-3-large",
)

# Load the vector store from Qdrant vector database
vector_store = QdrantVectorStore.from_existing_collection(
    url="http://localhost:6333",
    collection_name="learning_rag",
    embedding=embeddings_model,
)


def process_query(query: str):
    print(f"Searching Chunks : {query}")
    # Do a similarity search
    search_results = vector_store.similarity_search(query=query)
    context = "\n\n\n".join(
        [f"Page content: {result.page_content}\nPage Number: {result.metadata['page']}\nFile Location: {result.metadata['source']}" for result in search_results])
    SYSTEM_PROMPT = f"""
        You are a helpful AI assistant that answers questions about TypeScript based on the provided context retrieve from
        pdf document along with page contents and page number.

        You should ony answer the user based on the following content and navigate the user to the right page number to know more details.

        Context:
        {context}
    """
    response = openai_client.chat.completions.create(
        model="gpt-5",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": query},
        ]
    )
    print(f"🤖 : {response.choices[0].message.content}")
    return response.choices[0].message.content
