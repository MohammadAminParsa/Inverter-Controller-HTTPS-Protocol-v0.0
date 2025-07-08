from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

class InverterData(BaseModel):
    timestamp: str
    voltage_1: float
    voltage_2: float
    current_1: float
    current_2: float
    status: int
    error_text: str

# فقط آخرین داده ذخیره می‌شود
last_data: Optional[InverterData] = None

@app.post("/data")
async def receive_data(data: InverterData):
    global last_data
    last_data = data
    return {"success": True}

# API برای دریافت فقط آخرین داده
@app.get("/api/data")
async def get_latest_data():
    return last_data if last_data else {"message": "No data yet"}

# صفحه HTML برای نمایش آخرین داده و آپدیت خودکار
@app.get("/data", response_class=HTMLResponse)
async def data_page():
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Inverter Monitor</title>
        <style>
            body { font-family: monospace; background: #111; color: #0f0; padding: 1rem; }
            pre { background: #222; padding: 1rem; border-radius: 8px; }
        </style>
    </head>
    <body>
        <h2>Real-Time Inverter Data</h2>
        <pre id="output">Waiting for data...</pre>
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
            setInterval(fetchData, 1000);
        </script>
    </body>
    </html>
    """
    return HTMLResponse(content=html)
