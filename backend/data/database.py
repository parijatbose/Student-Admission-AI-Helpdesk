# database.py (ChromaDB version)

import chromadb
from chromadb.api.types import Documents, Embeddings, Metadatas

# Path to your ChromaDB persistent storage directory
CHROMA_DB_PATH = "./chroma_db"

# Singleton to maintain a single database client
_db_client = None


def get_db_client():
    """Get or create a ChromaDB persistent client."""
    global _db_client

    if _db_client is None:
        _db_client = chromadb.PersistentClient(path=CHROMA_DB_PATH)

    return _db_client


def get_collection(name: str):
    """Get or create a collection by name."""
    client = get_db_client()
    return client.get_or_create_collection(name=name)


def initialize_collections():
    """Initialize required collections for student admission data."""
    client = get_db_client()

    # Create necessary collections if they don't exist
    collections = [
        "students",
        "applications",
        "documents",
        "communication_logs",
        "loan_requests",
        "fee_slips",
        "agents",
        "admission_status"
    ]

    for name in collections:
        client.get_or_create_collection(name)

    print("ChromaDB collections initialized.")
