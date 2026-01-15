from employee_store import read_employees
from services.drive_service import get_current_month_pdfs, download_pdf
from payroll_store import already_sent, log_sent
from config import current_year_month

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

        # 🔜 burada Drive + Gmail olacak
        print(f"[TEST] Bordro gönderilecek → {emp['email']}")

        log_sent(emp["email"], year, month)
        report["sent"] += 1

    return report

def match_users_to_pdfs():
    year, month = current_year_month()
    users = read_employees()
    pdfs = get_current_month_pdfs()  # {"Arif Sami Erdoğan.pdf": file_id}

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

        pdf_name = f"{user['full_name']}.pdf"
        if pdf_name in pdfs:
            matched.append({
                "user": user,
                "file_id": pdfs[pdf_name]
            })
            report["matched"] += 1
        else:
            report["missing_pdf"].append(user["full_name"])

    return matched, report
