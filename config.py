from datetime import datetime
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"

EMPLOYEE_CSV = DATA_DIR / "employees.csv"
PAYROLL_LOG_CSV = DATA_DIR / "payroll_logs.csv"


SHARED_DRIVE_ID = '0ANdqRtOLUFsYUk9PVA'
BORDRO_ROOT_FOLDER_ID = '0ANdqRtOLUFsYUk9PVA'
    
def current_year_month():
    now = datetime.now()
    return now.year, f"{now.month:02d}"