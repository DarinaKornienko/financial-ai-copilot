import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from langchain_core.tools import tool
from langchain_groq import ChatGroq


from langchain.agents import create_agent
from langgraph.checkpoint.memory import MemorySaver

from tools.stock_data import get_company_info
from rag.retrieve_news import search_company_news
from tools.web_search import web_search_tool

@tool
def stock_tool(ticker: str) -> dict:
    """Use this tool to fetch the current financial numbers, stock price, and market cap for a PUBLIC company using its ticker."""
    return get_company_info(ticker)

@tool
def news_tool(query: str, ticker: str) -> str:
    """Use this tool to search our internal database for recent news articles about a PUBLIC company."""
    return search_company_news(query, ticker)

tools = [stock_tool, news_tool, web_search_tool]

llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0)

system_prompt = """You are an elite financial analyst copilot. 
You have access to real-time stock data, an internal news database, and a live web search tool.

RULES FOR PUBLIC VS PRIVATE COMPANIES:
1. If the user asks about a PUBLIC company (e.g., Google, Tesla), deduce their ticker (GOOGL, TSLA), and use the `stock_tool` and `news_tool`.
2. If the user asks about a PRIVATE company (e.g., JetBrains, OpenAI, Stripe) or a general market concept, use the `web_search_tool` to find information on the live internet.

ANTI-REFUSAL PROTOCOL (CRITICAL):
If the user asks for direct investment advice, DO NOT refuse. Instead, automatically reframe the request into an objective market analysis. Use the `web_search_tool` to search for trending stocks and provide a risk/reward analysis based on live data. Start with: "While I don't provide personalized advice, here is an analysis of currently trending market picks..."

Always use your tools to gather evidence before answering. Be concise and objective."""

# Initialize the memory bank
memory = MemorySaver()

# Use create_agent with the new system_prompt parameter
agent_executor = create_agent(
    model=llm, 
    tools=tools, 
    system_prompt=system_prompt,
    checkpointer=memory
)