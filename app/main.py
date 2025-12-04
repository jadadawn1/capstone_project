"""
FastAPI Climate Signals Backend API
"""
from fastapi import FastAPI, Depends, HTTPException, Path, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
from datetime import datetime

from app.database import get_db, init_db, ClimateRecord
from app.schemas import ClimateRecordSchema, ClimateStatisticsSchema

# Initialize FastAPI app
app = FastAPI(
    title="Climate Signals API",
    description="Backend API for Climate Change Indicators Analysis",
    version="1.0.0"
)

# Initialize database on startup
@app.on_event("startup")
def startup_event():
    init_db()


@app.get("/")
def root():
    return {
        "message": "Climate Signals API",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "Climate Signals API",
        "timestamp": datetime.utcnow().isoformat()
    }


@app.get("/api/records", response_model=List[ClimateRecordSchema])
def get_records(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    """Get all climate records with pagination"""
    records = db.query(ClimateRecord).offset(skip).limit(limit).all()
    return records


@app.get("/api/records/{record_id}", response_model=ClimateRecordSchema)
def get_record(record_id: int = Path(..., gt=0), db: Session = Depends(get_db)):
    """Get a specific climate record by ID"""
    record = db.query(ClimateRecord).filter(ClimateRecord.id == record_id).first()
    if not record:
        raise HTTPException(status_code=404, detail=f"Record {record_id} not found")
    return record


@app.get("/api/records/country/{country}", response_model=List[ClimateRecordSchema])
def get_records_by_country(country: str, db: Session = Depends(get_db)):
    """Get all records for a specific country"""
    records = db.query(ClimateRecord).filter(ClimateRecord.country == country).all()
    if not records:
        raise HTTPException(status_code=404, detail=f"No records found for country: {country}")
    return records


@app.get("/api/records/year/{year}", response_model=List[ClimateRecordSchema])
def get_records_by_year(year: int = Path(..., ge=1900, le=2100), db: Session = Depends(get_db)):
    """Get all records for a specific year"""
    records = db.query(ClimateRecord).filter(ClimateRecord.year == year).all()
    if not records:
        raise HTTPException(status_code=404, detail=f"No records found for year: {year}")
    return records


@app.get("/api/records/country/{country}/year/{year}", response_model=List[ClimateRecordSchema])
def get_records_by_country_and_year(
    country: str,
    year: int = Path(..., ge=1900, le=2100),
    db: Session = Depends(get_db)
):
    """Get records for a specific country and year"""
    records = db.query(ClimateRecord).filter(
        ClimateRecord.country == country,
        ClimateRecord.year == year
    ).all()
    if not records:
        raise HTTPException(
            status_code=404,
            detail=f"No records found for {country} in {year}"
        )
    return records


@app.get("/api/statistics/country/{country}", response_model=ClimateStatisticsSchema)
def get_country_statistics(country: str, db: Session = Depends(get_db)):
    """Get statistical summary for a specific country"""
    records = db.query(ClimateRecord).filter(ClimateRecord.country == country).all()
    if not records:
        raise HTTPException(status_code=404, detail=f"No records found for country: {country}")
    
    stats = db.query(
        ClimateRecord.country,
        func.count(ClimateRecord.id).label("record_count"),
        func.avg(ClimateRecord.avg_temperature).label("avg_temperature_mean"),
        func.avg(ClimateRecord.co2_per_capita).label("co2_per_capita_mean"),
        func.max(ClimateRecord.co2_per_capita).label("co2_per_capita_max"),
        func.avg(ClimateRecord.rainfall).label("rainfall_mean"),
        func.sum(ClimateRecord.sea_level_rise).label("sea_level_rise_total"),
        func.avg(ClimateRecord.renewable_energy_percent).label("renewable_energy_mean")
    ).filter(ClimateRecord.country == country).group_by(ClimateRecord.country).first()
    
    return stats


@app.get("/api/statistics/year/{year}", response_model=List[ClimateStatisticsSchema])
def get_year_statistics(year: int = Path(..., ge=1900, le=2100), db: Session = Depends(get_db)):
    """Get statistical summaries for all countries in a specific year"""
    records = db.query(ClimateRecord).filter(ClimateRecord.year == year).all()
    if not records:
        raise HTTPException(status_code=404, detail=f"No records found for year: {year}")
    
    stats = db.query(
        ClimateRecord.country,
        func.count(ClimateRecord.id).label("record_count"),
        func.avg(ClimateRecord.avg_temperature).label("avg_temperature_mean"),
        func.avg(ClimateRecord.co2_per_capita).label("co2_per_capita_mean"),
        func.max(ClimateRecord.co2_per_capita).label("co2_per_capita_max"),
        func.avg(ClimateRecord.rainfall).label("rainfall_mean"),
        func.sum(ClimateRecord.sea_level_rise).label("sea_level_rise_total"),
        func.avg(ClimateRecord.renewable_energy_percent).label("renewable_energy_mean")
    ).filter(ClimateRecord.year == year).group_by(ClimateRecord.country).all()
    
    return stats
