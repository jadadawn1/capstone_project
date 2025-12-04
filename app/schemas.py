"""
Pydantic schemas for request/response validation
"""
from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class ClimateRecordSchema(BaseModel):
    id: int
    country: str
    year: Optional[int] = None
    avg_temperature: Optional[float] = None
    co2_per_capita: Optional[float] = None
    rainfall: Optional[float] = None
    sea_level_rise: Optional[float] = None
    renewable_energy_percent: Optional[float] = None
    forest_area_percent: Optional[float] = None
    extreme_weather_events: Optional[int] = None
    population: Optional[int] = None
    created_at: datetime

    class Config:
        from_attributes = True


class ClimateRecordCreateSchema(BaseModel):
    country: str
    year: Optional[int] = None
    avg_temperature: Optional[float] = None
    co2_per_capita: Optional[float] = None
    rainfall: Optional[float] = None
    sea_level_rise: Optional[float] = None
    renewable_energy_percent: Optional[float] = None
    forest_area_percent: Optional[float] = None
    extreme_weather_events: Optional[int] = None
    population: Optional[int] = None


class ClimateStatisticsSchema(BaseModel):
    country: str
    record_count: int
    avg_temperature_mean: Optional[float] = None
    co2_per_capita_mean: Optional[float] = None
    co2_per_capita_max: Optional[float] = None
    rainfall_mean: Optional[float] = None
    sea_level_rise_total: Optional[float] = None
    renewable_energy_mean: Optional[float] = None
