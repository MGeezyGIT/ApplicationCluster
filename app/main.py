# main.py
import os
import json
import logging
from dotenv import load_dotenv
from fastapi import FastAPI
from app.routes import process_json_router, get_matrix_router, scrape_content_router, save_data_router, get_saved_data_router
# Load environment variables from .env file
load_dotenv()

# Load service account info from JSON file specified in environment variable
SERVICE_ACCOUNT_FILE = os.getenv("SERVICE_ACCOUNT_FILE")
if not SERVICE_ACCOUNT_FILE:
    raise ValueError("SERVICE_ACCOUNT_FILE is not set in the environment variables")

with open(SERVICE_ACCOUNT_FILE) as f:
    service_account_info = json.load(f)

# Print to check if environment variables are loaded correctly
print("GOOGLE_API_KEY:", os.getenv("GOOGLE_API_KEY"))
print("GOOGLE_SEARCH_ENGINE_ID:", os.getenv("GOOGLE_SEARCH_ENGINE_ID"))
print("SERVICE_ACCOUNT_FILE:", SERVICE_ACCOUNT_FILE)

# Initialize FastAPI app
app = FastAPI()

# Include routers
app.include_router(process_json_router)
app.include_router(get_matrix_router)
app.include_router(scrape_content_router)
app.include_router(save_data_router)
app.include_router(get_saved_data_router)

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

@app.get("/")
async def root():
    return {"message": "Welcome to the FastAPI Content Generator"}
