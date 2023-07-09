from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from apscheduler.schedulers.background import BackgroundScheduler

from . import models
from .database import engine 
from .date_simulation import load_data

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event('startup')
def init_data():
    scheduler = BackgroundScheduler()
    scheduler.add_job(
        load_data, 'cron', 
        args=[models], 
        hour= 23, 
        minute=30
    )
    scheduler.start()


@app.get("/")
def root():
    return {"message": "Los Angeles analysis"}
