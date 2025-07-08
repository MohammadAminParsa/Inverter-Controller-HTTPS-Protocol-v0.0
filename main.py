from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel
from typing import List

app = FastAPI()

class InverterData(BaseModel):
    timestamp: str
    voltage_1: float
    voltage_2: float
    current_1: float
    current_2: float
    status: int
    error_text: str

data_log: List[InverterData] = []

@app.post("/data")
async def receive_data(data: InverterData):
    data_log.append(data)
    return {"success": True}

# API برای دریافت JSON خام
@app.get("/api/data")
async def get_all_data():
    return data_log

# صفحه HTML برای نمایش و آپدیت خودکار
@app.get("/data", response_class=HTMLResponse)
async def data_page():
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Inverter Data Monitor</title>
        <style>
            body { font-family: monospace; background: #111; color: #0f0; padding: 1rem; }
            pre { background: #222; padding: 1rem; border-radius: 8px; }
        </style>
    </head>
    <body>
        <h2>Real-Time Inverter Data</h2>
        <pre id="output">Loading...</pre>
        <script>
            async function fetchData() {
                try {
                    const res = await fetch('/api/data');
                    const json = await res.json();
                    document.getElementById('output').textContent = JSON.stringify(json, null, 2);
                } catch (e) {
                    document.getElementById('output').textContent = 'Error fetching data';
                }
            }
            fetchData();
            setInterval(fetchData, 1000);  // هر 1 ثانیه یک بار
        </script>
    </body>
    </html>
    """
    return HTMLResponse(content=html)
