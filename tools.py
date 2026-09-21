import time
import requests
from bs4 import BeautifulSoup
from crewai.tools import tool
from duckduckgo_search import DDGS

@tool("Get Live PSX Stock Price")
def get_live_psx_price(symbol: str) -> str:
    """Scrapes the exact live price for a Pakistan Stock Exchange (PSX) symbol from Sarmaaya.pk."""
    clean_symbol = symbol.strip().upper().replace(".PSX", "")
    url = f"https://sarmaaya.pk/stocks/company/{clean_symbol}"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            # Locate price element on Sarmaaya page
            price_element = soup.find("span", {"id": "stock-price"}) or soup.find("div", {"class": "price"})
            if price_element:
                return f"LIVE MARKET PRICE for {clean_symbol} on PSX: {price_element.text.strip()} PKR."
        
        return f"Could not fetch direct live price from portal for {clean_symbol}. Verify ticker."
    except Exception as e:
        return f"Error fetching live price: {str(e)}"

@tool("Search DuckDuckGo Stock Data")
def duckduckgo_stock_search(query: str) -> str:
    """Searches DuckDuckGo for recent news, announcements, and fundamental reports for PSX stocks."""
    time.sleep(8)  # Rate limit cooldown for Groq
    
    psx_query = f"{query} PSX Pakistan Stock Exchange analysis news 2026"
    
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(psx_query, max_results=3))
            if not results:
                return f"No results found for: {query}"
            
            output = []
            for r in results:
                snippet = r.get('body', '')[:250]
                output.append(f"Title: {r.get('title', '')}\nSnippet: {snippet}")
            return "\n---\n".join(output)
    except Exception as e:
        return f"Search error: {str(e)}"
