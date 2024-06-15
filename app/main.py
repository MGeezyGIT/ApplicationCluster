# main.py
import os
import logging
from dotenv import load_dotenv
from fastapi import FastAPI
from app.routes import process_json_router, get_matrix_router, scrape_content_router, save_data_router

load_dotenv()  # Load environment variables from .env file

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

app = FastAPI()

app.include_router(process_json_router)
app.include_router(get_matrix_router)
app.include_router(scrape_content_router)
app.include_router(save_data_router)

@app.get("/")
async def root():
    return {"message": "Welcome to the FastAPI Content Generator"}
