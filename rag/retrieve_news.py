from qdrant_client.models import Filter, FieldCondition, MatchValue
from sentence_transformers import SentenceTransformer
from rag.database import get_client
from rag.ingest_news import ingest_company_news

def search_company_news(query: str, ticker: str = None, top_k: int = 3, _is_retry: bool = False) -> str:
    print(f"\nSearching database for: '{query}' (Ticker filter: {ticker})...")
    model = SentenceTransformer('all-MiniLM-L6-v2')
    query_vector = model.encode(query).tolist()

    # Use the global client
    client = get_client()
    collection_name = "financial_news"
    
    # Ensure collection exists before searching
    if not client.collection_exists(collection_name):
        if not _is_retry and ticker:
             ingest_company_news(ticker)
             return search_company_news(query, ticker, top_k, _is_retry=True)
        return "Database is empty."
        
    query_filter = None
    if ticker:
        query_filter = Filter(must=[FieldCondition(key="ticker", match=MatchValue(value=ticker))])

    search_response = client.query_points(
        collection_name=collection_name, query=query_vector, query_filter=query_filter, limit=top_k
    )
    
    search_results = search_response.points

    if not search_results:
        if not _is_retry and ticker:
            print(f"No data found for {ticker}. Initiating Dynamic Auto-Ingestion...")
            ingest_company_news(ticker)
            return search_company_news(query, ticker, top_k, _is_retry=True)
        else:
            return f"No relevant news found for {ticker}."

    return "\n".join([f"- [{hit.payload['publisher']}] {hit.payload['title']}" for hit in search_results])