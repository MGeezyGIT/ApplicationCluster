import logging
from fastapi import APIRouter, BackgroundTasks, HTTPException
from app.utils.file_utils import load_matrix, save_matrix
from app.services.scrapy_service import scrape_content_from_url
from app.services.webhook_service import send_webhook_signal

router = APIRouter()

@router.post("/scrape-content")
async def scrape_content(background_tasks: BackgroundTasks):
    background_tasks.add_task(scrape_content_task)
    return {"message": "Content scraping started"}

def scrape_content_task():
    try:
        matrix = load_matrix()
        logging.debug("Loaded matrix for content scraping")

        for chapter in matrix["chapters"]:
            for keyword_entry in chapter["keywords"]:
                urls_with_content = []
                for index, url_entry in enumerate(keyword_entry["urls"], start=1):
                    url = url_entry["url"]
                    logging.debug(f"Scraping content from URL: {url}")
                    try:
                        content = scrape_content_from_url(url)
                        if content:
                            urls_with_content.append({f"url{index}": url, f"content{index}": content})
                            logging.debug(f"Scraped content from URL: {url}")
                        else:
                            urls_with_content.append({f"url{index}": url, f"content{index}": ""})
                            logging.warning(f"No content found for URL: {url}")
                    except Exception as scrape_error:
                        logging.error(f"Error scraping URL: {url}, error: {scrape_error}")
                        urls_with_content.append({f"url{index}": url, f"content{index}": ""})

                keyword_entry["urls"] = urls_with_content

        save_matrix(matrix)
        logging.debug("Updated matrix with scraped content successfully")
        
        # Send signal to Make.com webhook
        send_webhook_signal()
    except Exception as e:
        logging.error(f"Error during content scraping: {e}")
        raise HTTPException(status_code=500, detail="Error during content scraping")
