from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import mysql.connector
from datetime import datetime, date
import os

app = FastAPI()

# ---------- Pydantic Model ----------
class FarmLogEntry(BaseModel):
    entry_date: date
    entry_time: datetime
    crop_name: str
    activity: str
    labour_working_per_plant: int
    canteen: str
    max_temp: float
    min_temp: float
    rainfall_mm: float
    cumulative_rainfall_mm: float
    max_humidity: float
    min_humidity: float
    irrigation_volume: float
    fertigation_volume: float
    total_fertilizer_used: float
    Major_pest_observation: str
    pest_control_measure: str
    pestiside_name: str
    dose_per_litre: float
    total_volume_used: float
    Status_of_condition: str
    fuel_used_in_tractor1_big: float
    fuel_used_in_tractor2_small: float
    grass_cutter: float
    Auger_sprayer: float
    Company_Bike: float
    miscellaneous: str
    Total_petrol_used: float
    Total_disel_used: float

# ---------- DB Connection ----------
def get_connection():
    return mysql.connector.connect(
        host=os.environ["DB_HOST"],
        user=os.environ["DB_USER"],
        password=os.environ["DB_PASSWORD"],
        database=os.environ["DB_NAME"]
    )

@app.post("/submit-entry")
def submit_entry(entry: FarmLogEntry):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        query = """
INSERT INTO daily_farm_log (
    entry_date, entry_time, crop_name, activity, labour_working_per_plant, canteen,
    max_temp, min_temp, rainfall_mm, cumulative_rainfall_mm, max_humidity, min_humidity,
    irrigation_volume, fertigation_volume, total_fertilizer_used,
    Major_pest_observation, pest_control_measure, pestiside_name, dose_per_litre,
    total_volume_used, Status_of_condition,
    fuel_used_in_tractor1_big, fuel_used_in_tractor2_small, grass_cutter,
    Auger_sprayer, Company_Bike, miscellaneous,
    Total_petrol_used, Total_disel_used
) VALUES (
    %s, %s, %s, %s, %s, %s,
    %s, %s, %s, %s, %s, %s,
    %s, %s, %s, %s, %s, %s,
    %s, %s, %s, %s, %s, %s,
    %s, %s, %s, %s, %s, %s
)
"""
        data = tuple(entry.dict().values())

        cursor.execute(query, data)
        conn.commit()
        return {"message": "Entry successfully saved!"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        if 'cursor' in locals(): cursor.close()
        if 'conn' in locals(): conn.close()


@app.get("/")
def root():
    return {"status": "FastAPI is live"}

@app.get("/healthcheck")
def healthcheck():
    return {"status": "ok"}


