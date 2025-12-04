# Climate Signals Insight Platform

A comprehensive full-stack climate data analytics platform featuring FastAPI backend, SQLite database, and interactive Streamlit dashboard for analyzing global climate indicators.

## 📋 Project Overview

Climate Signals is a data-driven application that analyzes global climate indicators including temperature, CO₂ emissions, sea level rise, renewable energy adoption, forest coverage, and extreme weather events across 15 countries from 2000-2023.

### Key Features

- **10 Interactive Dashboard Pages** for comprehensive climate analysis
- **RESTful API** with 8+ endpoints for programmatic data access
- **Time-series forecasting** using Prophet for temperature and CO₂ predictions
- **Correlation analysis** with interactive heatmaps and scatter plots
- **Climate risk scoring** combining multiple vulnerability indicators
- **Performance rankings** showing top/bottom countries across metrics
- **Real-time data visualization** with Plotly interactive charts

---

## 🗂️ Project Structure

```
capstone/
├── app/
│   ├── __init__.py
│   ├── database.py          # SQLAlchemy models and database configuration
│   ├── main.py              # FastAPI application with API endpoints
│   └── schemas.py           # Pydantic validation models
├── dashboard/
│   └── app.py               # Streamlit multi-page dashboard
├── data/
│   └── climate_data.db      # SQLite database (created after ingestion)
├── scripts/
│   └── ingest_data.py       # CSV to database ingestion script
├── climate_change_dataset.csv  # Raw climate data (1000 records)
└── README.md
```

---

## 🚀 Quick Start

### Prerequisites

- Python 3.13 or higher
- pip package manager

### Installation

1. **Clone the repository:**
```bash
git clone https://github.com/jadadawn1/capstone_project.git
cd capstone
```

2. **Install dependencies:**
```bash
pip install uvicorn fastapi sqlalchemy pydantic streamlit pandas plotly requests scikit-learn prophet seaborn numpy
```

### Database Setup

3. **Ingest climate data into SQLite:**
```bash
python scripts/ingest_data.py
```
This creates `data/climate_data.db` and loads 1000 climate records.

### Running the Application

