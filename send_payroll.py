from services.payroll_service import match_users_to_pdfs
from services.drive_service import download_pdf
from services.gmail_service import send_email

ADMIN_EMAIL = "arif@bataryasan.com"

def send_payroll_mails():
    matched, report = match_users_to_pdfs()

    # Kullanıcılara PDF gönder
    for item in matched:
        user = item["user"]
        pdf_id = item["file_id"]
        pdf_bytes = download_pdf(pdf_id)

        subject = f"{user['full_name']} - Bordro"
        body = f"""
        <p>Merhaba {user['full_name']},</p>
        <p>Bu aya ait bordronuz ekte yer almaktadır.</p>
        <p>İyi çalışmalar.</p>
        """

        send_email(
            to=user["email"],
            subject=subject,
            body=body,
            attachments=[(f"{user['full_name']}.pdf", pdf_bytes)]
        )

    # Admin raporu
    report_body = f"""
    <p>Toplam kullanıcı: {report['total']}</p>
    <p>Eşleşen PDF sayısı: {report['matched']}</p>
    <p>Eksik PDF: {', '.join(report['missing_pdf'])}</p>
    <p>Aktif olmayanlar: {', '.join(report['inactive'])}</p>
    """
    send_email(
        to=ADMIN_EMAIL,
        subject="Bordro Gönderim Raporu",
        body=report_body
    )

if __name__ == "__main__":
    send_payroll_mails()
