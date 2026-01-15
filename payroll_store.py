import csv
from datetime import datetime
from config import PAYROLL_LOG_CSV

FIELDS = ["email", "year", "month", "sent_at"]

def already_sent(email, year, month):
    with open(PAYROLL_LOG_CSV, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if (
                row["email"] == email
                and int(row["year"]) == year
                and int(row["month"]) == month
            ):
                return True
    return False

def log_sent(email, year, month):
    with open(PAYROLL_LOG_CSV, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        writer.writerow({
            "email": email,
            "year": year,
            "month": month,
            "sent_at": datetime.now().isoformat()
        })
