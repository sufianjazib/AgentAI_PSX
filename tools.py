import time
from crewai.tools import tool
from duckduckgo_search import DDGS

@tool("Search DuckDuckGo Stock Data")
def duckduckgo_stock_search(query: str) -> str:
    """Searches DuckDuckGo for concise stock fundamental and technical data."""
    # Force a 12-second pause before tool response to allow Groq TPM token bucket to reset
    time.sleep(12)
    
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=2))
            if not results:
                return f"No results found for: {query}"
            
            output = []
            for r in results:
                # Truncate body to 200 characters to keep context small
                snippet = r.get('body', '')[:200]
                output.append(f"Title: {r.get('title', '')}\nSnippet: {snippet}")
            return "\n---\n".join(output)
    except Exception as e:
        return f"Search error: {str(e)}"
