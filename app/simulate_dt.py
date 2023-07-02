from datetime import datetime, timedelta
import requests

from fastapi import Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.database import SessionLocal
from app import models
from app.config import settings


def daterange(start_date, end_date):
    for n in range(1, int((end_date - start_date).days)+1):
        yield start_date + timedelta(n)

def latest_date(db_sesion: Session):
    db = db_sesion()

    date_time = db.query(models.Time.days).first()
    start_date = db.query(func.max(models.Crime.date_rptd)).first()[0]
    day_diff = (datetime.now().date() - start_date.date()).days
    
    if not date_time:
        db.add(models.Time(days=day_diff))
        db.commit()

    else:
        day_offset = day_diff - date_time[0]
        day_offset *= 3
        print(day_offset)
        end_date = start_date + timedelta(days=day_offset)
        for single_date in daterange(start_date, end_date):
            print(single_date)
            print(date_time[0] - day_offset)            
            db.query(models.Time).\
                filter(models.Time.id == 1).\
                update({'days': date_time[0] - day_offset})
            db.commit()
        

latest_date(SessionLocal)