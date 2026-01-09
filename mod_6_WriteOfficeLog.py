## MODULE: MOD_6_WRITEOFFICELOG.PY
## PURPOSE: WRITE INDIVIDUAL OFFICE PROCESSING LOG (TXT + CSV)

import os
from datetime import datetime

def fn_WriteOfficeLog(TableName, OfficeNumber, LogData, LogDir):
    """
    ## WRITE INDIVIDUAL OFFICE PROCESSING LOG (TXT AND CSV)
    ## INPUT: TABLENAME (STRING), OFFICENUMBER (STRING), LOGDATA (DICT), LOGDIR (STRING)
    ## OUTPUT: DICTIONARY WITH TXTLOGPATH AND CSVLOGPATH
    """
    
    ## INITIALIZE OUTPUT
    Result = {
        "TxtLogPath": "",
        "CsvLogPath": ""
    }
    
    ## CREATE TIMESTAMP FOR FILENAMES
    Timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    ## ENSURE TABLE SUBDIRECTORY EXISTS
    TableLogDir = os.path.join(LogDir, TableName)
    os.makedirs(TableLogDir, exist_ok=True)
    
    ## BUILD FILE PATHS
    BaseFilename = f"{TableName}_Office_{OfficeNumber}_{Timestamp}"
    TxtLogPath = os.path.join(TableLogDir, f"{BaseFilename}.log")
    CsvLogPath = os.path.join(TableLogDir, f"{BaseFilename}.csv")
    
    ## EXTRACT LOG DATA
    FirmName = LogData.get("FirmName", "")
    ContactResults = LogData.get("ContactResults", [])
    CompanyResults = LogData.get("CompanyResults", [])
    
    ## CALCULATE SUMMARY STATS
    ContactSent = sum(1 for R in ContactResults if R.get("Success"))
    CompanySent = sum(1 for R in CompanyResults if R.get("Success"))
    TotalRowsUpdated = len(ContactResults) + len(CompanyResults)
    Failures = sum(1 for R in ContactResults if not R.get("Success")) + sum(1 for R in CompanyResults if not R.get("Success"))
    
    ## WRITE TXT LOG
    try:
        with open(TxtLogPath, "w", encoding="utf-8") as TxtFile:
            TxtFile.write(f"=== OFFICE {OfficeNumber} - {FirmName} ===\n")
            TxtFile.write(f"Timestamp: {Timestamp}\n")
            TxtFile.write(f"Table: {TableName}\n\n")
            
            ## CONTACT EMAILS SECTION
            TxtFile.write("CONTACT EMAILS:\n")
            if ContactResults:
                for Index, R in enumerate(ContactResults, 1):
                    TxtFile.write(f"  {Index}. {R.get('Email', '')}\n")
                    TxtFile.write(f"     - Status: {R.get('Status', '')}\n")
                    TxtFile.write(f"     - Mailgun ID: {R.get('MailgunMessageID', '')}\n")
                    TxtFile.write(f"     - Attempts: {R.get('Attempts', '')}\n")
            else:
                TxtFile.write("  (none)\n")
            TxtFile.write("\n")
            
            ## COMPANY EMAILS SECTION
            TxtFile.write("COMPANY EMAILS:\n")
            if CompanyResults:
                for Index, R in enumerate(CompanyResults, 1):
                    TxtFile.write(f"  {Index}. {R.get('Email', '')}\n")
                    TxtFile.write(f"     - Status: {R.get('Status', '')}\n")
                    TxtFile.write(f"     - Mailgun ID: {R.get('MailgunMessageID', '')}\n")
                    TxtFile.write(f"     - Attempts: {R.get('Attempts', '')}\n")
                    TxtFile.write(f"     - Row ID: {R.get('RowID', '')}\n")
            else:
                TxtFile.write("  (none)\n")
            TxtFile.write("\n")
            
            ## SUMMARY SECTION
            TxtFile.write("SUMMARY:\n")
            TxtFile.write(f"  - Contact emails sent: {ContactSent}\n")
            TxtFile.write(f"  - Company emails sent: {CompanySent}\n")
            TxtFile.write(f"  - Total rows updated: {TotalRowsUpdated}\n")
            TxtFile.write(f"  - Failures: {Failures}\n\n")
            
            TxtFile.write(f"=== END OFFICE {OfficeNumber} ===\n")
        
        Result["TxtLogPath"] = TxtLogPath
        
    except Exception as E:
        print(f"## ERROR WRITING TXT LOG: {E}")
    
    ## WRITE CSV LOG
    try:
        with open(CsvLogPath, "w", encoding="utf-8") as CsvFile:
            ## WRITE HEADER (SEMICOLON DELIMITER)
            CsvFile.write("Timestamp;Table;OfficeNumber;EmailType;EmailAddress;Status;MailgunMessageID;Attempts;RowID;ErrorMessage\n")
            
            ## WRITE CONTACT EMAIL ROWS
            for R in ContactResults:
                RowIdStr = str(R.get("RowID", ""))
                ErrorMsg = R.get("ErrorMessage", "") or ""
                CsvFile.write(f"{Timestamp};{TableName};{OfficeNumber};contact;{R.get('Email', '')};{R.get('Status', '')};{R.get('MailgunMessageID', '')};{R.get('Attempts', '')};{RowIdStr};{ErrorMsg}\n")
            
            ## WRITE COMPANY EMAIL ROWS
            for R in CompanyResults:
                RowIdStr = str(R.get("RowID", ""))
                ErrorMsg = R.get("ErrorMessage", "") or ""
                CsvFile.write(f"{Timestamp};{TableName};{OfficeNumber};company;{R.get('Email', '')};{R.get('Status', '')};{R.get('MailgunMessageID', '')};{R.get('Attempts', '')};{RowIdStr};{ErrorMsg}\n")
        
        Result["CsvLogPath"] = CsvLogPath
        
    except Exception as E:
        print(f"## ERROR WRITING CSV LOG: {E}")
    
    return Result