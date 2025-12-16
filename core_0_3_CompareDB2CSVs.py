## IMPORT MODULES
import sqlite3
import csv
## DECLARE VARIABLES
DBPath = "data.db"
## TABLE NAMES AND CORRESPONDING CSV FILES
TableCSVPairs = [
    ("FamilyOffices", "DATA_INPUT/DB_1_FamilyOffices.csv"),
    ("WealthManagement", "DATA_INPUT/DB_2_WealthManagement.csv"),
    ("Endowments", "DATA_INPUT/DB_3_Endowments.csv"),
    ("InstitutionalInvestment", "DATA_INPUT/DB_4_InstitutionalInvestment.csv"),
    ("InvestmentBanking", "DATA_INPUT/DB_5_InvestmentBanking.csv"),
    ("PrivateBanks", "DATA_INPUT/DB_6_PrivateBanks.csv"),
    ("MerchantBanks", "DATA_INPUT/DB_7_MerchantBanks.csv"),
    ("PensionFunds", "DATA_INPUT/DB_8_PensionFunds.csv"),
    ("FundOfFund", "DATA_INPUT/DB_9_FundOfFund.csv")
]
## TABLES WITH MULTIPLE CONTACTS PER CSV ROW (EXPANDED IN DB)
TablesWithExpansion = ["FundOfFund"]

## BEGIN DEFINE FUNCTION
def fn_CompareDB2CSVs():

    # VERIFY ALL DATABASE TABLES AGAINST SOURCE CSV FILES
    
    ## CONNECT TO DATABASE
    Connection = sqlite3.connect(DBPath)
    Cursor = Connection.cursor()
    
    ## BUILD VERIFICATION REPORT
    Report = f"\nDATABASE TO CSVs COMPARISON REPORT\n"
    Report += f"=" * 80 + "\n\n"
    
    TotalMismatches = 0
    
    ## LOOP THROUGH EACH TABLE-CSV PAIR
    for TableName, CSVFilePath in TableCSVPairs:
        
        ## GET DB ROW COUNT
        Cursor.execute(f"SELECT COUNT(*) FROM {TableName}")
        DBRowCount = Cursor.fetchone()[0]
        
        ## GET DB COLUMN COUNT
        Cursor.execute(f"PRAGMA table_info({TableName})")
        Columns = Cursor.fetchall()
        DBColumnCount = len(Columns)
        ColumnNames = [col[1] for col in Columns]
        
        ## GET CSV ROW COUNT AND SECONDARY CONTACT COUNT
        CSVRowCount = 0
        SecondaryContactCount = 0
        
        with open(CSVFilePath, 'r', encoding='utf-8') as CsvFile:
            Reader = csv.DictReader(CsvFile, delimiter=';')
            for Row in Reader:
                CSVRowCount += 1
                ## COUNT SECONDARY CONTACTS FOR FUNDOFFUND
                if TableName == "FundOfFund":
                    SecondaryName = Row.get('SecondaryContact_Name', '').strip()
                    if SecondaryName:
                        SecondaryContactCount += 1
        
        ## CHECK FOR MISMATCH
        if TableName in TablesWithExpansion:
            ## FOR TABLES WITH EXPANSION, EXPECTED = CSV + SECONDARY CONTACTS
            ExpectedDBRows = CSVRowCount + SecondaryContactCount
            IsMatch = (DBRowCount == ExpectedDBRows)
            StatusMsg = f"EXPANSION {'✓' if IsMatch else '✗'} (Expected: {ExpectedDBRows})"
        else:
            ## FOR NORMAL TABLES, EXACT MATCH EXPECTED
            IsMatch = (CSVRowCount == DBRowCount)
            StatusMsg = "MATCH ✓" if IsMatch else "MISMATCH ✗"
        
        if not IsMatch:
            TotalMismatches += 1
        
        ## ADD TO REPORT
        Report += f"Table: {TableName}\n"
        Report += f"  CSV File: {CSVFilePath}\n"
        Report += f"  CSV Rows: {CSVRowCount}\n"
        if TableName in TablesWithExpansion:
            Report += f"  Secondary Contacts: {SecondaryContactCount}\n"
        Report += f"  DB Rows: {DBRowCount}\n"
        Report += f"  DB Columns: {DBColumnCount}\n"
        Report += f"  Status: {StatusMsg}\n"
        Report += f"  Column Names: {', '.join(ColumnNames[:5])}{'...' if len(ColumnNames) > 5 else ''}\n\n"
    
    ## CLOSE CONNECTION
    Connection.close()
    
    ## ADD SUMMARY
    Report += f"=" * 80 + "\n"
    Report += f"SUMMARY: {len(TableCSVPairs) - TotalMismatches}/{len(TableCSVPairs)} tables verified\n"
    if TotalMismatches > 0:
        Report += f"WARNING: {TotalMismatches} table(s) have mismatches!\n"
    
    ## RETURN REPORT
    return Report
## END DEFINE FUNCTION