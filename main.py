from fastapi import FastAPI, Request, Query
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime

app = FastAPI()

# برای ذخیره ولتاژ و وضعیت
voltage = "0.000"
status = "ON"

# CORS برای ارتباط از ESP32 و مرورگر
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_credentials=True,
    allow_methods=["*"], allow_headers=["*"]
)

@app.get("/", response_class=HTMLResponse)
async def home():
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>ESP32 Monitor</title>
        <meta http-equiv="refresh" content="1"> <!-- هر 1 ثانیه رفرش -->
        <style>
            body {{ font-family: sans-serif; margin: 2rem; }}
            .value {{ font-size: 2rem; font-weight: bold; }}
            .status {{ font-size: 1.5rem; color: green; }}
            button {{ padding: 10px 20px; font-size: 16px; margin-right: 10px; }}
        </style>
    </head>
    <body>
        <h2>ESP32 Monitoring</h2>
        <p>🔋 Voltage: <span class="value">{voltage}</span> V</p>
        <p>📟 Status: <span class="status">{status}</span></p>
        <form action="/status" method="post">
            <input type="hidden" name="status" value="ON">
            <button type="submit">🔛 Turn ON</button>
        </form>
        <form action="/status" method="post">
            <input type="hidden" name="status" value="OFF">
            <button type="submit">⛔ Turn OFF</button>
        </form>
    </body>
    </html>
    """
    return HTMLResponse(content=html)

@app.get("/data")
def get_data():
    return {
        "device_id": "esp32-001",
        "timestamp": datetime.utcnow().isoformat(),
        "data": {
            "voltage": voltage,
            "status": status
        }
    }

@app.post("/data")
def post_data(v: str = Query(...)):
    global voltage
    voltage = v.strip()
    print(f"📥 Received voltage: {voltage}")
    return {"message": "Voltage updated", "voltage": voltage}

@app.get("/status")
def get_status():
    return {"status": status}

@app.post("/status")
async def post_status(request: Request):
    global status
    form = await request.form()
    s = form.get("status", "").upper()
    if s in ["ON", "OFF"]:
        status = s
        print(f"📥 Status set to: {status}")
        return HTMLResponse(content=f"<script>location.href='/'</script>")
    return JSONResponse(status_code=400, content={"error": "Invalid status"})
