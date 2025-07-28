# tools.py
import os, json, requests
from brave import Brave
from dotenv import load_dotenv

load_dotenv()
BRAVE_API_KEY     = os.getenv("BRAVE_API_KEY")
FIRECRAWL_API_KEY = os.getenv("FIRECRAWL_API_KEY")

def web_search(query: str) -> str:
    """Return top Brave results as JSON‐serialisable primitives."""
    brave  = Brave(api_key=BRAVE_API_KEY)
    result = brave.search(q=query, count=5)

    # Each item is a dict; make sure all values are JSON‑friendly
    web_results = [
        {
            "title":   item.get("title"),
            "url":     str(item.get("url")),   # HttpUrl → str
            "snippet": item.get("snippet"),
        }
        for item in getattr(result, "web_results", []) or []
    ]

    return json.dumps({"query": query, "web_results": web_results})

def scrape_url(url: str) -> str:
    """Use FireCrawl to pull cleaned markdown from a page."""
    resp = requests.post(
        "https://api.firecrawl.dev/scrape",
        headers={"Authorization": f"Bearer {FIRECRAWL_API_KEY}"},
        json={"url": url},
        timeout=30,
    )
    data     = resp.json()
    content  = data.get("markdown") or data.get("page_content") or ""
    return json.dumps({"url": url, "content": content})
