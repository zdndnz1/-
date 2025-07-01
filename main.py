
from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime, timedelta

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", response_class=HTMLResponse)
def form_page():
    return """
    <h2>API พร้อมทำงาน</h2>
    <form method="post" action="/calculate">
      Start Date: <input name="start_date" value="2025-06-25"><br>
      Cycle Length: <input name="cycle_length" value="28"><br>
      Period Length: <input name="period_length" value="5"><br>
      Notify Before (days): <input name="notify_days" value="2"><br>
      <button type="submit">คำนวณ</button>
    </form>
    """

@app.post("/calculate")
def calculate(
    start_date: str = Form(...),
    cycle_length: int = Form(...),
    period_length: int = Form(...),
    notify_days: int = Form(...)
):
    start = datetime.strptime(start_date, "%Y-%m-%d")
    ovulation = start + timedelta(days=cycle_length - 14)
    next_period = start + timedelta(days=cycle_length)
    period_end = start + timedelta(days=period_length)
    notify_date = ovulation - timedelta(days=notify_days)
    return {
        "ovulation_date": ovulation.date(),
        "period_end": period_end.date(),
        "next_period": next_period.date(),
        "notify_before": notify_date.date()
    }
