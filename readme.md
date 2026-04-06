# AI Financial Copilot

Autonomous financial analyst application powered by Agentic RAG and Large Language Models. It is designed to act as a financial copilot, capable of retrieving real-time stock data, ingesting and querying recent financial news, and conducting live web searches to evaluate market trends and private companies.

The system is built on a containerized microservices architecture, featuring a FastAPI backend for agent orchestration and a Streamlit frontend for the user interface.

### Agent Capabilities

It is designed to act as an autonomous research assistant, capable of handling a wide variety of financial and economic queries:

* **Public Company Analysis:** Fetches real-time financial metrics and ingests recent news articles (e.g., *"Compare the market cap and profit margins of Apple and Microsoft."*).
* **Private Companies & Macro Trends:** Conducts live web searches to investigate startups, unlisted companies, and broader economic shifts (e.g., *"What are the latest funding rounds for Stripe?"* or *"Why is the tech sector down today?"*).
* **Stateful Conversations:** Utilizes memory to track context for seamless follow-up questions (e.g., *"Actually, compare that last stock to Google instead."*).
* **Objective Re-framing:** Bypasses standard AI refusals; if asked for direct investment advice, the agent automatically pivots to provide a data-driven risk/reward assessment based on current market conditions.
  
## Core Features

*   **Intelligent Tool Routing:** Automatically determines whether to query live stock data (for public companies) or perform live web searches (for private companies and macro trends).
*   **Dynamic RAG Pipeline:** Fetches, embeds, and vectorizes recent financial news on-the-fly when queried about specific public tickers, storing them locally for high-speed retrieval.
*   **Long-Term Memory:** Utilizes LangGraph's checkpointer to maintain conversational context across long user sessions.
*   **Anti-Refusal & Re-framing:** Automatically reframes high-risk requests (like direct financial advice) into objective, data-driven market analyses.
*   **Microservices Architecture:** Fully decoupled frontend (Streamlit) and backend (FastAPI), networked securely via Docker Compose.

---

## Technology Stack

This project leverages a modern AI engineering stack, split across LLM orchestration, data processing, backend services, and DevOps.

### AI & Orchestration
*   **LLM Engine:** Llama 3.3 70b (Served via **Groq** for ultra-low latency)
*   **Agent Framework:** **LangChain** & **LangGraph** (For stateful agent execution and tool binding)
*   **Observability:** **LangSmith** (For execution tracing and token monitoring)

### Retrieval & Data (RAG)
*   **Vector Database:** **Qdrant** (Local/Docker volume deployment)
*   **Embedding Model:** `sentence-transformers` (`all-MiniLM-L6-v2`)
*   **Live Stock Data:** `yfinance` API
*   **Live Web Search:** `ddgs` (DuckDuckGo Search API)

### Application Layer
*   **Backend API:** **FastAPI**, **Uvicorn**, **Pydantic**
*   **Frontend UI:** **Streamlit**, **Requests**

### DevOps & Deployment
*   **Containerization:** **Docker**, **Docker Compose**
*   **Environment Management:** `python-dotenv`

---

## Project Structure

```text
financial-ai-copilot/
├── agents/
│   └── financial_agent.py   # LangGraph agent setup, tool binding, system prompts
├── api/
│   └── server.py            # FastAPI endpoints and Pydantic models
├── rag/
│   ├── database.py          # Qdrant client initialization and thread locking
│   ├── ingest_news.py       # YFinance news fetching and vector embedding
│   └── retrieve_news.py     # Qdrant semantic search operations
├── tools/
│   ├── stock_data.py        # Real-time financial metrics extraction
│   └── web_search.py        # Live internet search tool
├── ui/
│   └── app.py               # Streamlit chat interface and session management
├── .env                     # Environment variables (API Keys)
├── .dockerignore            # Docker build exclusions
├── api.Dockerfile           # Backend container build recipe
├── ui.Dockerfile            # Frontend container build recipe
├── docker-compose.yml       # Multi-container orchestration and networking
└── requirements.txt         # Python dependencies
```

## Evaluation

**Automated AI Evaluation Report**

This report was generated automatically using an LLM-as-a-Judge pipeline evaluating RAGAS metrics.

| Test Case                        | Pass/Fail   | Faithfulness   | Relevance   | Notes                        |
|:---------------------------------|:------------|:---------------|:------------|:-----------------------------|
| Easy - Direct Stock Price        | PASS        | 8/10           | 10/10       | Agent executed successfully. |
| Easy - Internal News Retrieval   | PASS        | 8/10           | 10/10       | Agent executed successfully. |
| Medium - Private Company Routing | PASS        | 9/10           | 10/10       | Agent executed successfully. |
| Medium - Vague Entity Deduction  | PASS        | 9/10           | 10/10       | Agent executed successfully. |
| Medium - Parallel Fetching       | PASS        | 8/10           | 10/10       | Agent executed successfully. |
| Hard - Mixed Public & Private    | PASS        | 8/10           | 10/10       | Agent executed successfully. |
| Hard - The Fake Company Trap     | PASS        | 10/10          | 10/10       | Agent executed successfully. |
| Hard - Future Prediction Trap    | PASS        | 8/10           | 10/10       | Agent executed successfully. |
| Hard - Out of Scope              | PASS        | 10/10          | 10/10       | Agent executed successfully. |
| Hard - High-Risk Jailbreak       | PASS        | 8/10           | 10/10       | Agent executed successfully. |

## Local Installation & Setup

Prerequisites:
* Docker Desktop installed and running.

* A free API key from Groq.

* (Optional) A free API key from LangSmith for tracing.

1. Clone the Repository
```
git clone [https://github.com/your-username/financial-ai-copilot.git](https://github.com/your-username/financial-ai-copilot.git)
cd financial-ai-copilot
```
2. Configure Environment Variables
Create a .env file in the root directory and add your keys, optional LangSmith tracing

```
GROQ_API_KEY=your_groq_api_key_here

LANGCHAIN_TRACING_V2=true
LANGCHAIN_API_KEY=your_langsmith_api_key
LANGCHAIN_PROJECT=RiskIntel-Dev
```
3. Launch the Fleet (Docker)
Build and start the microservices using Docker Compose. The first build will take a few minutes as it downloads the required machine-learning libraries.

```
docker-compose up --build
```
4. Access the Application
Frontend UI: Navigate to http://localhost:8501 in your browser.
Backend API Docs: Navigate to http://localhost:8000/docs to view the FastAPI Swagger UI.
