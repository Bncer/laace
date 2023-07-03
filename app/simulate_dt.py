import requests
from datetime import datetime, timedelta

from sqlalchemy import func

from app.config import settings
from app.schemas import CrimeBase


def daterange(start_date, end_date):
    for n in range(1, int((end_date - start_date).days)+1):
        yield start_date + timedelta(n)

def add_data(models, db_sesion):
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
        end_date = start_date + timedelta(days=day_offset)
        print(date_time[0] - day_offset)
        for single_date in daterange(start_date, end_date):
            print(single_date)
            db.query(models.Time).\
                filter(models.Time.id == 1).\
                update({'days': date_time[0] - day_offset})
            db.commit()
