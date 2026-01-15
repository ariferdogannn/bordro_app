from fastapi import FastAPI
from employee_store import read_employees, add_employee
from payroll_service import send_payrolls

app = FastAPI(title="Bordro Otomasyon API (CSV)")

@app.get("/")
def root():
    return {"status": "CSV tabanlı Bordro API çalışıyor"}

@app.get("/employees")
def list_employees():
    return read_employees()

@app.post("/employees")
def create_employee(email: str, full_name: str):
    add_employee(email, full_name)
    return {"status": "Çalışan eklendi"}

@app.post("/send-payrolls")
def trigger_payrolls():
    report = send_payrolls()
    return report