4. **Start FastAPI backend (Terminal 1):**
```bash
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

5. **Start Streamlit dashboard (Terminal 2):**
```bash
python -m streamlit run dashboard/app.py --server.port 8501 --server.headless true
```

6. **Access the application:**
   - **Dashboard:** http://localhost:8501
   - **API Documentation:** http://localhost:8000/docs
   - **API Health Check:** http://localhost:8000/health

---

## 📊 Dashboard Pages

### 1. **Overview**
- Platform statistics (1000 records, 15 countries, 24 years)
- Feature summary and navigation guide

### 2. **Country Analysis**
- Select country to view detailed metrics
- Temperature trend line chart with change indicators
- CO₂ emissions bar chart with color gradients
- Summary statistics and trends

### 3. **Time Series**
- Multi-indicator time series visualization
- Available indicators: Temperature, CO₂, Rainfall, Sea Level, Renewable Energy
- Min/max/average statistics

### 4. **Comparisons**
- Side-by-side comparison of two countries
- Metric cards for all indicators
- Grouped bar charts with dual-color coding

### 5. **Statistics**
- Year-based statistical summaries
- Country-level aggregations (mean, count)
- Temperature and CO₂ bar charts

### 6. **Climate Risk Dashboard**
- Temperature rise rankings
- Sea level rise tracking
- Extreme weather event monitoring
- CO₂ emission leaders
- Composite risk score (0-100) combining all factors

### 7. **Top Performers**
- **4 Tabs:** Renewable Energy, Forest Conservation, CO₂ Emissions, Overall Performance
- Top 10 leaders vs bottom 10 laggards
- Forest area change over time
- Composite performance scoring

### 8. **Key Insights**
- Global climate snapshot with 24-year changes
- Historical trend visualizations
- Auto-generated key findings
- Areas of concern with warnings

### 9. **Correlation Analysis**
- Interactive correlation heatmap (8 indicators)
- Strongest positive/negative correlations
- Scatter plot explorer with trendlines
- Correlation trends over time

### 10. **Forecasting**
- Prophet-based time series forecasting
- 1-5 year predictions for Temperature, CO₂, Sea Level, Renewable Energy
- Confidence intervals and uncertainty metrics
- Multi-country forecast comparison

---

## 🔌 API Endpoints

### Health & Root
- `GET /` - Root endpoint
- `GET /health` - Health check

### Records
- `GET /api/records` - Get all records (paginated, limit parameter)
- `GET /api/records/{record_id}` - Get record by ID
- `GET /api/records/country/{country}` - Get records by country
- `GET /api/records/year/{year}` - Get records by year
- `GET /api/records/country/{country}/year/{year}` - Get records by country and year

### Statistics
- `GET /api/statistics/country/{country}` - Country-level statistics
- `GET /api/statistics/year/{year}` - Year-level statistics

**Example:**
```bash
curl http://localhost:8000/api/records/country/USA
```

---

## 📦 Dependencies

### Core Framework
- **FastAPI** - Modern web framework for building APIs
- **Uvicorn** - ASGI server for FastAPI
- **Streamlit** - Interactive dashboard framework

### Database & ORM
- **SQLAlchemy** - SQL toolkit and ORM
- **Pydantic** - Data validation using Python type hints

### Data Processing & Visualization
- **Pandas** - Data manipulation and analysis
- **NumPy** - Numerical computing
- **Plotly** - Interactive charts and graphs

### Machine Learning
- **Prophet** - Time-series forecasting by Meta
- **scikit-learn** - Machine learning utilities (MinMaxScaler)
- **Seaborn** - Statistical data visualization

### HTTP Client
- **Requests** - HTTP library for API calls

---

## 📈 Data Overview

**Dataset:** `climate_change_dataset.csv`

**Records:** 1000 climate data points  
**Countries:** 15 (Argentina, Australia, Brazil, Canada, China, France, Germany, India, Indonesia, Japan, Mexico, Russia, South Africa, UK, USA)  
**Years:** 2000-2023 (24 years)

**Indicators:**
- `avg_temperature` - Average annual temperature (°C)
- `co2_per_capita` - CO₂ emissions per capita (metric tons)
- `rainfall` - Annual precipitation (mm)
- `sea_level_rise` - Sea level change (mm)
- `renewable_energy_percent` - Renewable energy share (%)
- `forest_area_percent` - Forest coverage (%)
- `extreme_weather_events` - Number of extreme weather events
- `population` - Country population

---

## 🧪 Development

### Run in Development Mode

FastAPI auto-reloads on code changes with `--reload` flag:
```bash
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

### Re-ingest Data

To refresh the database:
```bash
python scripts/ingest_data.py
```

### View API Documentation

Interactive API docs with Swagger UI:
```
http://localhost:8000/docs
```

---

## 🔍 Key Analyses

### Climate Risk Score
Composite metric combining:
- Temperature change (30% weight)
- Sea level rise (25% weight)
- Extreme weather events (25% weight)
- CO₂ emissions (20% weight)

### Performance Score
Overall climate action metric:
- Renewable energy adoption (+30%)
- Forest area preservation (+30%)
- CO₂ emissions reduction (-25%)
- Extreme weather resilience (-15%)

### Forecasting
- **Model:** Facebook Prophet with custom parameters
- **Predictions:** 1-5 years ahead
- **Confidence:** Upper/lower bounds with uncertainty metrics
- **Supported indicators:** Temperature, CO₂, Sea Level, Renewable Energy

---

## 🛠️ Troubleshooting

### Port Already in Use
```bash
# Kill process on port 8000
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Kill process on port 8501
netstat -ano | findstr :8501
taskkill /PID <PID> /F
```

### Services Not Responding
Check both services are running:
```python
import requests
print(requests.get('http://localhost:8000/health').status_code)  # Should be 200
print(requests.get('http://localhost:8501').status_code)          # Should be 200
```

### Database Errors
Re-create the database:
```bash
# Delete old database
rm data/climate_data.db

# Re-ingest data
python scripts/ingest_data.py
```

---

## 📝 License

All Rights Reserved © 2025

---

## 👤 Author

**Jada Dawn**  
Repository: [capstone_project](https://github.com/jadadawn1/capstone_project)

---

## 🙏 Acknowledgments

- Climate data sourced from `climate_change_dataset.csv`
- Built with FastAPI, Streamlit, and Prophet
- Visualization powered by Plotly

---

## 📞 Support

For issues or questions:
1. Check the [API Documentation](http://localhost:8000/docs)
2. Review this README
3. Open an issue on GitHub

---

**Last Updated:** December 4, 2025
