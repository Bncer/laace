from apscheduler.schedulers.background import BackgroundScheduler
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app import models
from app.config import settings
from app.database import engine
from app.date_simulation import DateSimulation

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


@app.on_event("startup")
def init_data():
    scheduler = BackgroundScheduler()
    ds = DateSimulation(settings, models)
    scheduler.add_job(ds.load_data, "cron", args=[], hour=1, minute=34)
    scheduler.start()


@app.get("/")
def root():
    return {"message": "Los Angeles analysis"}
