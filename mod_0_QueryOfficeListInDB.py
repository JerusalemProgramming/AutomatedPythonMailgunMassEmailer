## MODULE: MOD_0_QUERYOFFICELISTINDB.PY
## PURPOSE: GET LIST OF OFFICES WITH PENDING/FAILED EMAILS TO PROCESS

import sqlite3
from config import DB_PATH

def fn_QueryOfficeListInDB(TableName, IncludeFailedEmails, MaxAttempts):
    """
    ## QUERY DISTINCT OFFICENUMBERS FROM TABLE BASED ON EMAIL STATUS FILTERS
    ## INPUT: TABLENAME (STRING), INCLUDEFAILEDEMAILS (BOOLEAN), MAXATTEMPTS (INTEGER)
    ## OUTPUT: LIST OF OFFICENUMBER STRINGS
    """
    
    ## INITIALIZE EMPTY LIST FOR RESULTS
    OfficeList = []
    
    ## BUILD SQL QUERY BASED ON INCLUDEFAILEDEMAILS FLAG
    if IncludeFailedEmails:
        ## INCLUDE FAILED, REJECTED, BOUNCED, AND NULL STATUS EMAILS UNDER MAX ATTEMPTS
        SqlQuery = f"""
            SELECT DISTINCT OfficeNumber 
            FROM {TableName}
            WHERE (
                (EmailStatus IS NULL AND (EmailSent IS NULL OR EmailSent = 0))
                OR EmailStatus = 'failed' 
                OR EmailStatus = 'rejected'
                OR EmailBounced = 1
            )
            AND (EmailUnsubscribed IS NULL OR EmailUnsubscribed = 0)
            AND (EmailAttempts IS NULL OR EmailAttempts < ?)
            ORDER BY CAST(OfficeNumber AS INTEGER)
        """
        QueryParams = (MaxAttempts,)
    else:
        ## ONLY INCLUDE NULL STATUS EMAILS (INITIAL SEND)
        SqlQuery = f"""
            SELECT DISTINCT OfficeNumber 
            FROM {TableName}
            WHERE EmailStatus IS NULL
            AND (EmailSent IS NULL OR EmailSent = 0)
            AND (EmailUnsubscribed IS NULL OR EmailUnsubscribed = 0)
            ORDER BY CAST(OfficeNumber AS INTEGER)
        """
        QueryParams = ()
    
    ## CONNECT TO DATABASE AND EXECUTE QUERY
    try:
        Connection = sqlite3.connect(DB_PATH)
        Cursor = Connection.cursor()
        Cursor.execute(SqlQuery, QueryParams)
        
        ## FETCH ALL RESULTS AND EXTRACT OFFICENUMBER STRINGS
        Results = Cursor.fetchall()
        OfficeList = [Row[0] for Row in Results]
        
        Connection.close()
        
    except sqlite3.Error as E:
        ## LOG DATABASE ERROR
        print(f"## DATABASE ERROR: {E}")
    
    return OfficeList