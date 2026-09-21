from crewai.tools import tool
from duckduckgo_search import DDGS

@tool("Search DuckDuckGo Stock Data")
def duckduckgo_stock_search(query: str) -> str:
    """Searches DuckDuckGo for stock fundamental data, technical indicators, financial news, and growth prospects."""
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=5))
            if not results:
                return f"No stock research results found for: {query}"
            
            output = []
            for r in results:
                output.append(f"Title: {r.get('title', '')}\nSnippet: {r.get('body', '')}\nLink: {r.get('href', '')}\n")
            return "\n---\n".join(output)
    except Exception as e:
        return f"Error executing DuckDuckGo search: {str(e)}"
