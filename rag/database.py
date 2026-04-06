import os
import threading
from qdrant_client import QdrantClient

# Global variables
_client = None
_lock = threading.Lock() # A thread lock to prevent race conditions

def get_client() -> QdrantClient:
    """Returns a single, shared Qdrant client instance in a thread-safe way."""
    global _client
    
    # When two tools try to connect at the exact same millisecond, 
    with _lock:
        if _client is None:
            print("🔒 Thread Lock acquired. Initializing Qdrant Database connection...")
            db_path = os.path.join(os.getcwd(), "qdrant_db")
            _client = QdrantClient(path=db_path)
            
    return _client