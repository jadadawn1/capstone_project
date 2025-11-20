# Climate Signals: Climate Change Indicators API & Dashboard

## Overview
In this mini-lab, you will build a FastAPI application to manage and analyze a global climate dataset, test it with pytest, set up CI/CD using GitHub Actions, and deploy it to Google Cloud Run. You will also configure an Ubuntu VM on Google Cloud Platform (GCP) with Chrome Remote Desktop to replicate the entire workflow.  
The dataset contains climate indicators such as average temperature, CO₂ emissions, sea-level rise, rainfall, renewable energy %, forest area %, population, and extreme weather events for different countries over time.

A rubric will be used to assess your submission on Canvas.

## Learning Objectives
By completing this project, you will be able to:

- Build a REST API using FastAPI and SQLite  
- Process climate data into structured models  
- Test the API using pytest  
- Build a CI/CD pipeline with GitHub Actions  
- Deploy to Google Cloud Run  
- Set up an Ubuntu VM with Chrome Remote Desktop on GCP  
- Document your process with screenshots and a written report  

## Prerequisites

- GitHub account  
- Google Cloud Platform account (billing enabled; free tier available)  
- Python basics  
- Terminal/command-line familiarity  
- Basic understanding of REST APIs, CSV data, and JSON  

# Step-by-Step Instructions

# Part 1: Set Up the Climate Dataset and FastAPI Application

## 1. Create Project Directory
```bash
mkdir climate-signals-api && cd climate-signals-api
mkdir tests
touch main.py database.py requirements.txt README.md \
      tests/__init__.py tests/test_api.py
2. Add the Climate Dataset
Create a CSV file named climate_change_dataset.csv with your actual dataset.
Sample structure:

csv
Copy code
country,year,avg_temperature,co2_per_capita,sea_level_rise,rainfall,renewable_energy_percent,forest_area_percent,extreme_weather_events,population
United States,2015,13.2,16.5,3.2,715,12.5,33.9,12,320000000
India,2015,24.5,1.8,2.1,1120,18.3,23.1,28,1290000000
Brazil,2015,25.3,2.1,1.9,1780,42.5,61.9,22,204000000

3. Set Up SQLite Database (database.py)
python
Copy code
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import csv

Base = declarative_base()
engine = create_engine("sqlite:///climate.db")

class ClimateRecord(Base):
    __tablename__ = "climate_records"
    id = Column(Integer, primary_key=True, index=True)
    country = Column(String)
    year = Column(Integer)
    avg_temperature = Column(Float)
    co2_per_capita = Column(Float)
    sea_level_rise = Column(Float)
    rainfall = Column(Float)
    renewable_energy_percent = Column(Float)
    forest_area_percent = Column(Float)
    extreme_weather_events = Column(Integer)
    population = Column(Integer)

Base.metadata.create_all(engine)

def init_db():
    with open("climate_change_dataset.csv", "r") as f:
        csv_reader = csv.DictReader(f)
        with sessionmaker(bind=engine)() as session:
            for row in csv_reader:
                record = ClimateRecord(**row)
                session.add(record)
            session.commit()

def get_db():
    db = sessionmaker(bind=engine)()
    try:
        yield db
    finally:
        db.close()

4. Create FastAPI Application (main.py)
python
Copy code
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from database import ClimateRecord, get_db, init_db

app = FastAPI(title="Climate Signals API")

class ClimateModel(BaseModel):
    country: str
    year: int
    avg_temperature: float
    co2_per_capita: float
    sea_level_rise: float
    rainfall: float
    renewable_energy_percent: float
    forest_area_percent: float
    extreme_weather_events: int
    population: int

@app.on_event("startup")
def startup_event():
    init_db()

@app.get("/records/")
def get_all_records(db: Session = Depends(get_db)):
    return db.query(ClimateRecord).all()

@app.get("/records/{country}")
def get_by_country(country: str, db: Session = Depends(get_db)):
    records = db.query(ClimateRecord).filter(ClimateRecord.country == country).all()
    if not records:
        raise HTTPException(status_code=404, detail="Country not found")
    return records

@app.post("/records/")
def add_record(record: ClimateModel, db: Session = Depends(get_db)):
    db_record = ClimateRecord(**record.dict())
    db.add(db_record)
    db.commit()
    db.refresh(db_record)
    return db_record
5. Requirements File (requirements.txt)
ini
Copy code
fastapi==0.115.0
uvicorn==0.30.6
sqlalchemy==2.0.31
pytest==8.3.2
pytest-httpx==0.30.0
pandas==2.2.2

6. Run the Application Locally
bash
Copy code
pip install -r requirements.txt
uvicorn main:app --reload
Access the API at:

arduino
Copy code
http://127.0.0.1:8000/docs

Part 2: Test the Application with pytest
Create Test File (tests/test_api.py)
python
Copy code
from fastapi.testclient import TestClient
from main import app
import pytest

client = TestClient(app)

def test_get_all_records():
    response = client.get("/records/")
    assert response.status_code == 200
    assert type(response.json()) is list

def test_missing_country():
    response = client.get("/records/UnknownLand")
    assert response.status_code == 404
Run tests:

bash
Copy code
pytest tests/test_api.py -v
Take screenshots of test output.

Part 3: Set Up GitHub Repository and CI/CD
1. Initialize Git Repository
bash
Copy code
git init
git add .
git commit -m "Initial Climate Signals API"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
git push origin main
2. Create Dockerfile
dockerfile
Copy code
FROM python:3.8-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn","main:app","--host","0.0.0.0","--port","8080"]
3. CI/CD Workflow (.github/workflows/ci-cd.yml)
yaml
Copy code
name: CI/CD
on:
  push:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: "3.9"
      - name: Install dependencies
        run: pip install -r requirements.txt
      - name: Run tests
        run: pytest -v

  deploy:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: google-github-actions/setup-gcloud@v1
        with:
          project_id: ${{ secrets.GCP_PROJECT_ID }}
          service_account_key: ${{ secrets.GCP_SA_KEY }}
      - run: gcloud auth configure-docker
      - run: |
          docker build -t gcr.io/${{ secrets.GCP_PROJECT_ID }}/climate-signals-api .
          docker push gcr.io/${{ secrets.GCP_PROJECT_ID }}/climate-signals-api
      - run: |
          gcloud run deploy climate-signals-api \
            --image gcr.io/${{ secrets.GCP_PROJECT_ID }}/climate-signals-api \
            --platform managed \
            --region us-central1 \
            --allow-unauthenticated
