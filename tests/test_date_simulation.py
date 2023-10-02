import pytest
from unittest.mock import Mock
from app.database import SessionLocal
from app import models  # Import your models

from app.date_simulation import DateSimulation  # Import your DateSimulation class

@pytest.fixture
def mock_db_session(mocker):
    return mocker.patch("app.date_simulation.SessionLocal", autospec=True)

@pytest.fixture
def date_simulation(mock_db_session):
    return DateSimulation(settings=None, models=models)

def test_get_current_day_diff(date_simulation, mock_db_session):
    print(mock_db_session)
    mock_query = mock_db_session.return_value.query.return_value
    mock_query.first.return_value = (5,)

    curr_day_diff = date_simulation.get_current_day_diff()

    assert curr_day_diff == (5,)
