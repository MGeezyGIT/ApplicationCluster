import requests
import logging

WEBHOOK_URL = "https://hook.eu2.make.com/kxn70vvv19ov1nu4v73vwk5cqb5n133e"

def send_webhook_signal():
    try:
        response = requests.post(WEBHOOK_URL, json={"message": "Scraping completed"})
        response.raise_for_status()
        logging.debug(f"Successfully sent signal to Make.com webhook: {response.status_code}")
    except Exception as e:
        logging.error(f"Error sending signal to Make.com webhook: {e}")
