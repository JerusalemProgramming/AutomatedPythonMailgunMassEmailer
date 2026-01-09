## SCRIPT: P_CREATEDB_TEST.PY
## PURPOSE: CREATE TEST DATABASE WITH EMAIL SPLITTING LOGIC

import sqlite3
import csv
from datetime import datetime
import os

## CREATE LOGS FOLDER IF IT DOESN'T EXIST
os.makedirs("logs", exist_ok=True)

## DATABASE PATH
DBPath = "data.db"

## TABLE NAME FOR TESTING
TableName = "FamilyOffices"

## LOG FILE PATHS
TextLogPath = "logs/test_data_input.txt"
CsvLogPath = "logs/test_data_export.csv"

## DEFINE EMAIL VALIDATION COLUMNS
ValidationColumns = """
    ValidationSyntax INTEGER DEFAULT NULL,
    ValidationDomainExists INTEGER DEFAULT NULL,
    ValidationMxRecords INTEGER DEFAULT NULL,
    ValidationMailboxExists INTEGER DEFAULT NULL,
    ValidationIsDisposable INTEGER DEFAULT NULL,
    ValidationIsRoleBased INTEGER DEFAULT NULL,
    ValidationScore INTEGER DEFAULT NULL,
    ValidationStatus TEXT DEFAULT NULL,
    ValidationDateTime TEXT DEFAULT NULL,
    ValidationAttempts INTEGER DEFAULT NULL,
    ValidationErrorMessage TEXT DEFAULT NULL
"""

## DEFINE ALL EMAIL TRACKING COLUMNS
EmailColumns = """
    EmailSent INTEGER DEFAULT NULL,
    EmailSentDateTime TEXT DEFAULT NULL,
    EmailDelivered INTEGER DEFAULT NULL,
    EmailDeliveredDateTime TEXT DEFAULT NULL,
    EmailOpened INTEGER DEFAULT NULL,
    EmailClicked INTEGER DEFAULT NULL,
    EmailBounced INTEGER DEFAULT NULL,
    EmailRejected INTEGER DEFAULT NULL,
    EmailDropped INTEGER DEFAULT NULL,
    EmailComplained INTEGER DEFAULT NULL,
    EmailUnsubscribed INTEGER DEFAULT NULL,
    EmailStatus TEXT DEFAULT NULL,
    EmailFailureReason TEXT DEFAULT NULL,
    EmailFailureSeverity TEXT DEFAULT NULL,
    EmailAttempts INTEGER DEFAULT NULL,
    EmailAcceptedDateTime TEXT DEFAULT NULL,
    MailgunMessageID TEXT DEFAULT NULL,
    EmailSentToContact INTEGER DEFAULT NULL,
    EmailSentToCompany INTEGER DEFAULT NULL
"""

## CREATE TABLE SQL
CreateTableSql = f"""
    CREATE TABLE IF NOT EXISTS {TableName} (
        OfficeNumber TEXT,
        FirmName TEXT,
        AddressOfCompany TEXT,
        City TEXT,
        State_Province TEXT,
        PostalZipCode TEXT,
        Website TEXT,
        EmailOfCompany TEXT,
        ContactName_First TEXT,
        ContactName_Last TEXT,
        Contact_TitlePosition TEXT,
        NumberPhone TEXT,
        EmailOfContact TEXT,
        {ValidationColumns},
        {EmailColumns}
    )
"""
## OFFICE 1 - 2 COMMA-SEPARATED COMPANY EMAILS + 1 CONTACT EMAIL
## OFFICE 2 - 2 COMMA-SEPARATED COMPANY EMAILS + 1 CONTACT EMAIL
## OFFICE 3 - 1 COMPANY EMAIL + 2 COMMA-SEPARATED CONTACT EMAILS
## OFFICE 6 - 1 COMPANY EMAIL + 2 COMMA-SEPARATED CONTACT EMAILS
## OFFICE 4 - 1 COMPANY EMAIL + 1 CONTACT EMAIL
## OFFICE 5 - NO COMPANY EMAIL + 1 CONTACT EMAIL
## OFFICE 7 - 1 COMPANY EMAIL + NO CONTACT EMAIL

