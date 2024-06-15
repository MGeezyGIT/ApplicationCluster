import logging
from fastapi import APIRouter, HTTPException, Query
from app.utils.file_utils import load_matrix

router = APIRouter()

@router.get("/get-matrix")
async def get_matrix(chapter: str = Query(None), keyword: str = Query(None)):
    try:
        matrix = load_matrix()
        logging.debug("Loaded matrix for retrieval")

        if not chapter and not keyword:
            return matrix

        result = {}
        
        if chapter:
            result["chapter"] = next((chap for chap in matrix["chapters"] if chap["title"] == chapter), None)
            if not result["chapter"]:
                raise HTTPException(status_code=404, detail="Chapter not found")
        
        if keyword and result.get("chapter"):
            result["keyword"] = next((kw for kw in result["chapter"]["keywords"] if kw["keyword"] == keyword), None)
            if not result["keyword"]:
                raise HTTPException(status_code=404, detail="Keyword not found")

        return result
    except Exception as e:
        logging.error(f"Error retrieving matrix data: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/get-content")
async def get_content(chapter: str):
    try:
        matrix = load_matrix()
        logging.debug(f"Loaded matrix for chapter: {chapter}")

        # Find the specified chapter
        chapter_data = next((chap for chap in matrix["chapters"] if chap["title"] == chapter), None)
        if not chapter_data:
            raise HTTPException(status_code=404, detail="Chapter not found")

        return chapter_data
    except Exception as e:
        logging.error(f"Error retrieving content for chapter {chapter}: {e}")
        raise HTTPException(status_code=500, detail="Error retrieving content")
