import requests
from bs4 import BeautifulSoup
import logging
import re

NCBI_API_KEY = "b75faa985ebecfd1c6228dcecda323958c09"

def clean_text(text):
    # Remove non-ASCII characters
    text = re.sub(r'[^\x00-\x7F]+', ' ', text)
    # Replace multiple spaces with a single space
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def scrape_content_from_url(url):
    try:
        logging.debug(f"Scraping content from URL: {url}")
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extract relevant content, customize as per your need
        paragraphs = soup.find_all('p')
        content = ' '.join([para.get_text() for para in paragraphs])
        return content
    except Exception as e:
        logging.error(f"Error scraping content from {url}: {e}")
        return None

def scrape_ncbi_content(url):
    try:
        logging.debug(f"Scraping NCBI content from URL: {url}")
        article_id = url.split("/")[-1]
        api_url = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=pubmed&id={article_id}&api_key={NCBI_API_KEY}"
        response = requests.get(api_url)
        response.raise_for_status()
        data = response.json()
        content = data.get('result', {}).get(article_id, {}).get('title', '') + "\n" + data.get('result', {}).get(article_id, {}).get('summary', '')
        return content
    except Exception as e:
        logging.error(f"Error scraping NCBI content from {url}: {e}")
        return None