# from unittest import mock
# import pytest

# from app.database import SessionLocal
# from app.date_simulation import DateSimulation
# from app import models

# @pytest.fixture
# def mock_db_session():
    # with mock.patch("app.database.SessionLocal") as db_session:
        # yield  db_session.return_value
# def test_get_current_day_diff():
    # session = mock.MagicMock()
    # settings = mock.Mock()
    # models = mock.Mock()

    # simulation = DateSimulation(settings, models)
    # simulation.get_current_day_diff()
    # simulation.get_current_day_diff.assert_called_once()

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
    mock_query = mock_db_session.return_value.query.return_value
    mock_query.first.return_value = (5,)

    curr_day_diff = date_simulation.get_current_day_diff()

    assert curr_day_diff == (5,)
