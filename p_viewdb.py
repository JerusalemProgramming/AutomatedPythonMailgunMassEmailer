## SCRIPT: VIEW_DB.PY
## PURPOSE: VIEW DATABASE CONTENTS

import sqlite3
from config import DB_PATH, TABLE_NAMES

def fn_ViewDatabase():
    """
    ## VIEW ALL TABLES AND THEIR CONTENTS
    """
    
    Connection = sqlite3.connect(DB_PATH)
    Cursor = Connection.cursor()
    
    ## GET LIST OF ALL TABLES IN DATABASE
    Cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    Tables = [Row[0] for Row in Cursor.fetchall()]
    
    print(f"DATABASE: {DB_PATH}")
    print(f"TABLES FOUND: {Tables}")
    print("=" * 80)
    
    for TableName in Tables:
        print(f"\nTABLE: {TableName}")
        print("-" * 40)
        
        ## GET ROW COUNT
        Cursor.execute(f"SELECT COUNT(*) FROM {TableName}")
        RowCount = Cursor.fetchone()[0]
        print(f"ROWS: {RowCount}")
        
        ## GET COLUMN NAMES
        Cursor.execute(f"PRAGMA table_info({TableName})")
        Columns = [Row[1] for Row in Cursor.fetchall()]
        print(f"COLUMNS: {Columns}")
        
        ## GET ALL ROWS
        Cursor.execute(f"SELECT rowid, * FROM {TableName}")
        Rows = Cursor.fetchall()
        
        print("\nDATA:")
        for Row in Rows:
            print(f"  rowid={Row[0]}")
            for Index, ColName in enumerate(Columns):
                Value = Row[Index + 1]
                if Value is not None:
                    print(f"    {ColName}: {Value}")
            print()
    
    Connection.close()


def fn_ViewEmailStatus():
    """
    ## VIEW EMAIL STATUS COLUMNS ONLY
    """
    
    Connection = sqlite3.connect(DB_PATH)
    Cursor = Connection.cursor()
    
    ## GET LIST OF ALL TABLES IN DATABASE
    Cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    Tables = [Row[0] for Row in Cursor.fetchall()]
    
    print(f"DATABASE: {DB_PATH}")
    print("EMAIL STATUS SUMMARY")
    print("=" * 80)
    
    for TableName in Tables:
        print(f"\nTABLE: {TableName}")
        print("-" * 40)
        
        Cursor.execute(f"""
            SELECT rowid, OfficeNumber, FirmName, EmailOfContact, EmailOfCompany,
                   EmailSent, EmailStatus, EmailAttempts, MailgunMessageID
            FROM {TableName}
        """)
        Rows = Cursor.fetchall()
        
        for Row in Rows:
            print(f"  rowid={Row[0]} | Office={Row[1]} | Firm={Row[2]}")
            print(f"    ContactEmail: {Row[3]}")
            print(f"    CompanyEmail: {Row[4]}")
            print(f"    Sent={Row[5]} | Status={Row[6]} | Attempts={Row[7]}")
            print(f"    MailgunID: {Row[8]}")
            print()
    
    Connection.close()


## MAIN
if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--status":
        fn_ViewEmailStatus()
    else:
        fn_ViewDatabase()
        print("\nTIP: Run with --status to see email status only")