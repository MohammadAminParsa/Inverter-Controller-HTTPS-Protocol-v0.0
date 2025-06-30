from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_credentials=True,
    allow_methods=["*"], allow_headers=["*"]
)

# متغیرهای سراسری
voltage = "0.000"
status = "ON"
device_id = "esp32-001"
last_data = {}


@app.get("/", response_class=HTMLResponse)
async def home():
    return """
    <html>
      <head>
        <meta charset="UTF-8">
        <title>ESP32 Monitor</title>
        <style>
          body { font-family: sans-serif; padding: 20px; }
          .label { font-weight: bold; }
        </style>
      </head>
      <body>
        <h2>📡 ESP32 Monitoring Dashboard</h2>
        <p><span class="label">Voltage:</span> <span id="voltage">--</span> V</p>
        <p><span class="label">Status:</span> <span id="status">--</span></p>
        <p><span class="label">Device ID:</span> <span id="device_id">--</span></p>
        <p><span class="label">Timestamp:</span> <span id="timestamp">--</span></p>

        <script>
          async function fetchData() {
            try {
              const res = await fetch("/data");
              const data = await res.json();
              document.getElementById("voltage").innerText = data.voltage;
              document.getElementById("status").innerText = data.status;
              document.getElementById("device_id").innerText = data.device_id;
              document.getElementById("timestamp").innerText = new Date(data.timestamp).toLocaleString();
            } catch (e) {
              console.error("Fetch error:", e);
            }
          }

          // هر ثانیه یک بار داده جدید بگیر
          setInterval(fetchData, 1000);
          fetchData();  // بار اول فوری اجرا کن
        </script>
      </body>
    </html>
    """

@app.post("/data")
async def receive_data(req: Request):
    json = await req.json()
    print("📥 Received:", json)

    # ذخیره داده‌ی آخر
    global last_data
    last_data = {
        "device_id": json.get("device_id", "unknown"),
        "voltage": json.get("voltage", "0.000"),
        "status": json.get("status", "UNKNOWN"),
        "timestamp": json.get("timestamp", datetime.utcnow().isoformat())
    }

    return {
        "message": "Data received",
        **last_data
    }

@app.get("/data")
def get_data():
    return last_data

@app.post("/status")
async def update_status(req: Request):
    body = await req.json()
    global status
    s = body.get("status", "").upper()
    if s in ["ON", "OFF"]:
        status = s
        return {"message": f"Status set to {status}"}
    
    return JSONResponse(status_code=400, content={"error": "Invalid status"})

