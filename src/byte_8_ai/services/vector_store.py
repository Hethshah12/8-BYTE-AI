from pathlib import Path
import chromadb
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction

CHROMA_FOLDER=Path(__file__).resolve().parents[3]/"data"/"chroma"

EMBEDDING_MODEL="all-MiniLM-l6-v2"

def get_collection(name:str, embedding_function=None):
    client=chromadb.PersistentClient(path=str(CHROMA_FOLDER))
    if embedding_function is None:
        embedding_function=SentenceTransformerEmbeddingFunction(model_name=EMBEDDING_MODEL)
    return client.get_or_create_collection(name=name, embedding_function=embedding_function, configuration={"hnsw":{"space":"cosine"}})

