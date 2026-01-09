## MODULE: MOD_7_WRITESUMMARYLOG.PY
## PURPOSE: WRITE OVERALL CAMPAIGN SUMMARY LOG (TXT + CSV)

import os
from datetime import datetime

def fn_WriteSummaryLog(CampaignData, LogDir):
    """
    ## WRITE OVERALL CAMPAIGN SUMMARY LOG (TXT AND CSV)
    ## INPUT: CAMPAIGNDATA (DICT WITH AGGREGATED STATS), LOGDIR (STRING)
    ## OUTPUT: DICTIONARY WITH TXTLOGPATH AND CSVLOGPATH
    """
    
    ## INITIALIZE OUTPUT
    Result = {
        "TxtLogPath": "",
        "CsvLogPath": ""
    }
    
    ## CREATE TIMESTAMP FOR FILENAMES
    Timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    ## ENSURE LOG DIRECTORY EXISTS
    os.makedirs(LogDir, exist_ok=True)
    
    ## BUILD FILE PATHS
    TxtLogPath = os.path.join(LogDir, f"summary_{Timestamp}.log")
    CsvLogPath = os.path.join(LogDir, f"summary_{Timestamp}.csv")
    
    ## EXTRACT CAMPAIGN DATA
    TableStats = CampaignData.get("TableStats", {})
    TablesProcessed = CampaignData.get("TablesProcessed", 0)
    TotalOfficesProcessed = CampaignData.get("OfficesProcessed", 0)
    TotalContactEmailsSent = CampaignData.get("ContactEmailsSent", 0)
    TotalCompanyEmailsSent = CampaignData.get("CompanyEmailsSent", 0)
    TotalFailures = CampaignData.get("Failures", 0)
    Duration = CampaignData.get("Duration", "")
    
    ## WRITE TXT LOG
    try:
        with open(TxtLogPath, "w", encoding="utf-8") as TxtFile:
            TxtFile.write(f"EMAIL CAMPAIGN SUMMARY - {Timestamp}\n")
            TxtFile.write("=" * 44 + "\n\n")
            
            ## WRITE STATS FOR EACH TABLE
            for TableName, Stats in TableStats.items():
                TxtFile.write(f"TABLE: {TableName}\n")
                TxtFile.write(f"  - Offices processed: {Stats.get('OfficesProcessed', 0)}\n")
                TxtFile.write(f"  - Contact emails sent: {Stats.get('ContactEmailsSent', 0)}\n")
                TxtFile.write(f"  - Company emails sent: {Stats.get('CompanyEmailsSent', 0)}\n")
                TxtFile.write(f"  - Failures: {Stats.get('Failures', 0)}\n\n")
            
            ## WRITE OVERALL TOTALS
            TxtFile.write("OVERALL TOTALS:\n")
            TxtFile.write(f"  - Tables processed: {TablesProcessed}\n")
            TxtFile.write(f"  - Offices processed: {TotalOfficesProcessed}\n")
            TxtFile.write(f"  - Contact emails sent: {TotalContactEmailsSent}\n")
            TxtFile.write(f"  - Company emails sent: {TotalCompanyEmailsSent}\n")
            TxtFile.write(f"  - Failures: {TotalFailures}\n")
            TxtFile.write(f"  - Duration: {Duration}\n")
        
        Result["TxtLogPath"] = TxtLogPath
        
    except Exception as E:
        print(f"## ERROR WRITING TXT SUMMARY LOG: {E}")
    
    ## WRITE CSV LOG
    try:
        with open(CsvLogPath, "w", encoding="utf-8") as CsvFile:
            ## WRITE HEADER (SEMICOLON DELIMITER)
            CsvFile.write("Table;OfficesProcessed;ContactEmailsSent;CompanyEmailsSent;Failures;SuccessRate\n")
            
            ## WRITE ROW FOR EACH TABLE
            for TableName, Stats in TableStats.items():
                OfficesProcessed = Stats.get("OfficesProcessed", 0)
                ContactEmailsSent = Stats.get("ContactEmailsSent", 0)
                CompanyEmailsSent = Stats.get("CompanyEmailsSent", 0)
                Failures = Stats.get("Failures", 0)
                
                ## CALCULATE SUCCESS RATE
                TotalAttempts = ContactEmailsSent + CompanyEmailsSent + Failures
                if TotalAttempts > 0:
                    SuccessRate = ((ContactEmailsSent + CompanyEmailsSent) / TotalAttempts) * 100
                    SuccessRateStr = f"{SuccessRate:.1f}%"
                else:
                    SuccessRateStr = "N/A"
                
                CsvFile.write(f"{TableName};{OfficesProcessed};{ContactEmailsSent};{CompanyEmailsSent};{Failures};{SuccessRateStr}\n")
            
            ## WRITE TOTAL ROW
            TotalAttempts = TotalContactEmailsSent + TotalCompanyEmailsSent + TotalFailures
            if TotalAttempts > 0:
                TotalSuccessRate = ((TotalContactEmailsSent + TotalCompanyEmailsSent) / TotalAttempts) * 100
                TotalSuccessRateStr = f"{TotalSuccessRate:.1f}%"
            else:
                TotalSuccessRateStr = "N/A"
            
            CsvFile.write(f"TOTAL;{TotalOfficesProcessed};{TotalContactEmailsSent};{TotalCompanyEmailsSent};{TotalFailures};{TotalSuccessRateStr}\n")

        Result["CsvLogPath"] = CsvLogPath
        
    except Exception as E:
        print(f"## ERROR WRITING CSV SUMMARY LOG: {E}")
    
    return Result
