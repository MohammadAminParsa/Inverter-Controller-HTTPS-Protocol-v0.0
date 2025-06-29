from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
import json

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_credentials=True,
    allow_methods=["*"], allow_headers=["*"]
)

voltage = "0.000"
status = "ON"
device_id = "esp32-001"

@app.post("/data")
async def receive_data(req: Request):
    body = await req.json()
    global voltage, status, device_id
    device_id = body.get("device_id", "unknown")
    voltage = body.get("voltage", "0.000")
    status = body.get("status", status)
    print(f"📥 Received: {body}")
    return {
        "message": "Data received",
        "voltage": voltage,
        "status": status,
        "device_id": device_id,
        "timestamp": datetime.utcnow().isoformat()
    }

@app.get("/data")
def get_data():
    return {
        "device_id": device_id,
        "voltage": voltage,
        "status": status,
        "timestamp": datetime.utcnow().isoformat()
    }

@app.post("/status")
async def update_status(req: Request):
    body = await req.json()
    global status
    s = body.get("status", "").upper()
    if s in ["ON", "OFF"]:
        status = s
        return {"message": f"Status set to {status}"}
    return JSONResponse(status_code=400, content={"error": "Invalid status"})

@app.get("/status")
def get_status():
    return {"status": status}
