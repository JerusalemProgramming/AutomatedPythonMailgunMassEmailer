## MODULE: MOD_1_QUERYOFFICEDATAINDB.PY
## PURPOSE: GET ALL CONTACT ROWS FOR SPECIFIC OFFICE

import sqlite3
from config import DB_PATH

def fn_QueryOfficeDataInDB(TableName, OfficeNumber, IncludeFailedEmails, MaxAttempts):
    """
    ## QUERY ALL ROWS FOR A SPECIFIC OFFICE BASED ON EMAIL STATUS FILTERS
    ## INPUT: TABLENAME (STRING), OFFICENUMBER (STRING), INCLUDEFAILEDEMAILS (BOOLEAN), MAXATTEMPTS (INTEGER)
    ## OUTPUT: LIST OF DICTIONARIES (ONE PER CONTACT ROW)
    """
    
    ## INITIALIZE EMPTY LIST FOR RESULTS
    OfficeData = []
    
    ## DEFINE COLUMNS TO SELECT
    Columns = [
        "OfficeNumber",
        "FirmName",
        "AddressOfCompany",
        "City",
        "State_Province",
        "PostalZipCode",
        "Website",
        "EmailOfCompany",
        "ContactName_First",
        "ContactName_Last",
        "Contact_TitlePosition",
        "NumberPhone",
        "EmailOfContact",
        "rowid",
        "EmailAttempts"
    ]
    
    ColumnString = ", ".join(Columns)
    
    ## BUILD SQL QUERY BASED ON INCLUDEFAILEDEMAILS FLAG
    if IncludeFailedEmails:
        ## INCLUDE FAILED, REJECTED, BOUNCED, AND NULL STATUS EMAILS UNDER MAX ATTEMPTS
        SqlQuery = f"""
            SELECT {ColumnString}
            FROM {TableName}
            WHERE OfficeNumber = ?
            AND (
                (EmailStatus IS NULL AND (EmailSent IS NULL OR EmailSent = 0))
                OR EmailStatus = 'failed' 
                OR EmailStatus = 'rejected'
                OR EmailBounced = 1
            )
            AND (EmailUnsubscribed IS NULL OR EmailUnsubscribed = 0)
            AND (EmailAttempts IS NULL OR EmailAttempts < ?)
        """
        QueryParams = (OfficeNumber, MaxAttempts)
    else:
        ## ONLY INCLUDE NULL STATUS EMAILS (INITIAL SEND)
        SqlQuery = f"""
            SELECT {ColumnString}
            FROM {TableName}
            WHERE OfficeNumber = ?
            AND EmailStatus IS NULL
            AND (EmailSent IS NULL OR EmailSent = 0)
            AND (EmailUnsubscribed IS NULL OR EmailUnsubscribed = 0)
        """
        QueryParams = (OfficeNumber,)
    
    ## CONNECT TO DATABASE AND EXECUTE QUERY
    try:
        Connection = sqlite3.connect(DB_PATH)
        Connection.row_factory = sqlite3.Row
        Cursor = Connection.cursor()
        Cursor.execute(SqlQuery, QueryParams)
        
        ## FETCH ALL RESULTS AND CONVERT TO LIST OF DICTIONARIES
        Results = Cursor.fetchall()
        OfficeData = [dict(Row) for Row in Results]
        
        Connection.close()
        
    except sqlite3.Error as E:
        ## LOG DATABASE ERROR
        print(f"## DATABASE ERROR: {E}")
    
    return OfficeData