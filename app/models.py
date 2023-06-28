from sqlalchemy import Column, Integer, Float, String
from sqlalchemy.sql.sqltypes import TIMESTAMP

from .database import Base

class Crime(Base):
    __tablename__ = "crimes"

    dr_no = Column(String, primary_key=True, nullable=False)
    date_rptd = Column(TIMESTAMP,
                        nullable=False)
    date_occ = Column(TIMESTAMP,
                        nullable=False)
    time_occ = Column(String, nullable=True)
    area = Column(String, nullable=True)
    area_name = Column(String, nullable=True)
    rpt_dist_no = Column(String, nullable=True)
    part_1_2 = Column(Integer, nullable=True)
    crm_cd = Column(String, nullable=True)
    crm_cd_desc = Column(String, nullable=True)
    mocodes = Column(String, nullable=True)
    vict_age = Column(String, nullable=True)
    vict_sex = Column(String, nullable=True)
    vict_descent = Column(String, nullable=True)
    premis_cd = Column(Integer, nullable=True)
    premis_desc = Column(String, nullable=True)
    weapon_used_cd = Column(String, nullable=True)
    weapon_desc = Column(String, nullable=True)
    status = Column(String, nullable=True)
    status_desc = Column(String, nullable=True)
    crm_cd_1 = Column(String, nullable=True)
    crm_cd_2 = Column(String, nullable=True)
    location = Column(String, nullable=True)
    lat = Column(Float, nullable=True)
    lon = Column(Float, nullable=True)
