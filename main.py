# main.py
from fastapi import FastAPI, Request
from pydantic import BaseModel

app = FastAPI()

class InverterData(BaseModel):
    timestamp: str
    voltage_1: float
    voltage_2: float
    current_1: float
    current_2: float
    status: int
    error_text: str

@app.post("/data")
async def receive_data(data: InverterData):
    # اینجا می‌تونی ذخیره در دیتابیس، فایل یا پردازش دیگه انجام بدی
    return {"success": True}
