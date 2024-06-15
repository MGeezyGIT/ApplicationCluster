import logging
from fastapi import APIRouter, HTTPException
import json
import os

router = APIRouter()

@router.get("/get-saved-data")
async def get_saved_data():
    try:
        # Load the data from the file
        with open('saved_data.json', 'r') as f:
            data = f.read()
        
        logging.debug("Data retrieved successfully")
        
        # Try to parse as JSON if possible
        try:
            return json.loads(data)
        except json.JSONDecodeError:
            return {"data": data}
    except Exception as e:
        logging.error(f"Error retrieving data: {e}")
        raise HTTPException(status_code=500, detail="Error retrieving data")
