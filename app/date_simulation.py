import json
from datetime import datetime, timedelta

import requests
from sqlalchemy import func

from app import models
from app.config import settings
from app.database import SessionLocal
from app.schemas import CrimeBase


class DateSimulation:
    """
    Data loader to database from open API with fastforwarding days.
    In real time we spend 1 day in DateSimulation data will load for 3 days.
    """

    def __init__(self, settings, models):
        self.db = SessionLocal()
        self.settings = settings
        self.models = models
        self.curr_day_diff = self.get_current_day_diff()

    def get_current_day_diff(self):
        curr_day_diff = self.db.query(self.models.Time.days).first()
        return curr_day_diff

    def get_soure_data(self):
        start_date = self.db.query(func.max(self.models.Crime.date_rptd)).first()[0]
        start_date += timedelta(days=1)
        next_day_diff = (datetime.now().date() - start_date.date()).days
        return start_date, next_day_diff

    def insert_new_day_diff(self, day_diff):
        self.db.add(models.Time(days=day_diff))
        self.db.commit()

    def daterange(self, start_date, end_date):
        for n in range(int((end_date - start_date).days)):
            yield start_date + timedelta(n)

    def fastforward_days(self, next_val, start_dt, curr_val):
        day_offset = next_val - curr_val
        day_offset *= self.settings.fast_forward_number
        end_dt = start_dt + timedelta(days=day_offset)
        return end_dt, day_offset

    def request_data(self, curr_date):
        curr_date = curr_date.strftime("%Y-%m-%dT%H:%M:%S")
        print(curr_date)

        url = "{}?date_rptd='{}'&$$app_token={}".format(
            self.settings.api_host, curr_date, self.settings.api_token
        )

        response = requests.get(url).json()
        return response

    def validate_and_insert_data(self, resp):
        for res in resp:
            crime = json.dumps(res)
            crime_val = CrimeBase.parse_raw(crime)
            new_crime = models.Crime(**crime_val.dict())
            self.db.add(new_crime)
            self.db.commit()

    def update_day_diff(self, curr, offset):
        upd_day_diff = curr - offset
        self.db.query(self.models.Time).filter(self.models.Time.id == 1).update(
            {"days": upd_day_diff}
        )
        self.db.commit()

    def load_data(self):
        start_date, next_day_diff = self.get_soure_data()

        if not self.curr_day_diff:
            self.insert_new_day_diff(next_day_diff)

        elif (next_day_diff - self.curr_day_diff[0]) >= 1:
            end_date, day_offset = self.fastforward_days(
                next_day_diff, start_date, self.curr_day_diff[0]
            )
            for date in self.daterange(start_date, end_date):
                response = self.request_data(date)
                self.validate_and_insert_data(response)

            self.update_day_diff(self.curr_day_diff[0], day_offset)


if __name__ == "__main__":
    ds = DateSimulation(settings, models)
    ds.load_data()