## TEST DATA - 7 OFFICES WITH REAL EMAIL ADDRESSES (RAW FORMAT WITH COMMA-SEPARATED EMAILS)
TestDataRaw = [
    ## OFFICE 1 - 2 COMMA-SEPARATED COMPANY EMAILS + 1 CONTACT EMAIL
    {
        "OfficeNumber": "1",
        "FirmName": "Z.Z. IMPORT EXPORT",
        "AddressOfCompany": "123 Main Street",
        "City": "New York",
        "State_Province": "NY",
        "PostalZipCode": "10001",
        "Website": "www.alphacapital.com",
        "EmailOfCompany": "info@zzimportexport.com, zzimportexport777@gmail.com",
        "ContactName_First": "David",
        "ContactName_Last": "Cohen",
        "Contact_TitlePosition": "Managing Director",
        "NumberPhone": "212-555-1001",
        "EmailOfContact": "bleon143143@gmail.com"
    },
    ## OFFICE 2 - 2 COMMA-SEPARATED COMPANY EMAILS + 1 CONTACT EMAIL
    {
        "OfficeNumber": "2",
        "FirmName": "TorahBibleCodes",
        "AddressOfCompany": "456 Oak Avenue",
        "City": "Los Angeles",
        "State_Province": "CA",
        "PostalZipCode": "90001",
        "Website": "www.betawealth.com",
        "EmailOfCompany": "info@torahbiblecodes.com, torahbiblecodes@gmail.com",
        "ContactName_First": "Michael",
        "ContactName_Last": "Johnson",
        "Contact_TitlePosition": "CEO",
        "NumberPhone": "310-555-2001",
        "EmailOfContact": "danielazariah143@gmail.com"
    },
    ## OFFICE 3 - 1 COMPANY EMAIL + 2 COMMA-SEPARATED CONTACT EMAILS
    {
        "OfficeNumber": "3",
        "FirmName": "ZZ Financing",
        "AddressOfCompany": "789 Pine Road",
        "City": "Chicago",
        "State_Province": "IL",
        "PostalZipCode": "60601",
        "Website": "www.gammainvest.com",
        "EmailOfCompany": "info@zzfinancing.com",
        "ContactName_First": "Benjamin",
        "ContactName_Last": "Franklin",
        "Contact_TitlePosition": "Partner",
        "NumberPhone": "312-555-3001",
        "EmailOfContact": "zzstockloans@gmail.com, brandon.l1@turing.com"
    },
    ## OFFICE 4 - 1 COMPANY EMAIL + 1 CONTACT EMAIL
    {
        "OfficeNumber": "4",
        "FirmName": "Teach ESL English",
        "AddressOfCompany": "321 Elm Street",
        "City": "Houston",
        "State_Province": "TX",
        "PostalZipCode": "77001",
        "Website": "www.deltafamily.com",
        "EmailOfCompany": "info@TeachESLEnglish.com",
        "ContactName_First": "William",
        "ContactName_Last": "Smith",
        "Contact_TitlePosition": "Director",
        "NumberPhone": "713-555-4001",
        "EmailOfContact": "teacheslenglish777@gmail.com"
    },
    ## OFFICE 5 - NO COMPANY EMAIL + 1 CONTACT EMAIL
    {
        "OfficeNumber": "5",
        "FirmName": "Jerusalem Programming",
        "AddressOfCompany": "654 Maple Drive",
        "City": "Miami",
        "State_Province": "FL",
        "PostalZipCode": "33101",
        "Website": "www.epsilonhold.com",
        "EmailOfCompany": "",
        "ContactName_First": "Jennifer",
        "ContactName_Last": "Adams",
        "Contact_TitlePosition": "President",
        "NumberPhone": "305-555-5001",
        "EmailOfContact": "danielyohai77@gmail.com"
    },
    ## OFFICE 6 - 1 COMPANY EMAIL + 2 COMMA-SEPARATED CONTACT EMAILS
    {
        "OfficeNumber": "6",
        "FirmName": "The Hypnosis Game",
        "AddressOfCompany": "654 Maple Drive",
        "City": "Miami",
        "State_Province": "FL",
        "PostalZipCode": "33101",
        "Website": "www.epsilonhold.com",
        "EmailOfCompany": "thehypnosisgame@gmail.com",
        "ContactName_First": "Jennifer",
        "ContactName_Last": "Adams",
        "Contact_TitlePosition": "President",
        "NumberPhone": "305-555-5001",
        "EmailOfContact": "JerusalemProgramming@gmail.com, jerusalemprogrammer@gmail.com"
    },
    ## OFFICE 7 - 1 COMPANY EMAIL + NO CONTACT EMAIL
    {
        "OfficeNumber": "7",
        "FirmName": "Gamma Holdings",
        "AddressOfCompany": "444 Maple Drive",
        "City": "Miami",
        "State_Province": "FL",
        "PostalZipCode": "33101",
        "Website": "www.epsilonhold.com",
        "EmailOfCompany": "info@cannabislaw.org.il",
        "ContactName_First": "John",
        "ContactName_Last": "Wick",
        "Contact_TitlePosition": "President",
        "NumberPhone": "305-555-5001",
        "EmailOfContact": ""
    }
]

