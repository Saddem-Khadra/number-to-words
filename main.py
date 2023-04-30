import random
from functools import partial
import requests
from apscheduler.schedulers.background import BackgroundScheduler
from fastapi import FastAPI, Depends, Request
from starlette.middleware.cors import CORSMiddleware
from converter import convert_to_currency, Item, validate_input_data

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/api/converter/")
async def converter(item: Item = Depends(validate_input_data)):
    return {"message": convert_to_currency(item=item)}


def my_job(url: str):
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
    print(response.text)


@app.get("/")
async def schedule_job(request: Request):
    print(request.base_url)
    job_with_params = partial(my_job, url=f"{request.base_url}api/converter/")
    scheduler = BackgroundScheduler()
    scheduler.add_job(job_with_params, 'cron', minute='*/5')
    scheduler.start()
    return {"message": "converter request will run every 5 minutes"}
