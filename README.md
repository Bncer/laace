# laace
Los Angeles ACE - open source data and machine learning project of crime data of LA 

## Structure of this project

- [data_api](./data_api/) - [Los Angeles open data](https://data.lacity.org/) preparation and api to store in db.
- [backend](./backend/) - FastAPI backend server.
- [mlops](./mlops/) - Machine Learning Life Cycle.

### Development

1. `git clone git@github.com:opendatavibeq/laace.git`

2. `cd laace`

3. Create a virtual environment: python3 -m venv env

4. Activate the virtual environment: source env/bin/activate

5. Build a docker container with database: docker-compose up -d --build

6. Change directory: cd app/

7. Install requirements: pip install -r requirements.txt
