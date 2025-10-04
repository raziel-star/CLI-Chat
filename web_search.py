from serpapi import google_scholar_search
from config import SERPAPI_KEY

def search_web(query, num_results=10):
    try:
        params = {
            "engine": "google",
            "q": query,
            "api_key": SERPAPI_KEY,
            "num": num_results
        }
        search = google_scholar_search.GoogleSearch(params)
        results = search.get_dict()
        snippets = [item.get('snippet', '') for item in results.get('organic_results', [])[:num_results]]
        return '\n'.join(snippets) if snippets else "No results found."
    except Exception as e:
        return f"Search failed: {e}"

