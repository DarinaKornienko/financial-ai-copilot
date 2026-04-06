from langchain_community.tools import DuckDuckGoSearchRun
from langchain_core.tools import tool

@tool
def web_search_tool(query: str) -> str:
    """
    Use this tool to search the live internet for news, risks, and general information. 
    This is CRITICAL to use when asked about PRIVATE COMPANIES that do not have public stock tickers.
    """
    print(f"\n🌐 Initiating Web Search for: {query}...")
    search = DuckDuckGoSearchRun()
    
    try:
        results = search.invoke(query)
        return results
    except Exception as e:
        return f"Web search failed: {e}"

# 
if __name__ == "__main__":
    print(web_search_tool.invoke("Latest news and risks regarding JetBrains software company"))