# Climate Signals: Climate Change Indicators Analysis & Dashboard
Capstone Project — Planning Phase

---

## 1. Project Overview
Climate Signals is a data-driven project designed to analyze global climate indicators using the dataset `climate_change_dataset.csv`.  
The goal of this project is to examine how climate factors such as temperature, CO₂ emissions, sea-level rise, renewable energy usage, and extreme weather events have changed over time across different countries, and to determine which regions are most vulnerable to climate risk.

This project will produce:
- A FastAPI backend that processes and serves climate data  
- A Streamlit dashboard for interactive climate analytics  
- Forecasting models to project climate trends  
- A vulnerability index to identify high-risk countries  
- Clear insights that highlight relationships between climate factors  

---

## 2. Problem Statement
Climate change is accelerating, but understanding *where* and *why* countries are becoming more vulnerable is difficult without data tools.  
The dataset you provided reveals multiple climate signals—temperature increase, CO₂ emissions, extreme weather, and renewable energy adoption—but the patterns are not immediately clear.

This project solves the problem by:
- Cleaning and standardizing climate data
- Identifying historical trends
- Determining correlations between variables  
- Building a measurable climate vulnerability score  
- Forecasting CO₂ and temperature for the next 5 years  
- Presenting these results through an interactive dashboard  

---

## 3. Project Objectives
This project aims to answer questions directly from the dataset:

### **Primary Questions**
1. Which countries are experiencing the strongest rise in temperature over time?  
3. How does renewable energy usage impact vulnerability?  
4. Are extreme weather events increasing globally?  
5. Which countries face the highest climate risk when combining all indicators?  
6. What will climate conditions look like 1–5 years from now?

### **Deliverables**
- Processed and cleaned dataset  
- Vulnerability index formula + ranking  
- Forecasting models for Temp & CO₂  
- API endpoints for accessing insights  
- Fully interactive Streamlit dashboard  
- Architecture diagrams  
- GitHub repository with full documentation  

---

## 4. Dataset Description
**File:** `climate_change_dataset.csv`  
This dataset contains multi-year climate metrics for multiple countries, including:

- **avg_temperature** – annual average temperature  
- **co2_per_capita** – carbon emissions per person  
- **sea_level_rise** – sea-level change  
- **rainfall** – precipitation levels  
- **renewable_energy_percent** – percent of energy from renewable sources  
- **forest_area_percent** – amount of forest coverage  
- **extreme_weather_events** – number of extreme events  
- **population** – country population

This dataset supports:
- Time-series trend analysis  
- Climate risk scoring  
- Correlation & regression  
- Forecasting  
- Data visualization  

---

## 5. System Architecture
The project uses a full-stack architecture:

### **Backend (FastAPI)**
- Loads and processes the raw CSV  
- Stores cleaned data in SQLite  
- Generates insights (correlations, rankings, summaries)  
- Serves forecast results through API endpoints  
- Sends structured data to Streamlit  

### **Frontend (Streamlit)**
- Visualizes climate trends  
- Displays forecasts  
- Shows country comparisons  
- Renders vulnerability scores  
- Allows users to select and explore indicators  

### **Storage**
- **SQLite** for processed datasets  
- **Google Cloud Storage** for raw CSV + model artifacts  

### **Machine Learning**
- Prophet/ARIMA forecasting for CO₂ + temperature  
- KMeans clustering for “similar countries” analysis  
- Linear regression for influence of features  

---

## 6. Architecture Diagram Description
**Your diagram should include these components:**

**Left Side**  
- Raw CSV dataset  
- Upload → Google Cloud Storage  

**Center**  
- FastAPI ingestion  
- Data cleaning pipeline (Pandas)  
- SQLite processed database  
- Modeling engine  
- Model artifacts storage  

**Right Side**  
- FastAPI insight endpoints  
- Streamlit dashboard  
- User interacting with UI  

**Bottom**  
- GitHub → CI/CD workflow → Deployment

A Mermaid diagram version (for GitHub) will be placed in `/diagrams`.

---

## 7. Project Structure

## 4.1 Create Project Directory
```bash
mkdir climate-signals-api && cd climate-signals-api
mkdir tests
touch main.py database.py requirements.txt README.md tests/__init__.py tests/test_api.py
