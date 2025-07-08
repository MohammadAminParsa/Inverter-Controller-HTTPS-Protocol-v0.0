# main.py
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

app = FastAPI()

# ساختار داده‌ای که از ESP32 دریافت می‌شود
class InverterData(BaseModel):
    timestamp: str
    voltage_1: float
    voltage_2: float
    current_1: float
    current_2: float
    status: int
    error_text: str

# حافظه موقت برای ذخیره داده‌ها
data_log: List[InverterData] = []

@app.post("/data")
async def receive_data(data: InverterData):
    data_log.append(data)
    return {"success": True}

@app.get("/data")
async def get_all_data():
    return data_log
