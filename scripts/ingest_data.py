"""
Data ingestion script for Climate Signals Platform
Loads CSV data into SQLite database with header mapping
"""
import sqlite3
import csv
import os
from datetime import datetime

# Paths
DB_PATH = "data/climate_data.db"
CSV_PATH = "climate_change_dataset.csv"

# Create database directory if it doesn't exist
os.makedirs("data", exist_ok=True)

# Connect to database
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Create table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS climate_records (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        country TEXT NOT NULL,
        year INTEGER,
        avg_temperature REAL,
        co2_per_capita REAL,
        rainfall REAL,
        sea_level_rise REAL,
        renewable_energy_percent REAL,
        forest_area_percent REAL,
        extreme_weather_events INTEGER,
        population INTEGER,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP
    )
""")

print(f"Loading data from {CSV_PATH}...")

# Read CSV and detect headers
with open(CSV_PATH, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    headers = reader.fieldnames
    print(f"CSV Headers: {headers}")
    
    # Create mapping from CSV headers to DB columns
    header_map = {}
    for h in headers:
        h_lower = h.lower().strip()
        if 'country' in h_lower:
            header_map[h] = 'country'
        elif 'year' in h_lower:
            header_map[h] = 'year'
        elif 'temp' in h_lower or 'temperature' in h_lower:
            header_map[h] = 'avg_temperature'
        elif 'co2' in h_lower or 'emission' in h_lower:
            header_map[h] = 'co2_per_capita'
        elif 'rain' in h_lower or 'precipitation' in h_lower:
            header_map[h] = 'rainfall'
        elif 'sea' in h_lower or 'level' in h_lower:
            header_map[h] = 'sea_level_rise'
        elif 'renewable' in h_lower or 'energy' in h_lower:
            header_map[h] = 'renewable_energy_percent'
        elif 'forest' in h_lower:
            header_map[h] = 'forest_area_percent'
        elif 'weather' in h_lower or 'extreme' in h_lower or 'event' in h_lower:
            header_map[h] = 'extreme_weather_events'
        elif 'population' in h_lower:
            header_map[h] = 'population'
    
    print(f"\nHeader Mapping:")
    for csv_h, db_col in header_map.items():
        print(f"  {csv_h} => {db_col}")
    
    # Reset file pointer
    f.seek(0)
    reader = csv.DictReader(f)
    
    # Insert data
    count = 0
    for row in reader:
        # Map CSV row to database columns
        db_row = {
            'country': row.get(next((k for k, v in header_map.items() if v == 'country'), None), ''),
            'year': row.get(next((k for k, v in header_map.items() if v == 'year'), None)),
            'avg_temperature': row.get(next((k for k, v in header_map.items() if v == 'avg_temperature'), None)),
            'co2_per_capita': row.get(next((k for k, v in header_map.items() if v == 'co2_per_capita'), None)),
            'rainfall': row.get(next((k for k, v in header_map.items() if v == 'rainfall'), None)),
            'sea_level_rise': row.get(next((k for k, v in header_map.items() if v == 'sea_level_rise'), None)),
            'renewable_energy_percent': row.get(next((k for k, v in header_map.items() if v == 'renewable_energy_percent'), None)),
            'forest_area_percent': row.get(next((k for k, v in header_map.items() if v == 'forest_area_percent'), None)),
            'extreme_weather_events': row.get(next((k for k, v in header_map.items() if v == 'extreme_weather_events'), None)),
            'population': row.get(next((k for k, v in header_map.items() if v == 'population'), None)),
        }
        
        # Convert empty strings to None
        for key in db_row:
            if db_row[key] == '' or db_row[key] is None:
                db_row[key] = None
        
        cursor.execute("""
            INSERT INTO climate_records 
            (country, year, avg_temperature, co2_per_capita, rainfall, sea_level_rise, 
             renewable_energy_percent, forest_area_percent, extreme_weather_events, population, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            db_row['country'],
            db_row['year'],
            db_row['avg_temperature'],
            db_row['co2_per_capita'],
            db_row['rainfall'],
            db_row['sea_level_rise'],
            db_row['renewable_energy_percent'],
            db_row['forest_area_percent'],
            db_row['extreme_weather_events'],
            db_row['population'],
            datetime.utcnow().isoformat()
        ))
        count += 1

conn.commit()

# Verify
cursor.execute("SELECT COUNT(*) FROM climate_records")
total = cursor.fetchone()[0]
print(f"\n✓ Successfully ingested {count} rows")
print(f"✓ Total records in database: {total}")

# Show sample
cursor.execute("SELECT * FROM climate_records LIMIT 3")
print(f"\nSample records:")
for row in cursor.fetchall():
    print(f"  {row}")

conn.close()
print(f"\n✓ Database ready at {DB_PATH}")
