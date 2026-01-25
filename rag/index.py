from dotenv import load_dotenv

from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore

load_dotenv()

BASE_DIR = Path(__file__).parent

pdf_path = BASE_DIR / "typescript.pdf"

print("File exists:", pdf_path.exists())

# Load the PDF file in python program
loader = PyPDFLoader(str(pdf_path))
docs = loader.load()

# Split the document into smaller chunks
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    # overlap between chunks to maintain context
    chunk_overlap=200,
)
chunks = text_splitter.split_documents(documents=docs)

# Vector Embedding for the chunks
embeddings_model = OpenAIEmbeddings(
    model="text-embedding-3-large",
)

# Store the embeddings in Qdrant vector database
vector_store = QdrantVectorStore.from_documents(
    documents=chunks,
    embedding=embeddings_model,
    url="http://localhost:6333",
    collection_name="learning_rag",
)

print("Indexing of documents done...")
