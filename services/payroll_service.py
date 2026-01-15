from employee_store import read_employees
from services.drive_service import get_current_month_pdfs, download_pdf
from payroll_store import already_sent, log_sent
from config import current_year_month
import unicodedata
import re

def send_payrolls():
    year, month = current_year_month()
    employees = read_employees()

    report = {
        "total": 0,
        "sent": 0,
        "errors": []
    }

    for emp in employees:
        if not emp["active"]:
            continue

        report["total"] += 1

        if already_sent(emp["email"], year, month):
            continue

        print(f"[TEST] Bordro gönderilecek → {emp['email']}")

        log_sent(emp["email"], year, month)
        report["sent"] += 1

    return report

def normalize_text(text: str) -> str:
    if not text:
        return ""

    text = unicodedata.normalize("NFKD", text)
    text = text.encode("ascii", "ignore").decode("utf-8")


    text = text.lower()

    text = re.sub(r"[^a-z0-9]", "", text)

    return text


def match_users_to_pdfs():
    year, month = current_year_month()
    users = read_employees()
    pdfs = get_current_month_pdfs()  

    matched = []
    report = {
        "total": len(users),
        "matched": 0,
        "missing_pdf": [],
        "inactive": [],
    }

    for user in users:
        if not user["active"]:
            report["inactive"].append(user["full_name"])
            continue

        user_key = normalize_text(user["full_name"])
        found = False

        for pdf in pdfs:
            pdf_key = normalize_text(pdf["name"])

            if user_key in pdf_key:
                matched.append({
                    "user": user,
                    "file_id": pdf["id"],
                    "file_name": pdf["name"]
                })
                report["matched"] += 1
                found = True
                break

        if not found:
            report["missing_pdf"].append(user["full_name"])

    return matched, report
