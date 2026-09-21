from crewai.tools import tool
from duckduckgo_search import DDGS

@tool("Search DuckDuckGo Stock Data")
def duckduckgo_stock_search(query: str) -> str:
    """Searches DuckDuckGo for concise stock fundamental and technical data."""
    try:
        with DDGS() as ddgs:
            # Reduced to 2 results to stay under token limits
            results = list(ddgs.text(query, max_results=2))
            if not results:
                return f"No results found for: {query}"
            
            output = []
            for r in results:
                # Truncate snippet text to 300 chars to save tokens
                snippet = r.get('body', '')[:300]
                output.append(f"Title: {r.get('title', '')}\nSnippet: {snippet}")
            return "\n---\n".join(output)
    except Exception as e:
        return f"Search error: {str(e)}"
