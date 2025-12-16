## IMPORT MODULES
import sqlite3

## DEFINE FUNCTION
def fn_VerifyNewColumnsInDB():
    ## DECLARE VARIABLES
    DBPath = "data.db"
    TableNames = [
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
    
    ## EXPECTED EMAIL COLUMNS
    ExpectedNewColumns = [
        "EmailSent",
        "EmailSentDateTime",
        "EmailDelivered",
        "EmailOpened",
        "EmailClicked",
        "EmailBounced",
        "EmailComplained",
        "EmailUnsubscribed",
        "EmailStatus",
        "EmailAttempts",
        "MailgunMessageID",
        "EmailSentToContact",
        "EmailSentToCompany",
        "EmailOfContact_PreNormalize",
        "EmailOfCompany_PreNormalize",
        "NumberPhone_PreNormalize",
        "NumberFax_PreNormalize"
    ]
    
    ## CONNECT TO DATABASE
    Connection = sqlite3.connect(DBPath)
    Cursor = Connection.cursor()
    
    ## BUILD REPORT
    Report = "\n" + "="*60 + "\n"
    Report += "EMAIL STATUS + PRENORMALIZE BACKUP COLUMNS VERIFICATION REPORT\n"
    Report += "="*60 + "\n\n"
    
    AllTablesValid = True
    
    ## LOOP THROUGH EACH TABLE
    for TableName in TableNames:
        ## GET TABLE SCHEMA
        Cursor.execute(f"PRAGMA table_info({TableName})")
        Columns = Cursor.fetchall()
        
        ## EXTRACT COLUMN NAMES
        ColumnNames = [Col[1] for Col in Columns]
        
        ## CHECK FOR EMAIL COLUMNS
        Report += f"TABLE: {TableName}\n"
        Report += f"Total Columns: {len(ColumnNames)}\n"
        
        MissingColumns = []
        PresentColumns = []
        
        for NewCol in ExpectedNewColumns:
            if NewCol in ColumnNames:
                PresentColumns.append(NewCol)
            else:
                MissingColumns.append(NewCol)
                AllTablesValid = False
        
        Report += f"Email Status + PreNormalize Backup Columns Present: {len(PresentColumns)}/17\n"
        
        if MissingColumns:
            Report += f"MISSING COLUMNS: {', '.join(MissingColumns)}\n"
        else:
            Report += "STATUS: All Email Status and PreNormalize Backup Columns present ✓\n"
        
        Report += "-"*60 + "\n\n"
    
    ## CLOSE CONNECTION
    Connection.close()
    
    ## FINAL STATUS
    if AllTablesValid:
        Report += "OVERALL STATUS: All tables have all Email Status and PreNormalize Backup columns ✓\n"
    else:
        Report += "OVERALL STATUS: Some tables are missing Email Status and/or PreNormalize Backup columns ✗\n"
    
    Report += "="*60 + "\n"
    
    ## RETURN REPORT
    return Report