import requests
from datetime import datetime, timedelta
import json

from sqlalchemy import func

from .config import settings
from .schemas import CrimeBase
from . import models
from .database import SessionLocal 

db = SessionLocal()

def get_soure_data():

    curr_day_diff = db.query(models.Time.days).first()
    start_date = db.query(func.max(models.Crime.date_rptd)).first()[0]
    start_date += timedelta(days=1)
    next_day_diff = (datetime.now().date() - start_date.date()).days

    return curr_day_diff, start_date, next_day_diff

def insert_new_day_diff(day_diff):

    db.add(models.Time(days=day_diff))
    db.commit()

def fastforward_days(next_val, start_dt, curr_val):

    day_offset = next_val - curr_val
    day_offset *= 3
    end_dt = start_dt + timedelta(days=day_offset)
    
    return end_dt, day_offset

def request_data(start, end):
    
    start_dt = start.strftime("%Y-%m-%dT%H:%M:%S")
    end_dt = end.strftime("%Y-%m-%dT%H:%M:%S")
    url = "{}?$where=date_rptd between '{}' and '{}'&$$app_token={}"\
                .format(settings.api_host, start_dt, end_dt, settings.api_token)
        
    response = requests.get(url).json()

    return response

def validate_and_load_data(resp):
    for res in resp:
        crime = json.dumps(res)
        crime_val = CrimeBase.parse_raw(crime)
        new_crime = models.Crime(**crime_val.dict())
        db.add(new_crime)
        db.commit()
        print(crime_val.date_rptd, crime_val.crm_cd_desc)

def update_day_diff(curr, offset):

    upd_day_diff = curr - offset
    db.query(models.Time).\
        filter(models.Time.id == 1).\
        update({'days': upd_day_diff})
    db.commit()

def load_data(models):

    curr_day_diff, start_date, next_day_diff = get_soure_data()

    if not curr_day_diff:
        insert_new_day_diff(next_day_diff)

    elif (next_day_diff - curr_day_diff[0]) >= 1:
        end_date, day_offset = fastforward_days(next_day_diff, 
                                                start_date, 
                                                curr_day_diff[0]
                                                )

        response = request_data(start_date, end_date)

        validate_and_load_data(response)

        update_day_diff(curr_day_diff[0], day_offset)


if __name__=='__main__':
    load_data(models, SessionLocal)