## BEGIN DEFINE FUNCTION
def fn_ApplyEmailSplittingLogic(TestDataRaw):
    ## APPLY EMAIL SPLITTING LOGIC TO TEST DATA
    
    ## GROUP BY OFFICE NUMBER
    OfficeData = {}
    
    for Row in TestDataRaw:
        OfficeNum = Row.get('OfficeNumber', '').strip()
        
        if OfficeNum not in OfficeData:
            OfficeData[OfficeNum] = []
        
        ## GET AND SPLIT CONTACT EMAILS
        EmailOfContactRaw = Row.get('EmailOfContact', '').strip()
        ContactEmails = []
        if EmailOfContactRaw:
            if ',' in EmailOfContactRaw:
                ContactEmails = [Email.strip() for Email in EmailOfContactRaw.split(',') if Email.strip()]
            else:
                ContactEmails = [EmailOfContactRaw]
        
        ## IF CONTACT EMAILS EXIST, CREATE SEPARATE ROW FOR EACH
        if ContactEmails:
            for ContactEmail in ContactEmails:
                Contact = {
                    'OfficeNumber': OfficeNum,
                    'FirmName': Row.get('FirmName', ''),
                    'AddressOfCompany': Row.get('AddressOfCompany', ''),
                    'City': Row.get('City', ''),
                    'State_Province': Row.get('State_Province', ''),
                    'PostalZipCode': Row.get('PostalZipCode', ''),
                    'Website': Row.get('Website', ''),
                    'EmailOfCompany': Row.get('EmailOfCompany', ''),
                    'ContactName_First': Row.get('ContactName_First', ''),
                    'ContactName_Last': Row.get('ContactName_Last', ''),
                    'Contact_TitlePosition': Row.get('Contact_TitlePosition', ''),
                    'NumberPhone': Row.get('NumberPhone', ''),
                    'EmailOfContact': ContactEmail
                }
                OfficeData[OfficeNum].append(Contact)
        else:
            ## NO CONTACT EMAIL - CREATE BASE ROW AS-IS
            Contact = {
                'OfficeNumber': OfficeNum,
                'FirmName': Row.get('FirmName', ''),
                'AddressOfCompany': Row.get('AddressOfCompany', ''),
                'City': Row.get('City', ''),
                'State_Province': Row.get('State_Province', ''),
                'PostalZipCode': Row.get('PostalZipCode', ''),
                'Website': Row.get('Website', ''),
                'EmailOfCompany': Row.get('EmailOfCompany', ''),
                'ContactName_First': Row.get('ContactName_First', ''),
                'ContactName_Last': Row.get('ContactName_Last', ''),
                'Contact_TitlePosition': Row.get('Contact_TitlePosition', ''),
                'NumberPhone': Row.get('NumberPhone', ''),
                'EmailOfContact': ''
            }
            OfficeData[OfficeNum].append(Contact)
    
    ## DEDUPLICATE AND ADD SPLIT COMPANY EMAILS PER OFFICE
    for OfficeNumber, ContactsList in OfficeData.items():
        CompanyEmailsAdded = set()
        if ContactsList:
            FirstContact = ContactsList[0]
            
            ## COLLECT ALL UNIQUE COMPANY EMAILS FROM ALL ROWS IN THIS OFFICE
            for Contact in ContactsList:
                EmailOfCompanyRaw = Contact.get('EmailOfCompany', '').strip()
                if EmailOfCompanyRaw:
                    if ',' in EmailOfCompanyRaw:
                        CompanyEmails = [Email.strip() for Email in EmailOfCompanyRaw.split(',') if Email.strip()]
                    else:
                        CompanyEmails = [EmailOfCompanyRaw]
                    
                    ## ADD EACH UNIQUE COMPANY EMAIL AS COMPANY-ONLY ROW
                    for CompanyEmail in CompanyEmails:
                        if CompanyEmail not in CompanyEmailsAdded:
                            CompanyEmailsAdded.add(CompanyEmail)
                            CompanyContact = {
                                'OfficeNumber': OfficeNumber,
                                'FirmName': FirstContact.get('FirmName', ''),
                                'AddressOfCompany': FirstContact.get('AddressOfCompany', ''),
                                'City': FirstContact.get('City', ''),
                                'State_Province': FirstContact.get('State_Province', ''),
                                'PostalZipCode': FirstContact.get('PostalZipCode', ''),
                                'Website': FirstContact.get('Website', ''),
                                'EmailOfCompany': CompanyEmail,
                                'ContactName_First': '',
                                'ContactName_Last': '',
                                'Contact_TitlePosition': '',
                                'NumberPhone': '',
                                'EmailOfContact': ''
                            }
                            ContactsList.append(CompanyContact)
    
    ## RETURN OFFICE DATA
    return OfficeData

