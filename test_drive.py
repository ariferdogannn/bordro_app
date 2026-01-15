from drive_service import get_current_month_pdfs

pdfs = get_current_month_pdfs()

print("Aktif ay PDF’leri:")
for name in pdfs:
    print("-", name)
