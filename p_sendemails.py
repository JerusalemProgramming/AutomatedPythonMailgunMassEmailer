## IMPORT MODULES
import argparse
import time
from datetime import datetime
from tqdm import tqdm
from config import TABLE_NAMES, MAX_ATTEMPTS, MAILGUN_CONFIG, LOG_DIR, MAX_OFFICES_PER_SESSION
import mod_00_GetUserInput as mod_00
import mod_0_QueryOfficeListInDB as mod_0
import mod_1_QueryOfficeDataInDB as mod_1
import mod_2_ExtractUniqueEmailsFromOffice as mod_2
import mod_2A_ValidateEmailBatch as mod_2A
import mod_3_BuildEmailTemplate as mod_3
import mod_4_SendEmailViaMailgun as mod_4
import mod_5_UpdateEmailStatusInDB as mod_5
import mod_6_WriteOfficeLog as mod_6
import mod_7_WriteSummaryLog as mod_7
import mod_8_CalculateHumanDelay as mod_8

## python p.py --retry-failed --office-range 1-2 --table FamilyOffices
## python p.py --retry-failed --max-offices 5 --table FamilyOffices

## DECLARE VARIABLES
IncludeFailedEmails = False

## BEGIN MAIN PROGRAM
if __name__ == "__main__":
    
    ## PARSE CLI ARGUMENTS
    Parser = argparse.ArgumentParser(description="Email Campaign System")
    Parser.add_argument("--retry-failed", action="store_true", help="Include failed emails for retry")
    Parser.add_argument("--max-offices", type=int, help="Max offices to process this session")
    Parser.add_argument("--table", type=str, help="Specific table to process")
    Parser.add_argument("--office-range", type=str, help="Office range to process (e.g., 1-50)")
    Args = Parser.parse_args()
    
    ## DETERMINE MODE: CLI OR INTERACTIVE
    CliMode = Args.table is not None or Args.max_offices is not None or Args.office_range is not None
    
    ## SET FLAGS BASED ON CLI ARGUMENTS
    IncludeFailedEmails = Args.retry_failed
    
    ## INTERACTIVE MODE LOOP
    ContinueProcessing = True
    
    while ContinueProcessing:
        
        ## GET TABLE AND OFFICE INPUT
        if CliMode:
            ## CLI MODE - PROCESS SPECIFIED TABLE OR ALL TABLES
            if Args.table:
                TablesToProcess = [Args.table]
            else:
                TablesToProcess = TABLE_NAMES
            MaxOffices = Args.max_offices if Args.max_offices else MAX_OFFICES_PER_SESSION
            
            ## PARSE OFFICE RANGE IF PROVIDED
            if Args.office_range:
                try:
                    Parts = Args.office_range.split('-')
                    if len(Parts) != 2:
                        print("ERROR: Invalid office range format. Use format: START-END (e.g., 1-50)")
                        break
                    OfficeInput = {
                        "type": "range",
                        "start": int(Parts[0].strip()),
                        "end": int(Parts[1].strip())
                    }
                    OfficeInputType = "range"
                except ValueError:
                    print("ERROR: Invalid office range values. Must be integers.")
                    break
            else:
                OfficeInputType = "count"
            
            ContinueProcessing = False  ## CLI MODE RUNS ONCE
        else:
            ## INTERACTIVE MODE - GET USER INPUT
            SelectedTable = mod_00.fn_GetTableSelection()
            
            if SelectedTable is None:
                print("\nEXITING PROGRAM.")
                break
            
            TablesToProcess = [SelectedTable]
            
            ## GET RETRY FAILED INPUT
            IncludeFailedEmails = mod_00.fn_GetRetryFailedInput()
            
            ## GET OFFICE INPUT
            OfficeInput = mod_00.fn_GetOfficeInput()
            OfficeInputType = OfficeInput["type"]
        
        ## INITIALIZE SESSION OFFICE COUNTER
        SessionOfficeCount = 0
        SessionLimitReached = False
        
        ## INITIALIZE CAMPAIGN STATS
        CampaignStats = {
            "TablesProcessed": 0,
            "OfficesProcessed": 0,
            "ContactEmailsSent": 0,
            "CompanyEmailsSent": 0,
            "Failures": 0,
            "StartTime": datetime.now(),
            "EndTime": None,
            "TableStats": {}
        }
        
        ## LOOP THROUGH EACH TABLE
        for TableName in TablesToProcess:
            
            ## CHECK IF SESSION LIMIT REACHED
            if SessionLimitReached:
                break
            
            print(f"\nProcessing table: {TableName}")
            
            ## INITIALIZE TABLE STATS
            CampaignStats["TableStats"][TableName] = {
                "OfficesProcessed": 0,
                "ContactEmailsSent": 0,
                "CompanyEmailsSent": 0,
                "Failures": 0
            }
            
            ## GET LIST OF OFFICES WITH PENDING/FAILED EMAILS
            OfficeList = mod_0.fn_QueryOfficeListInDB(TableName, IncludeFailedEmails, MAX_ATTEMPTS)
            
            ## CALCULATE OFFICES TO PROCESS BASED ON INPUT TYPE
            if OfficeInputType == "count":
                ## COUNT MODE - TAKE NEXT N OFFICES
                if CliMode:
                    RemainingOffices = MaxOffices - SessionOfficeCount
                else:
                    RemainingOffices = OfficeInput["value"] - SessionOfficeCount
                OfficesToProcess = OfficeList[:RemainingOffices]
            else:
                ## RANGE MODE - FILTER BY OFFICE NUMBER RANGE
                StartOffice = OfficeInput["start"]
                EndOffice = OfficeInput["end"]
                OfficesToProcess = [Office for Office in OfficeList if StartOffice <= int(Office) <= EndOffice]
            
            ## OUTER PROGRESS BAR - OFFICES
            OfficeProgressBar = tqdm(OfficesToProcess, desc="Offices", unit="office", leave=True)
            
            ## LOOP THROUGH EACH OFFICE
            for OfficeNumber in OfficeProgressBar:
                
                ## UPDATE PROGRESS BAR DESCRIPTION
                OfficeProgressBar.set_postfix({"Current": OfficeNumber})
                
                ## GET ALL CONTACT DATA FOR THIS OFFICE
                OfficeData = mod_1.fn_QueryOfficeDataInDB(TableName, OfficeNumber, IncludeFailedEmails, MAX_ATTEMPTS)
                
                ## EXTRACT UNIQUE EMAILS
                EmailData = mod_2.fn_ExtractUniqueEmailsFromOffice(OfficeData)
                print(f"DEBUG Office {OfficeNumber}: ContactEmails={EmailData['ContactEmails']}, CompanyEmails={EmailData['CompanyEmails']}")
                
                ## VALIDATE EMAILS AND FILTER OUT INVALID ONES
                EmailData, ValidationStats = mod_2A.fn_ValidateEmailBatch(EmailData, TableName)
                
                ## INITIALIZE OFFICE LOG DATA
                OfficeLogData = {
                    "FirmName": EmailData["OfficeInfo"].get("FirmName", ""),
                    "ContactResults": [],
                    "CompanyResults": []
                }
                
                ## COUNT TOTAL EMAILS FOR THIS OFFICE (AFTER VALIDATION FILTERING)
                TotalEmails = len(EmailData["ContactEmails"]) + len(EmailData["CompanyEmails"])
                
                ## INNER PROGRESS BAR - EMAILS
                EmailProgressBar = tqdm(total=TotalEmails, desc="  Emails", unit="email", leave=False)
                
                ## PROCESS CONTACT EMAILS
                for ContactEmail, ContactData in EmailData["ContactEmails"].items():
                    
                    ## BUILD TEMPLATE DATA
                    TemplateData = {
                        "ContactName_First": ContactData.get("ContactName_First"),
                        "ContactName_Last": ContactData.get("ContactName_Last"),
                        "Contact_TitlePosition": ContactData.get("Contact_TitlePosition"),
                        "FirmName": EmailData["OfficeInfo"].get("FirmName"),
                        "AddressOfCompany": EmailData["OfficeInfo"].get("AddressOfCompany"),
                        "City": EmailData["OfficeInfo"].get("City"),
                        "State_Province": EmailData["OfficeInfo"].get("State_Province"),
                        "PostalZipCode": EmailData["OfficeInfo"].get("PostalZipCode"),
                        "Country": EmailData["OfficeInfo"].get("Country"),
                        "NumberPhone": ContactData.get("NumberPhone"),
                        "EmailOfContact": ContactEmail,
                        "Website": EmailData["OfficeInfo"].get("Website")
                    }

                    ## BUILD EMAIL
                    EmailContent = mod_3.fn_BuildEmailTemplate("contact", TemplateData)
                    
                    ## SEND EMAIL
                    SendResult = mod_4.fn_SendEmailViaMailgun(
                        ContactEmail,
                        EmailContent["Subject"],
                        EmailContent["TextBody"],
                        MAILGUN_CONFIG
                    )
                    
                    ## UPDATE DATABASE
                    mod_5.fn_UpdateEmailStatusInDB(
                        TableName,
                        [ContactData.get("rowid")],
                        "contact",
                        SendResult
                    )
                    
                    ## GET CURRENT ATTEMPTS
                    CurrentAttempts = ContactData.get("EmailAttempts") or 0
                    NewAttempts = CurrentAttempts + 1
                    
                    ## ADD RESULT TO OFFICE LOG
                    OfficeLogData["ContactResults"].append({
                        "Email": ContactEmail,
                        "Success": SendResult["Success"],
                        "Status": SendResult["Status"],
                        "MailgunMessageID": SendResult["MailgunMessageID"],
                        "ErrorMessage": SendResult["ErrorMessage"],
                        "RowID": ContactData.get("rowid"),
                        "Attempts": NewAttempts
                    })
                    
                    ## UPDATE CAMPAIGN STATS
                    if SendResult["Success"]:
                        CampaignStats["ContactEmailsSent"] += 1
                        CampaignStats["TableStats"][TableName]["ContactEmailsSent"] += 1
                    else:
                        CampaignStats["Failures"] += 1
                        CampaignStats["TableStats"][TableName]["Failures"] += 1
                    
                    ## UPDATE INNER PROGRESS BAR
                    EmailProgressBar.update(1)
                    
                    ## CALCULATE AND APPLY EMAIL DELAY
                    DelaySeconds = mod_8.fn_CalculateEmailDelay()
                    time.sleep(DelaySeconds)
                
                ## PROCESS COMPANY EMAILS
                for CompanyEmail, CompanyData in EmailData["CompanyEmails"].items():
                    
                    ## EXTRACT ROWID AND ATTEMPTS FROM COMPANY DATA
                    RowId = CompanyData.get("rowid")
                    CurrentAttempts = CompanyData.get("EmailAttempts") or 0
                    NewAttempts = CurrentAttempts + 1
                    
                    ## BUILD TEMPLATE DATA
                    TemplateData = {
                        "FirmName": EmailData["OfficeInfo"].get("FirmName"),
                        "AddressOfCompany": EmailData["OfficeInfo"].get("AddressOfCompany"),
                        "City": EmailData["OfficeInfo"].get("City"),
                        "State_Province": EmailData["OfficeInfo"].get("State_Province"),
                        "PostalZipCode": EmailData["OfficeInfo"].get("PostalZipCode"),
                        "Country": EmailData["OfficeInfo"].get("Country"),
                        "Website": EmailData["OfficeInfo"].get("Website"),
                        "EmailOfCompany": CompanyEmail
                    }
                    
                    ## BUILD EMAIL
                    EmailContent = mod_3.fn_BuildEmailTemplate("company", TemplateData)
                    
                    ## SEND EMAIL
                    SendResult = mod_4.fn_SendEmailViaMailgun(
                        CompanyEmail,
                        EmailContent["Subject"],
                        EmailContent["TextBody"],
                        MAILGUN_CONFIG
                    )
                    
                    ## UPDATE DATABASE WITH SINGLE ROWID
                    mod_5.fn_UpdateEmailStatusInDB(
                        TableName,
                        [RowId],
                        "company",
                        SendResult
                    )
                    
                    ## ADD RESULT TO OFFICE LOG
                    OfficeLogData["CompanyResults"].append({
                        "Email": CompanyEmail,
                        "Success": SendResult["Success"],
                        "Status": SendResult["Status"],
                        "MailgunMessageID": SendResult["MailgunMessageID"],
                        "ErrorMessage": SendResult["ErrorMessage"],
                        "RowID": RowId,
                        "Attempts": NewAttempts
                    })
                    
                    ## UPDATE CAMPAIGN STATS
                    if SendResult["Success"]:
                        CampaignStats["CompanyEmailsSent"] += 1
                        CampaignStats["TableStats"][TableName]["CompanyEmailsSent"] += 1
                    else:
                        CampaignStats["Failures"] += 1
                        CampaignStats["TableStats"][TableName]["Failures"] += 1
                    
                    ## UPDATE INNER PROGRESS BAR
                    EmailProgressBar.update(1)
                    
                    ## CALCULATE AND APPLY EMAIL DELAY
                    DelaySeconds = mod_8.fn_CalculateEmailDelay()
                    time.sleep(DelaySeconds)
                
                ## CLOSE INNER PROGRESS BAR
                EmailProgressBar.close()
                
                ## WRITE OFFICE LOG
                mod_6.fn_WriteOfficeLog(TableName, OfficeNumber, OfficeLogData, LOG_DIR)
                
                ## TAKE BREAK BETWEEN OFFICES (EXCEPT FOR LAST OFFICE)
                if OfficeNumber != OfficesToProcess[-1]:
                    BreakSeconds = mod_8.fn_CalculateOfficeBreak()
                    BreakMinutes = int(BreakSeconds / 60)
                    print(f"\n  Taking {BreakMinutes} minute break before next office...")
                    
                    ## TAKE BREAK BETWEEN OFFICES (EXCEPT FOR LAST OFFICE)
                    if OfficeNumber != OfficesToProcess[-1]:
                        BreakSeconds = mod_8.fn_CalculateOfficeBreak()
                        BreakMinutes = int(BreakSeconds / 60)
                        print(f"\n  Taking {BreakMinutes} minute break before next office...")
                        for Remaining in range(int(BreakSeconds), 0, -1):
                            Minutes = Remaining // 60
                            Seconds = Remaining % 60
                            print(f"\r  Time remaining: {Minutes:02d}:{Seconds:02d}", end='', flush=True)
                            time.sleep(1)
                        print()
                
                ## INCREMENT OFFICE COUNTERS
                CampaignStats["OfficesProcessed"] += 1
                CampaignStats["TableStats"][TableName]["OfficesProcessed"] += 1
                SessionOfficeCount += 1
                
                ## CHECK IF SESSION LIMIT REACHED
                if OfficeInputType == "count":
                    if CliMode:
                        SessionLimit = MaxOffices
                    else:
                        SessionLimit = OfficeInput["value"]
                    
                    if SessionOfficeCount >= SessionLimit:
                        SessionLimitReached = True
                        print(f"\n\nSession limit reached: {SessionLimit} offices processed")
                        break
            
            ## INCREMENT TABLE COUNTER
            CampaignStats["TablesProcessed"] += 1
        
        ## CALCULATE CAMPAIGN DURATION
        CampaignStats["EndTime"] = datetime.now()
        Duration = CampaignStats["EndTime"] - CampaignStats["StartTime"]
        DurationMinutes = int(Duration.total_seconds() // 60)
        DurationSeconds = int(Duration.total_seconds() % 60)
        DurationStr = f"{DurationMinutes} minutes {DurationSeconds} seconds"
        
        ## PREPARE CAMPAIGN DATA FOR SUMMARY LOG
        CampaignData = {
            "TablesProcessed": CampaignStats["TablesProcessed"],
            "OfficesProcessed": CampaignStats["OfficesProcessed"],
            "ContactEmailsSent": CampaignStats["ContactEmailsSent"],
            "CompanyEmailsSent": CampaignStats["CompanyEmailsSent"],
            "Failures": CampaignStats["Failures"],
            "Duration": DurationStr,
            "TableStats": CampaignStats["TableStats"]
        }
        
        ## WRITE SUMMARY LOG
        mod_7.fn_WriteSummaryLog(CampaignData, LOG_DIR)
        
        ## PRINT COMPLETION MESSAGE
        print(f"\nSession complete")
        print(f"  Tables processed: {CampaignStats['TablesProcessed']}")
        print(f"  Offices processed: {CampaignStats['OfficesProcessed']}")
        print(f"  Contact emails sent: {CampaignStats['ContactEmailsSent']}")
        print(f"  Company emails sent: {CampaignStats['CompanyEmailsSent']}")
        print(f"  Failures: {CampaignStats['Failures']}")
        print(f"  Duration: {DurationStr}")
        
        ## INTERACTIVE MODE - ASK TO CONTINUE
        if not CliMode:
            ContinueProcessing = mod_00.fn_Ask2Continue()
        
        ## NOTIFY IF MORE WORK REMAINS
        if SessionLimitReached and not ContinueProcessing:
            print(f"\n  Run again to continue processing remaining offices.")

## END MAIN PROGRAM