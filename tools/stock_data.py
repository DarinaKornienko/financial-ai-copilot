import yfinance as yf
import pandas as pd

def get_company_info(ticker: str) -> dict:
    """
    Fetches core financial information for a given company ticker.
    This will be used by the AI agent to understand the company's current standing.
    """
    print(f"Fetching data for {ticker}...")
    stock = yf.Ticker(ticker)
    info = stock.info
    
    # We extract only the most critical financial metrics to avoid overwhelming the LLM
    structured_data = {
        "Company Name": info.get("shortName", "N/A"),
        "Sector": info.get("sector", "N/A"),
        "Current Price": info.get("currentPrice", "N/A"),
        "Market Cap": info.get("marketCap", "N/A"),
        "Forward PE": info.get("forwardPE", "N/A"),
        "Profit Margins": info.get("profitMargins", "N/A"),
        "52 Week High": info.get("fiftyTwoWeekHigh", "N/A"),
        "52 Week Low": info.get("fiftyTwoWeekLow", "N/A"),
        "Analyst Recommendation": info.get("recommendationKey", "N/A")
    }
    
    return structured_data

# Testing the tool 
if __name__ == "__main__":
    # Test with Apple and Tesla
    apple_data = get_company_info("AAPL")
    tesla_data = get_company_info("TSLA")
    
    print("\n--- Apple Data ---")
    for key, value in apple_data.items():
        print(f"{key}: {value}")
        
    print("\n--- Tesla Data ---")
    for key, value in tesla_data.items():
        print(f"{key}: {value}")