## END DEFINE FUNCTION

## BEGIN DEFINE FUNCTION
def fn_WriteTextLog(OfficeData):
    ## WRITE TEXT LOG OF INPUT DATA
    
    TotalRows = sum(len(Contacts) for Contacts in OfficeData.values())
    
    with open(TextLogPath, 'w', encoding='utf-8') as File:
        File.write("=" * 80 + "\n")
        File.write("TEST DATA INPUT LOG\n")
        File.write(f"GENERATED: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        File.write(f"TABLE: {TableName}\n")
        File.write(f"TOTAL OFFICES: {len(OfficeData)}\n")
        File.write(f"TOTAL ROWS (AFTER EMAIL SPLITTING): {TotalRows}\n")
        File.write("=" * 80 + "\n\n")
        
        for OfficeNumber, ContactsList in OfficeData.items():
            File.write(f"OFFICE {OfficeNumber}:\n")
            File.write("-" * 80 + "\n")
            for Index, Contact in enumerate(ContactsList, start=1):
                File.write(f"  ROW {Index}:\n")
                for Key, Value in Contact.items():
                    File.write(f"    {Key}: {Value}\n")
                File.write("\n")

## END DEFINE FUNCTION

## BEGIN DEFINE FUNCTION
def fn_ExportCsv(Connection):
    ## EXPORT DATABASE TABLE TO CSV
    
    Cursor = Connection.cursor()
    
    ## GET ALL DATA FROM TABLE
    Cursor.execute(f"SELECT * FROM {TableName}")
    Rows = Cursor.fetchall()
    
    ## GET COLUMN NAMES
    ColumnNames = [Description[0] for Description in Cursor.description]
    
    ## WRITE CSV
    with open(CsvLogPath, 'w', newline='', encoding='utf-8') as File:
        Writer = csv.writer(File, delimiter=';')
        Writer.writerow(ColumnNames)
        Writer.writerows(Rows)

## END DEFINE FUNCTION

## MAIN SCRIPT
if __name__ == "__main__":
    
    ## APPLY EMAIL SPLITTING LOGIC
    print("## APPLYING EMAIL SPLITTING LOGIC...")
    OfficeData = fn_ApplyEmailSplittingLogic(TestDataRaw)
    
    ## CONNECT TO DATABASE
    Connection = sqlite3.connect(DBPath)
    Cursor = Connection.cursor()
    
    ## DROP TABLE IF EXISTS
    Cursor.execute(f"DROP TABLE IF EXISTS {TableName}")
    
    ## CREATE TABLE
    Cursor.execute(CreateTableSql)
    
    ## TRACK TOTAL ROWS INSERTED
    TotalRowsInserted = 0
    
    ## INSERT ALL ROWS (CONTACT ROWS AND COMPANY-ONLY ROWS)
    for OfficeNumber, ContactsList in OfficeData.items():
        for Contact in ContactsList:
            Columns = ", ".join(Contact.keys())
            Placeholders = ", ".join(["?" for _ in Contact])
            Values = tuple(Contact.values())
            
            InsertSql = f"INSERT INTO {TableName} ({Columns}) VALUES ({Placeholders})"
            Cursor.execute(InsertSql, Values)
            TotalRowsInserted += 1
    
    ## COMMIT
    Connection.commit()
    
    ## WRITE TEXT LOG OF INPUT DATA
    print(f"## CREATING TEXT LOG: {TextLogPath}")
    fn_WriteTextLog(OfficeData)
    
    ## EXPORT TO CSV
    print(f"## CREATING CSV EXPORT: {CsvLogPath}")
    fn_ExportCsv(Connection)
    
    ## CLOSE CONNECTION
    Connection.close()
    
    print(f"\n## TEST DATABASE CREATED: {DBPath}")
    print(f"## TABLE: {TableName}")
    print(f"## TOTAL OFFICES: {len(OfficeData)}")
    print(f"## TOTAL ROWS (AFTER EMAIL SPLITTING): {TotalRowsInserted}")
    print(f"## TEXT LOG: {TextLogPath}")
    print(f"## CSV EXPORT: {CsvLogPath}")