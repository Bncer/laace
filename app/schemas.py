from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class CrimeBase(BaseModel):
    dr_no: str
    date_rptd: datetime
    date_occ: datetime
    time_occ: datetime
    area: str
    area_name: str
    rpt_dist_no: str
    part_1_2: int
    crm_cd: str
    crm_cd_desc: str
    mocodes: Optional[str]
    vict_age: str
    vict_sex: Optional[str]
    vict_descent: Optional[str]
    premis_cd: Optional[str]
    premis_desc: Optional[str]
    weapon_used_cd: Optional[str]
    weapon_desc: Optional[str]
    status: Optional[str]
    status_desc: Optional[str]
    crm_cd_1: Optional[str]
    crm_cd_2: Optional[str]
    crm_cd_3: Optional[str]
    crm_cd_4: Optional[str]
    location: str
    cross_street: Optional[str]
    lat: float
    lon: float
