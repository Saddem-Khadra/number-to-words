import random
from functools import partial
import requests
from apscheduler.schedulers.background import BackgroundScheduler
from fastapi import FastAPI, Depends, Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware.cors import CORSMiddleware
from converter import convert_to_currency, Item, validate_input_data
from logger import logger
from middleware import log_middleware

app = FastAPI(swagger_ui_parameters={"syntaxHighlight.theme": "obsidian"})
app.add_middleware(
    BaseHTTPMiddleware,
    dispatch=log_middleware,
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/api/converter/")
async def converter(item: Item = Depends(validate_input_data)):
    logger.info(f"Received conversion request: {item}")
    result = convert_to_currency(item=item)
    logger.info(f"Conversion result: {result}")
    return {"message": result}


def my_job(url: str):
    logger.info("Scheduled job running...")
    payload = {
        "number": random.uniform(1, 99999),
        "delete_from_sentence": None,
        "currency": "euros",
        "decimal_currency": "millimes",
        "separator": "et",
        "decimal": 3,
        "language": "fr"
    }
    headers = {'content-type': 'application/json'}
    response = requests.post(url, json=payload, headers=headers)
    logger.info(f"Job response: {response.text}")


@app.get("/")
async def schedule_job(request: Request):
    logger.info(f"Received schedule job request: {request.base_url}")
    job_with_params = partial(my_job, url=f"{request.base_url}api/converter/")
    scheduler = BackgroundScheduler()
    scheduler.add_job(job_with_params, 'cron', minute='*/5')
    scheduler.start()
    logger.info("Job scheduled to run every 5 minutes.")
    return {"message": "Converter request will run every 5 minutes"}
