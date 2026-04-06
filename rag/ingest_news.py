import yfinance as yf
from qdrant_client.models import Distance, VectorParams, PointStruct
from sentence_transformers import SentenceTransformer
import uuid
from rag.database import get_client

def ingest_company_news(ticker: str):
    print(f"\nFetching recent news for {ticker}...")
    stock = yf.Ticker(ticker)
    news_items = stock.news
    
    if not news_items:
        print(f"No news found for {ticker}.")
        return

    print("Loading embedding model (all-MiniLM-L6-v2)...")
    model = SentenceTransformer('all-MiniLM-L6-v2')
    
    # Use the global client
    client = get_client()
    collection_name = "financial_news"
    
    if not client.collection_exists(collection_name):
        print(f"Creating new Qdrant collection: {collection_name}")
        client.create_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(size=384, distance=Distance.COSINE),
        )

    points = []
    for item in news_items:
        if 'content' in item:
            title = item['content'].get('title', 'No Title')
            publisher = item['content'].get('provider', {}).get('displayName', 'Unknown')
            summary = item['content'].get('summary', '')
        else:
            title = item.get('title', 'No Title')
            publisher = item.get('publisher', 'Unknown')
            summary = item.get('summary', '')
            
        text_to_embed = f"Company: {ticker}\nTitle: {title}\nPublisher: {publisher}\nSummary: {summary}"
        vector = model.encode(text_to_embed).tolist()
        
        points.append(PointStruct(
            id=str(uuid.uuid4()), vector=vector,
            payload={"ticker": ticker, "title": title, "publisher": publisher, "text": text_to_embed}
        ))

    client.upsert(collection_name=collection_name, points=points)
    print(f"Successfully stored news for {ticker} in Qdrant!")