## MODULE: MOD_5_UPDATEEMAILSTATUSINDB.PY
## PURPOSE: UPDATE DB WITH EMAIL SEND RESULTS

import sqlite3
from datetime import datetime
from config import DB_PATH

def fn_UpdateEmailStatusInDB(TableName, RowIDs, EmailType, StatusData):
    """
    ## UPDATE DATABASE WITH EMAIL SEND RESULTS
    ## INPUT: TABLENAME (STRING), ROWIDS (LIST), EMAILTYPE ("contact" OR "company"), STATUSDATA (DICT)
    ## OUTPUT: SUCCESS BOOLEAN
    """
    
    ## GET CURRENT TIMESTAMP IN ISO FORMAT
    CurrentTimestamp = datetime.now().isoformat()
    
    ## EXTRACT STATUS DATA
    Success = StatusData.get("Success", False)
    MailgunMessageID = StatusData.get("MailgunMessageID")
    Status = StatusData.get("Status", "failed")
    ErrorMessage = StatusData.get("ErrorMessage")
    
    ## DETERMINE FAILURE SEVERITY BASED ON ERROR TYPE
    FailureSeverity = None
    if not Success and ErrorMessage:
        ## PERMANENT FAILURES: INVALID EMAIL, REJECTED, ETC.
        PermanentErrors = ["rejected", "invalid", "not found", "does not exist"]
        if any(Err in ErrorMessage.lower() for Err in PermanentErrors) or Status == "rejected":
            FailureSeverity = "permanent"
        else:
            FailureSeverity = "temporary"
    
    try:
        Connection = sqlite3.connect(DB_PATH)
        Cursor = Connection.cursor()
        
        ## UPDATE EACH ROWID
        for RowId in RowIDs:
            
            ## GET CURRENT EMAIL ATTEMPTS (OR 0 IF NULL)
            Cursor.execute(f"SELECT EmailAttempts FROM {TableName} WHERE rowid = ?", (RowId,))
            Row = Cursor.fetchone()
            CurrentAttempts = Row[0] if Row and Row[0] is not None else 0
            NewAttempts = CurrentAttempts + 1
            
            if Success:
                ## SUCCESS - EMAIL ACCEPTED
                if EmailType == "contact":
                    SqlUpdate = f"""
                        UPDATE {TableName}
                        SET EmailAttempts = ?,
                            EmailSentDateTime = ?,
                            EmailStatus = ?,
                            EmailSent = 1,
                            MailgunMessageID = ?,
                            EmailSentToContact = 1
                        WHERE rowid = ?
                    """
                    Cursor.execute(SqlUpdate, (NewAttempts, CurrentTimestamp, Status, MailgunMessageID, RowId))
                else:
                    ## COMPANY EMAIL
                    SqlUpdate = f"""
                        UPDATE {TableName}
                        SET EmailAttempts = ?,
                            EmailSentDateTime = ?,
                            EmailStatus = ?,
                            EmailSent = 1,
                            MailgunMessageID = ?,
                            EmailSentToCompany = 1
                        WHERE rowid = ?
                    """
                    Cursor.execute(SqlUpdate, (NewAttempts, CurrentTimestamp, Status, MailgunMessageID, RowId))
            else:
                ## FAILURE - EMAIL FAILED OR REJECTED
                SqlUpdate = f"""
                    UPDATE {TableName}
                    SET EmailAttempts = ?,
                        EmailSentDateTime = ?,
                        EmailStatus = ?,
                        EmailSent = 0,
                        EmailFailureReason = ?,
                        EmailFailureSeverity = ?
                    WHERE rowid = ?
                """
                Cursor.execute(SqlUpdate, (NewAttempts, CurrentTimestamp, Status, ErrorMessage, FailureSeverity, RowId))
        
        Connection.commit()
        Connection.close()
        return True
        
    except sqlite3.Error as E:
        print(f"## DATABASE ERROR: {E}")
        return False
    except Exception as E:
        print(f"## UNEXPECTED ERROR: {E}")
        return False