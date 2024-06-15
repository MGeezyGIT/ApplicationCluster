# google_search_service.py
import requests
import logging
import os

# Load environment variables explicitly (for debugging)
from dotenv import load_dotenv
load_dotenv()

API_KEY = os.getenv("GOOGLE_API_KEY")
SEARCH_ENGINE_ID = os.getenv("GOOGLE_SEARCH_ENGINE_ID")

def perform_google_search(query, num_results=5):
    try:
        logging.debug(f"GOOGLE_API_KEY: {API_KEY}")
        logging.debug(f"GOOGLE_SEARCH_ENGINE_ID: {SEARCH_ENGINE_ID}")

        if not API_KEY or not SEARCH_ENGINE_ID:
            raise ValueError("API_KEY or SEARCH_ENGINE_ID is not set")
        
        logging.debug(f"Sending Google search request for query: {query}")
        url = f"https://www.googleapis.com/customsearch/v1?q={query}&key={API_KEY}&cx={SEARCH_ENGINE_ID}&num={num_results}"
        response = requests.get(url)
        response.raise_for_status()
        logging.debug(f"Google API response for query '{query}': {response.json()}")
        results = response.json().get("items", [])
        return [{"url": item["link"], "content": ""} for item in results]
    except requests.exceptions.RequestException as e:
        logging.error(f"Error during Google search: {e}")
        raise
    except ValueError as e:
        logging.error(f"Configuration error: {e}")
        raise
