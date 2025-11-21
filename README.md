# Climate Signals API & Cloud Deployment

## 1. Overview
In this mini-lab, you will build a FastAPI application to manage and analyze a global climate dataset, test it using pytest, set up a CI/CD pipeline using GitHub Actions, and deploy the application to Google Cloud Run. You will also create an Ubuntu VM with Chrome Remote Desktop on Google Cloud Platform (GCP) to replicate the development and deployment process.

The dataset contains climate indicators such as temperature, CO₂ emissions, sea-level rise, rainfall, renewable energy usage, forest area, extreme weather events, and population.  
Your FastAPI backend will retrieve, insert, and process climate records and support future integration with a Streamlit dashboard.

---

## 2. Learning Objectives
By completing this project, you will:

- Build a REST API using FastAPI and SQLite  
- Parse a dataset and initialize a database  
- Test API endpoints using pytest  
- Implement CI/CD via GitHub Actions  
- Containerize the project using Docker  
- Deploy an API to Google Cloud Run  
- Create an Ubuntu VM on GCP with Chrome Remote Desktop  
- Document each step with screenshots and a report  

---

## 3. Prerequisites
- GitHub account  
- Google Cloud Platform account (billing enabled)  
- Python 3.8+  
- Basic terminal command skills  
- Docker installed  

---

# 4. Part 1 — Set Up Climate Dataset and FastAPI Application

## 4.1 Create Project Directory
```bash
mkdir climate-signals-api && cd climate-signals-api
mkdir tests
touch main.py database.py requirements.txt README.md tests/__init__.py tests/test_api.py
---
## 4.2 Create Dataset File
```bash
country,year,avg_temperature,co2_per_capita,sea_level_rise,rainfall,renewable_energy_percent,forest_area_percent,extreme_weather_events,population
United States,2015,13.2,16.5,3.2,715,12.5,33.9,12,320000000
India,2015,24.5,1.8,2.1,1120,18.3,23.1,28,1290000000
Brazil,2015,25.3,2.1,1.9,1780,42.5,61.9,22,204000000
