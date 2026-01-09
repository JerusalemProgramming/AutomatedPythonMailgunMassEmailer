## MODULE: P_SYNCUNSUBSCRIBES.PY
## PURPOSE: SYNC UNSUBSCRIBES FROM REMOTE DATABASE TO LOCAL DATABASE AND MAILGUN SUPPRESSION LIST

import os
import sqlite3
import pymysql
import requests
from dotenv import load_dotenv
from config import TABLE_NAMES

## LOAD ENVIRONMENT VARIABLES
load_dotenv()

## UNSUBSCRIBE DATABASE CREDENTIALS (FROM .ENV FILE)
UNSUB_DB_CONFIG = {
    "host": os.getenv("UNSUB_DB_HOST"),
    "user": os.getenv("UNSUB_DB_USER"),
    "password": os.getenv("UNSUB_DB_PASSWORD"),
    "database": os.getenv("UNSUB_DB_NAME")
}

## LOCAL DATABASE PATH
LOCAL_DB_PATH = "data.db"

## MAILGUN API CREDENTIALS (FROM .ENV FILE)
MAILGUN_API_KEY = os.getenv("MAILGUN_API_KEY")
MAILGUN_DOMAIN = os.getenv("MAILGUN_DOMAIN")

def fn_ConnectUnsubDB():
    """
    ## CONNECT TO UNSUBSCRIBE MYSQL DATABASE
    ## RETURNS: CONNECTION OBJECT
    """
    try:
        Connection = pymysql.connect(
            host=UNSUB_DB_CONFIG["host"],
            user=UNSUB_DB_CONFIG["user"],
            password=UNSUB_DB_CONFIG["password"],
            database=UNSUB_DB_CONFIG["database"],
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
        return Connection
    except pymysql.Error as Error:
        print(f"## ERROR CONNECTING TO UNSUBSCRIBE DATABASE: {Error}")
        return None

def fn_GetUnsubscribedEmails(UnsubConnection):
    """
    ## GET ALL UNSUBSCRIBED EMAIL ADDRESSES FROM REMOTE DATABASE
    ## RETURNS: LIST OF EMAIL ADDRESSES
    """
    try:
        with UnsubConnection.cursor() as Cursor:
            SQL = "SELECT Email FROM Unsubscribes"
            Cursor.execute(SQL)
            Results = Cursor.fetchall()
            EmailList = [Row["Email"] for Row in Results]
            return EmailList
    except pymysql.Error as Error:
        print(f"## ERROR FETCHING UNSUBSCRIBED EMAILS: {Error}")
        return []

def fn_UpdateLocalDatabase(EmailList):
    """
    ## UPDATE LOCAL DATABASE TO MARK EMAILS AS UNSUBSCRIBED
    ## INPUT: EMAIL LIST
    ## RETURNS: STATS DICTIONARY
    """
    Stats = {
        "TotalEmailsProcessed": len(EmailList),
        "TotalRowsUpdated": 0,
        "PerTableResults": {}
    }
    
    if not EmailList:
        return Stats
    
    try:
        Connection = sqlite3.connect(LOCAL_DB_PATH)
        Cursor = Connection.cursor()
        
        ## PROCESS EACH TABLE
        for TableName in TABLE_NAMES:
            TableRowsUpdated = 0
            
            ## CHECK IF TABLE EXISTS
            Cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name=?", (TableName,))
            if not Cursor.fetchone():
                continue
            
            ## UPDATE EACH EMAIL ADDRESS
            for Email in EmailList:
                ## UPDATE ROWS WHERE EMAILOFCONTACT OR EMAILOFCOMPANY MATCHES
                SqlUpdate = f"""
                    UPDATE {TableName}
                    SET EmailUnsubscribed = 1,
                        EmailStatus = 'unsubscribed'
                    WHERE LOWER(EmailOfContact) = LOWER(?) OR LOWER(EmailOfCompany) = LOWER(?)
                """
                Cursor.execute(SqlUpdate, (Email, Email))
                TableRowsUpdated += Cursor.rowcount
            
            ## STORE PER-TABLE RESULTS
            Stats["PerTableResults"][TableName] = TableRowsUpdated
            Stats["TotalRowsUpdated"] += TableRowsUpdated
        
        Connection.commit()
        Connection.close()
        
    except sqlite3.Error as Error:
        print(f"## DATABASE ERROR: {Error}")
    
    return Stats

def fn_CheckMailgunUnsubscribe(Email):
    """
    ## CHECK IF EMAIL EXISTS IN MAILGUN SUPPRESSION LIST
    ## INPUT: EMAIL ADDRESS
    ## RETURNS: TRUE IF EXISTS, FALSE OTHERWISE
    """
    if not MAILGUN_API_KEY or not MAILGUN_DOMAIN:
        return False
    
    Url = f"https://api.mailgun.net/v3/{MAILGUN_DOMAIN}/unsubscribes/{Email}"
    
    try:
        Response = requests.get(
            Url,
            auth=("api", MAILGUN_API_KEY)
        )
        
        ## 200 = EXISTS, 404 = DOES NOT EXIST
        return Response.status_code == 200
        
    except requests.RequestException as Error:
        print(f"## ERROR CHECKING {Email} IN MAILGUN: {Error}")
        return False

def fn_AddToMailgunSuppressionList(EmailList):
    """
    ## ADD EMAIL ADDRESSES TO MAILGUN SUPPRESSION LIST VIA API
    ## INPUT: EMAIL LIST
    ## RETURNS: STATS DICTIONARY
    """
    Stats = {
        "TotalEmailsProcessed": len(EmailList),
        "SuccessfullyAdded": 0,
        "AlreadyExists": 0,
        "Failed": 0
    }
    
    if not EmailList or not MAILGUN_API_KEY or not MAILGUN_DOMAIN:
        print("## MAILGUN API CREDENTIALS MISSING")
        return Stats
    
    ## MAILGUN API ENDPOINT
    Url = f"https://api.mailgun.net/v3/{MAILGUN_DOMAIN}/unsubscribes"
    
    for Email in EmailList:
        ## CHECK IF EMAIL ALREADY EXISTS
        if fn_CheckMailgunUnsubscribe(Email):
            Stats["AlreadyExists"] += 1
            continue
        
        ## ADD EMAIL TO SUPPRESSION LIST
        try:
            Response = requests.post(
                Url,
                auth=("api", MAILGUN_API_KEY),
                data={"address": Email, "tag": "*"}
            )
            
            if Response.status_code == 200:
                Stats["SuccessfullyAdded"] += 1
            else:
                Stats["Failed"] += 1
                print(f"## FAILED TO ADD {Email}: {Response.status_code} - {Response.text}")
        
        except requests.RequestException as Error:
            Stats["Failed"] += 1
            print(f"## ERROR ADDING {Email} TO MAILGUN: {Error}")
    
    return Stats

## MAIN FUNCTION
def fn_SyncUnsubscribes():
    """
    ## MAIN SYNC FUNCTION
    ## ORCHESTRATES THE ENTIRE SYNC PROCESS
    """
    print("="*60)
    print("UNSUBSCRIBE SYNC UTILITY")
    print("="*60)
    
    ## STEP 1: CONNECT TO REMOTE UNSUBSCRIBE DATABASE
    print("\n## STEP 1: CONNECTING TO REMOTE UNSUBSCRIBE DATABASE...")
    UnsubConnection = fn_ConnectUnsubDB()
    
    if not UnsubConnection:
        print("## FAILED TO CONNECT TO UNSUBSCRIBE DATABASE")
        return
    
    print("## CONNECTED SUCCESSFULLY")
    
    ## STEP 2: GET UNSUBSCRIBED EMAILS
    print("\n## STEP 2: FETCHING UNSUBSCRIBED EMAILS...")
    EmailList = fn_GetUnsubscribedEmails(UnsubConnection)
    UnsubConnection.close()
    
    if not EmailList:
        print("## NO UNSUBSCRIBED EMAILS FOUND")
        return
    
    print(f"## FOUND {len(EmailList)} UNSUBSCRIBED EMAILS")
    
    ## STEP 3: UPDATE LOCAL DATABASE
    print("\n## STEP 3: UPDATING LOCAL DATABASE...")
    LocalStats = fn_UpdateLocalDatabase(EmailList)
    
    print(f"## LOCAL DATABASE UPDATED: {LocalStats['TotalRowsUpdated']} ROWS ACROSS ALL TABLES")
    
    ## STEP 4: ADD TO MAILGUN SUPPRESSION LIST
    print("\n## STEP 4: ADDING TO MAILGUN SUPPRESSION LIST...")
    MailgunStats = fn_AddToMailgunSuppressionList(EmailList)
    
    ## DISPLAY RESULTS
    print("\n" + "="*60)
    print("SYNC COMPLETE")
    print("="*60)
    print(f"\nLOCAL DATABASE:")
    print(f"  Total emails processed: {LocalStats['TotalEmailsProcessed']}")
    print(f"  Total rows updated: {LocalStats['TotalRowsUpdated']}")
    print(f"\n  Per-table breakdown:")
    for TableName, Count in LocalStats["PerTableResults"].items():
        if Count > 0:
            print(f"    {TableName}: {Count} rows")
    
    print(f"\nMAILGUN SUPPRESSION LIST:")
    print(f"  Total emails processed: {MailgunStats['TotalEmailsProcessed']}")
    print(f"  Successfully added: {MailgunStats['SuccessfullyAdded']}")
    print(f"  Already exists: {MailgunStats['AlreadyExists']}")
    print(f"  Failed: {MailgunStats['Failed']}")
    print("="*60)

## RUN AS STANDALONE SCRIPT
if __name__ == "__main__":
    fn_SyncUnsubscribes()