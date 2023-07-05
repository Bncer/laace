import urllib.parse
import requests
from datetime import datetime, timedelta
import json

from sqlalchemy import func

from config import settings
from schemas import CrimeBase
import models
from database import engine, SessionLocal 

def add_data(models, db_sesion):
    db = db_sesion()

    curr_days = db.query(models.Time.days).first()
    start_date = db.query(func.max(models.Crime.date_rptd)).first()[0]
    start_date += timedelta(days=1)
    day_diff = (datetime.now().date() - start_date.date()).days
    

    if not curr_days:
        db.add(models.Time(days=day_diff))
        db.commit()
    elif (day_diff - curr_days[0]) >= 1:
        day_offset = day_diff - curr_days[0]
        day_offset *= 3
        end_date = start_date + timedelta(days=day_offset)

        start_dt = start_date.strftime("%Y-%m-%dT%H:%M:%S")
        end_dt = end_date.strftime("%Y-%m-%dT%H:%M:%S")
        url = "https://data.lacity.org/resource/63jg-8b9z.json?$where=date_rptd between '{}' and '{}'&$$app_token={}"\
                .format(start_dt, end_dt, settings.api_token)
        
        response = requests.get(url).json()
        for res in response:
            c = json.dumps(res)
            crime = CrimeBase.parse_raw(c)
            new_crime = models.Crime(**crime.dict())
            db.add(new_crime)
            db.commit()
            print(crime.date_rptd, crime.crm_cd_desc)
        upd_day_diff = curr_days[0] - day_offset
        db.query(models.Time).\
            filter(models.Time.id == 1).\
            update({'days': upd_day_diff})
        db.commit()

if __name__=='__main__':
    add_data(models, SessionLocal)