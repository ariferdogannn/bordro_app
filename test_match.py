from payroll_service import match_users_to_pdfs

matched, report = match_users_to_pdfs()

print("Rapor:")
print("Toplam kullanıcı:", report["total"])
print("Eşleşen PDF sayısı:", report["matched"])
print("Eksik PDF:", report["missing_pdf"])
print("Aktif olmayanlar:", report["inactive"])

print("\nEşleşmeler:")
for m in matched:
    print(m["user"]["full_name"], "-", m["file_id"])
