from tavily import TavilyClient
from .config import settings

_tavily_client = None


def get_tavily_client():
    global _tavily_client
    if _tavily_client is None:
        _tavily_client = TavilyClient(api_key=settings.tavily_api_key)
    return _tavily_client


def search_web(query: str, max_results: int = 5) -> str:
    client = get_tavily_client()
    response = client.search(query=query, max_results=max_results)

    results = response.get("results", [])
    if not results:
        return "No results found for this query."

    formatted = []
    for i, result in enumerate(results, start=1):
        title = result.get("title", "Untitled")
        url = result.get("url", "")
        content = result.get("content", "")
        formatted.append(f"[{i}] {title}\nURL: {url}\nSummary: {content}\n")

    return "\n".join(formatted)


TOOL_SPECS = [
    {
        "type": "function",
        "function": {
            "name": "search_web",
            "description": (
                "Search the web for current information on a topic. "
                "Returns a list of sources with titles, URLs, and short summaries."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The search query.",
                    },
                    "max_results": {
                        "type": "integer",
                        "description": "Number of results to return, default 5.",
                    },
                },
                "required": ["query"],
            },
        },
    }
]

TOOL_FUNCTIONS = {
    "search_web": search_web,
}
