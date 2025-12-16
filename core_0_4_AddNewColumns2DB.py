## IMPORT MODULES
import sqlite3

## DEFINE FUNCTION
def fn_AddNewColumns2DB():
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
    
    ## DEFINE COLUMNS TO ADD
    Columns = [
        "EmailSent INTEGER DEFAULT 0",
        "EmailSentDateTime TEXT DEFAULT NULL",
        "EmailDelivered INTEGER DEFAULT 0",
        "EmailOpened INTEGER DEFAULT 0",
        "EmailClicked INTEGER DEFAULT 0",
        "EmailBounced INTEGER DEFAULT 0",
        "EmailComplained INTEGER DEFAULT 0",
        "EmailUnsubscribed INTEGER DEFAULT 0",
        "EmailStatus TEXT DEFAULT 'pending'",
        "EmailAttempts INTEGER DEFAULT 0",
        "MailgunMessageID TEXT DEFAULT NULL",
        "EmailSentToContact INTEGER DEFAULT 0",
        "EmailSentToCompany INTEGER DEFAULT 0",
        "EmailOfContact_PreNormalize TEXT DEFAULT NULL",
        "EmailOfCompany_PreNormalize TEXT DEFAULT NULL",
        "NumberPhone_PreNormalize TEXT DEFAULT NULL",
        "NumberFax_PreNormalize TEXT DEFAULT NULL"
    ]
    
    ## CONNECT TO DATABASE
    Connection = sqlite3.connect(DBPath)
    Cursor = Connection.cursor()
    
    ## ADD MAILGUN EMAIL STATUS + PRENORMALIZE BACKUP COLUMNS TO DB TABLES
    print(f"\nADDING EMAIL STATUS + PRENORMALIZE BACKUP COLUMNS TO DB TABLES")

    ## LOOP THROUGH EACH TABLE
    for TableName in TableNames:

        ## LOOP THROUGH EACH COLUMN
        for Column in Columns:
        
            try:
        
                ## ADD COLUMN TO TABLE
                Query = f"ALTER TABLE {TableName} ADD COLUMN {Column}"
                Cursor.execute(Query)
                print(f"Added column to {TableName}: {Column.split()[0]}")
        
            except sqlite3.OperationalError as E:
        
                ## COLUMN ALREADY EXISTS
                if "duplicate column name" in str(E).lower():
                    print(f"Column already exists in {TableName}: {Column.split()[0]}")
                else:
                    ## OTHER ERROR
                    print(f"Error adding column to {TableName}: {E}")
    
    ## COMMIT CHANGES AND CLOSE CONNECTION
    Connection.commit()
    Connection.close()
    
    ## RETURN SUCCESS MESSAGE
    return "Email tracking columns and PreNormalize Columns added to all tables successfully."