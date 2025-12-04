"""
Database configuration and models for Climate Signals Platform
"""
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

DATABASE_URL = "sqlite:///./data/climate_data.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class ClimateRecord(Base):
    __tablename__ = "climate_records"
    
    id = Column(Integer, primary_key=True, index=True)
    country = Column(String, nullable=False, index=True)
    year = Column(Integer, index=True)
    avg_temperature = Column(Float)
    co2_per_capita = Column(Float)
    rainfall = Column(Float)
    sea_level_rise = Column(Float)
    renewable_energy_percent = Column(Float)
    forest_area_percent = Column(Float)
    extreme_weather_events = Column(Integer)
    population = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)


def init_db():
    Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
