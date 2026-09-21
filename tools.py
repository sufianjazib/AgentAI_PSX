import time
from crewai.tools import tool
from duckduckgo_search import DDGS

@tool("Search DuckDuckGo Stock Data")
def duckduckgo_stock_search(query: str) -> str:
    """Searches DuckDuckGo specifically for Pakistan Stock Exchange (PSX) financial data."""
    # Pause to respect Groq token bucket reset limits
    time.sleep(8)
    
    # Force PSX context if not already present in the prompt
    psx_query = query if "PSX" in query.upper() or "PAKISTAN" in query.upper() else f"{query} PSX stock Pakistan Stock Exchange"
    
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(psx_query, max_results=3))
            if not results:
                return f"No stock results found on DuckDuckGo for: {psx_query}"
            
            output = []
            for r in results:
                snippet = r.get('body', '')[:300]
                output.append(f"Title: {r.get('title', '')}\nSnippet: {snippet}\nLink: {r.get('href', '')}")
            return "\n---\n".join(output)
    except Exception as e:
        return f"Search error: {str(e)}"
