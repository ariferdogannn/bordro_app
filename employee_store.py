import csv
from config import EMPLOYEE_CSV
from pathlib import Path

FIELDNAMES = ["email", "full_name", "active"]

EMPLOYEE_CSV = Path(__file__).parent / "data" / "employees.csv"

def read_employees():
    employees = []
    with open(EMPLOYEE_CSV, newline="", encoding="utf-8-sig") as f:  # UTF-8-SIG BOM temizler
        reader = csv.DictReader(f)
        for row in reader:
            row = {k.strip(): v.strip() for k, v in row.items()}  # başlık ve değerleri temizle
            row["active"] = row["active"] == "1"
            employees.append(row)
    return employees

def add_employee(email, full_name, active=True):
    employees = read_employees()
    if any(e["email"] == email for e in employees):
        raise ValueError("Bu email zaten var")

    with open(EMPLOYEE_CSV, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        writer.writerow({
            "email": email,
            "full_name": full_name,
            "active": "1" if active else "0"
        })
