import requests
from datetime import datetime, timedelta

from sqlalchemy import func

from app.config import settings
from app.schemas import CrimeBase


def add_data(models, db_sesion):
    db = db_sesion()

    curr_days = db.query(models.Time.days).first()
    start_date = db.query(func.max(models.Crime.date_rptd)).first()[0]
    day_diff = (datetime.now().date() - start_date.date()).days
    
    if not curr_days:
        db.add(models.Time(days=day_diff))
        db.commit()

    else:
        day_offset = day_diff - curr_days[0]
        day_offset *= 3
        start_date += timedelta(days=1)
        end_date = start_date + timedelta(days=day_offset)
        
        url = "https://data.lacity.org/resource/63jg-8b9z.json?$where=date_rptd between {} and {}&$$app_token={}".format(str(start_date), str(end_date), settings.api_token)
        
        response = requests.get(url)
        print(response.json())
        upd_day_diff = curr_days[0] - day_offset
        db.query(models.Time).\
            filter(models.Time.id == 1).\
            update({'days': upd_day_diff})
        db.commit()
