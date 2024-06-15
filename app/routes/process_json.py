# process_json.py
import logging
from fastapi import APIRouter, HTTPException, BackgroundTasks
from app.utils.file_utils import save_matrix, load_matrix
from app.services.google_search_service import perform_google_search
from app.routes.scrape_content import scrape_content_task
import os

router = APIRouter()

@router.post("/process-json")
async def process_json(data: dict, background_tasks: BackgroundTasks):
    logging.debug("Received JSON data for processing")
    chapters = data.get('chapters', [])

    if not chapters:
        logging.error("Invalid JSON structure: 'chapters' field is missing or empty")
        raise HTTPException(status_code=400, detail="Invalid JSON structure")

    matrix = {"chapters": []}

    for chapter in chapters:
        chapter_title = chapter.get('title', '')
        keywords = chapter.get('keywords', [])
        chapter_entry = {"title": chapter_title, "keywords": [], "content": ""}
        
        for keyword in keywords:
            chapter_entry["keywords"].append({"keyword": keyword, "urls": []})
        
        matrix["chapters"].append(chapter_entry)

    # Save the initial matrix
    save_matrix(matrix)
    logging.debug("Initial matrix saved successfully")

    try:
        # Automatically trigger the Google search after processing the JSON
        matrix = load_matrix()
        logging.debug("Loaded matrix for search")

        for chapter in matrix["chapters"]:
            for keyword_entry in chapter["keywords"]:
                keyword = keyword_entry["keyword"]
                logging.debug(f"Performing Google search for keyword: {keyword}")
                search_results = perform_google_search(keyword)
                logging.debug(f"Google search results for keyword '{keyword}': {search_results}")
                keyword_entry["urls"].extend(search_results)

        # Save the updated matrix with the URLs
        save_matrix(matrix)
        logging.debug("Updated matrix with URLs saved successfully")

        # Trigger content scraping as a background task
        logging.debug("Triggering content scraping")
        background_tasks.add_task(scrape_content_task)

        return {"message": "JSON processed, Google search completed, and content scraping triggered successfully"}
    except Exception as e:
        logging.error(f"Error during processing: {e}")
        raise HTTPException(status_code=500, detail=str(e))
