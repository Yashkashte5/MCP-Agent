import uuid
from datetime import datetime

import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer


# Persistent Chroma client
client = chromadb.Client(
    Settings(
        persist_directory="./vector_db",
        anonymized_telemetry=False
    )
)

collection = client.get_or_create_collection("agent_memory")

# Lightweight embedding model
embedder = SentenceTransformer("all-MiniLM-L6-v2")


# --------------------------------------------------
# STORE MEMORY
# --------------------------------------------------
def store_memory(text: str, metadata: dict | None = None):
    """
    Stores conversational memory in Chroma vector DB.
    Ensures metadata is valid and includes timestamp.
    """

    try:
        embedding = embedder.encode(text).tolist()

        # Ensure metadata exists
        metadata = metadata or {}

        # Add default metadata safely
        metadata.setdefault("source", "agent_memory")
        metadata.setdefault("timestamp", datetime.utcnow().isoformat())

        collection.add(
            documents=[text],
            embeddings=[embedding],
            metadatas=[metadata],
            ids=[str(uuid.uuid4())]
        )

    except Exception as e:
        print("Vector memory store error:", e)


# --------------------------------------------------
# RETRIEVE MEMORY
# --------------------------------------------------
def retrieve_memory(query: str, k: int = 3):
    """
    Retrieves semantically similar memories.
    """

    try:
        embedding = embedder.encode(query).tolist()

        results = collection.query(
            query_embeddings=[embedding],
            n_results=k,
            include=["documents", "distances"]
        )

        docs = results.get("documents", [[]])[0]
        distances = results.get("distances", [[]])[0]

        # Optional similarity filtering
        filtered_docs = []
        SIMILARITY_THRESHOLD = 1.5  # lower = stricter

        for doc, dist in zip(docs, distances):
            if dist <= SIMILARITY_THRESHOLD:
                filtered_docs.append(doc)

        return filtered_docs

    except Exception as e:
        print("Vector memory retrieval error:", e)
        return []
