import time
from crewai.tools import tool
from duckduckgo_search import DDGS

@tool("Search DuckDuckGo Stock Data")
def duckduckgo_stock_search(query: str) -> str:
    """Searches DuckDuckGo for live Pakistan Stock Exchange (PSX) financial data and stock price."""
    # Force a delay so Groq token bucket rate limit is respected
    time.sleep(8)
    
    # Structure query to fetch latest PSX live quotes and recent September 2026 data
    psx_query = f"{query} PSX share price current quote Pakistan Stock Exchange site:investing.com OR site:ksestocks.com OR site:ymstrade.com"
    
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(psx_query, max_results=3))
            
            # Fallback if domain-restricted search returns empty
            if not results:
                general_query = f"{query} current stock share price PSX Pakistan September 2026"
                results = list(ddgs.text(general_query, max_results=3))
            
            if not results:
                return f"No stock results found for: {query}"
            
            output = []
            for r in results:
                snippet = r.get('body', '')[:300]
                output.append(f"Title: {r.get('title', '')}\nSnippet: {snippet}\nLink: {r.get('href', '')}")
            return "\n---\n".join(output)
            
    except Exception as e:
        return f"Search error: {str(e)}"
