## SCRIPT: EXPORT_DB_TO_CSV.PY
## PURPOSE: EXPORT CURRENT DATABASE STATE TO CSV WITH ALL COLUMNS

import sqlite3
import csv
import os
from datetime import datetime

## CREATE LOGS FOLDER IF IT DOESN'T EXIST
os.makedirs("logs", exist_ok=True)

## DATABASE PATH
DB_PATH = "data.db"

## OUTPUT FOLDER
OUTPUT_FOLDER = "logs"

## AVAILABLE TABLES
TABLE_NAMES = [
    "FamilyOffices",
    "WealthManagement",
    "Endowments",
    "InstitutionalInvestment",
    "InvestmentBanking",
    "PrivateBanks",
    "MerchantBanks",
    "PensionFunds",
    "FundOfFund"
]

def fn_DisplayTableMenu():
    """
    ## DISPLAY NUMBERED LIST OF AVAILABLE TABLES
    """
    print("\n" + "="*50)
    print("AVAILABLE TABLES:")
    print("="*50)
    for Index, TableName in enumerate(TABLE_NAMES, start=1):
        print(f"  {Index}. {TableName}")
    print("="*50)

def fn_GetTableSelection():
    """
    ## PROMPT USER TO SELECT A TABLE BY NUMBER
    ## RETURNS: SELECTED TABLE NAME OR NONE IF INVALID
    """
    while True:
        try:
            fn_DisplayTableMenu()
            Choice = input("\nSELECT TABLE NUMBER TO EXPORT (OR 'Q' TO QUIT): ").strip().upper()
            
            if Choice == 'Q':
                return None
            
            Choice = int(Choice)
            
            if 1 <= Choice <= len(TABLE_NAMES):
                SelectedTable = TABLE_NAMES[Choice - 1]
                print(f"\nSELECTED: {SelectedTable}")
                return SelectedTable
            else:
                print(f"\nINVALID CHOICE. PLEASE SELECT 1-{len(TABLE_NAMES)}")
        
        except ValueError:
            print("\nINVALID INPUT. PLEASE ENTER A NUMBER.")

def fn_ExportTableToCsv(TableName):
    """
    ## EXPORT DATABASE TABLE TO CSV WITH TIMESTAMP
    """
    ## CREATE OUTPUT FOLDER IF IT DOESN'T EXIST
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)
    
    ## GENERATE TIMESTAMP FILENAME
    Timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    CsvFilename = f"{OUTPUT_FOLDER}/{TableName}_export_{Timestamp}.csv"
    
    ## CONNECT TO DATABASE
    Connection = sqlite3.connect(DB_PATH)
    Cursor = Connection.cursor()
    
    try:
        ## GET ALL DATA FROM TABLE
        Cursor.execute(f"SELECT * FROM {TableName}")
        Rows = Cursor.fetchall()
        
        ## GET COLUMN NAMES
        ColumnNames = [Description[0] for Description in Cursor.description]
        
        ## WRITE CSV WITH SEMICOLON DELIMITER
        with open(CsvFilename, 'w', newline='', encoding='utf-8') as File:
            Writer = csv.writer(File, delimiter=';')
            Writer.writerow(ColumnNames)
            Writer.writerows(Rows)
        
        print(f"\nEXPORT SUCCESSFUL!")
        print(f"FILE: {CsvFilename}")
        print(f"ROWS EXPORTED: {len(Rows)}")
        print(f"COLUMNS: {len(ColumnNames)}")
        
    except sqlite3.Error as Error:
        print(f"\nDATABASE ERROR: {Error}")
    
    finally:
        Connection.close()

## MAIN SCRIPT
if __name__ == "__main__":
    
    print("DATABASE EXPORT UTILITY")
    print("="*50)
    
    ## GET TABLE SELECTION FROM USER
    SelectedTable = fn_GetTableSelection()
    
    if SelectedTable is None:
        print("\nEXITING PROGRAM.")
    else:
        ## EXPORT TABLE TO CSV
        fn_ExportTableToCsv(SelectedTable)