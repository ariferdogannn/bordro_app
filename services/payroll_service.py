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
<<<<<<< HEAD
    text = unicodedata.normalize("NFKD", text)
    text = text.encode("ascii", "ignore").decode("utf-8")
    text = text.lower()
    text = re.sub(r"[^a-z0-9]", "", text)
    return text

=======

    text = unicodedata.normalize("NFKD", text)
    text = text.encode("ascii", "ignore").decode("utf-8")


    text = text.lower()

    text = re.sub(r"[^a-z0-9]", "", text)

    return text


>>>>>>> 9983693a8940350d50fde4df25738f3c2c535b4e
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
        if not user.get("active", True):
            report["inactive"].append(user.get("full_name", "Unknown"))
            continue

<<<<<<< HEAD
        user_key = normalize_text(user.get("full_name", ""))
        found = False

        for pdf_name, pdf_id in pdfs.items():  # dict items kullan
            pdf_key = normalize_text(pdf_name)
=======
        user_key = normalize_text(user["full_name"])
        found = False

        for pdf in pdfs:
            pdf_key = normalize_text(pdf["name"])
>>>>>>> 9983693a8940350d50fde4df25738f3c2c535b4e

            if user_key in pdf_key:
                matched.append({
                    "user": user,
<<<<<<< HEAD
                    "file_name": pdf_name,
                    "file_id": pdf_id
=======
                    "file_id": pdf["id"],
                    "file_name": pdf["name"]
>>>>>>> 9983693a8940350d50fde4df25738f3c2c535b4e
                })
                report["matched"] += 1
                found = True
                break

        if not found:
<<<<<<< HEAD
            report["missing_pdf"].append(user.get("full_name", "Unknown"))
=======
            report["missing_pdf"].append(user["full_name"])
>>>>>>> 9983693a8940350d50fde4df25738f3c2c535b4e

    return matched, report

