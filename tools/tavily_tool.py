import os

from dotenv import load_dotenv
from tavily import TavilyClient
from langchain_core.tools import tool

load_dotenv()

TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

if not TAVILY_API_KEY:
    raise ValueError("TAVILY_API_KEY is not configured.")

client = TavilyClient(api_key=TAVILY_API_KEY)


@tool
def search_destination(destination: str) -> str:
    """
    Research a travel destination.
    Finds popular attractions, culture, and useful travel information.
    """

    response = client.search(
        query=f"travel guide for {destination}: attractions, culture, food, travel tips",
        max_results=5,
    )

    results = []

    for result in response.get("results", []):
        results.append(
            f"Title: {result.get('title')}\n"
            f"URL: {result.get('url')}\n"
            f"Content: {result.get('content', '')[:1000]}"
        )

    return "\n\n---\n\n".join(results)


if __name__ == "__main__":
    result = search_destination.invoke(
        {"destination": "Bhubaneswar, India"}
    )

    print(result)
    