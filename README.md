LAACE (Los Angeles ACE) - open source data and machine learning project of crime data of LA 
=============================================

## Structure of the project

- [app](./app/) - [Los Angeles open data](https://data.lacity.org/) preparation and api to store in db
                           and FastAPI backend server.
- [mlops](./mlops/) - Machine Learning Life Cycle.

### Installation

1. Clone the repository
   
       git clone git@github.com:Bncer/laace.git && cd laace

2. Create a virtual environment and activate:
   
       python3 -m venv env && source env/bin/activate

3. Install requirements:
    
       pip install -r requirements.txt
   
5. Start the backend application:

       uvicorn app.main:app --reload
