import logging
from fastapi import APIRouter, HTTPException, Request
import json

router = APIRouter()

@router.post("/save-data")
async def save_data(request: Request):
    try:
        # Check the content type and process accordingly
        if request.headers.get('content-type') == 'application/json':
            data = await request.json()
        else:
            data = await request.body()
            data = data.decode('utf-8')

        # Save the data to a file
        with open('saved_data.json', 'w') as f:
            if isinstance(data, dict):
                json.dump(data, f, indent=4)
            else:
                f.write(data)
        
        logging.debug("Data saved successfully")
        return {"message": "Data saved successfully"}
    except Exception as e:
        logging.error(f"Error saving data: {e}")
        raise HTTPException(status_code=500, detail="Error saving data")
