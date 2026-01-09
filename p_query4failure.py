import sqlite3

conn = sqlite3.connect("data.db")
cursor = conn.cursor()

cursor.execute("""
    SELECT OfficeNumber, FirmName, EmailOfCompany, EmailOfContact, 
           EmailStatus, EmailFailureReason, EmailFailureSeverity,
           ContactName_First, EmailSentToCompany
    FROM FamilyOffices 
    WHERE EmailStatus = 'failed' OR EmailStatus = 'rejected'
    ORDER BY OfficeNumber
""")

results = cursor.fetchall()
for row in results:
    print(row)

conn.close()