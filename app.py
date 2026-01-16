from flask import Flask, render_template, request, redirect, url_for, flash
from send_payroll import send_payroll_mails


app = Flask(__name__)
app.secret_key = "bordro-secret"


@app.route("/")
def dashboard():
    return render_template(
        "dashboard.html",
        version="v1.0.3"
    )


@app.route("/send", methods=["POST"])
def send():
    report = send_payroll_mails()

    return {
        "total": report.get("total", 0),
        "sent": report.get("sent", 0),
        "missing": len(report.get("missing_pdf", []))
    }


if __name__ == "__main__":
     app.run(host="0.0.0.0", port=5000, debug=False)
