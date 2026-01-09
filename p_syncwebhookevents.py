## SCRIPT: P_SYNCWEBHOOKEVENTS.PY
## PURPOSE: SYNC MAILGUN WEBHOOK EVENTS FROM PHP DATABASE TO LOCAL DATABASE

import os
import sqlite3
import pymysql
from datetime import datetime
from dotenv import load_dotenv
from config import TABLE_NAMES

## LOAD ENVIRONMENT VARIABLES
load_dotenv()

## WEBHOOK DATABASE CREDENTIALS (FROM .ENV FILE)
WEBHOOK_DB_CONFIG = {
    "host": os.getenv("WEBHOOK_DB_HOST"),
    "user": os.getenv("WEBHOOK_DB_USER"),
    "password": os.getenv("WEBHOOK_DB_PASSWORD"),
    "database": os.getenv("WEBHOOK_DB_NAME")
}

## LOCAL DATABASE PATH
LOCAL_DB_PATH = "data.db"

def fn_ConnectWebhookDB():
    """
    ## CONNECT TO WEBHOOK MYSQL DATABASE
    ## RETURNS: CONNECTION OBJECT
    """
    try:
        Connection = pymysql.connect(
            host=WEBHOOK_DB_CONFIG["host"],
            user=WEBHOOK_DB_CONFIG["user"],
            password=WEBHOOK_DB_CONFIG["password"],
            database=WEBHOOK_DB_CONFIG["database"],
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
        return Connection
    except pymysql.Error as Error:
        print(f"## ERROR CONNECTING TO WEBHOOK DATABASE: {Error}")
        return None

def fn_GetUnprocessedEvents(WebhookConnection):
    """
    ## GET ALL EVENTS FROM WEBHOOK DATABASE
    ## RETURNS: LIST OF EVENT DICTIONARIES
    """
    try:
        with WebhookConnection.cursor() as Cursor:
            SQL = "SELECT * FROM mailgun_events ORDER BY CreatedAt ASC"
            Cursor.execute(SQL)
            Events = Cursor.fetchall()
            return Events
    except pymysql.Error as Error:
        print(f"## ERROR FETCHING EVENTS: {Error}")
        return []

def fn_UpdateLocalDatabase(Events, TableName):
    """
    ## UPDATE LOCAL DATABASE WITH WEBHOOK EVENTS
    ## INPUT: EVENTS LIST, TABLE NAME
    ## RETURNS: STATS DICTIONARY
    """
    Stats = {
        "Accepted": 0,
        "Delivered": 0,
        "Bounced": 0,
        "Failed": 0,
        "Opened": 0,
        "Clicked": 0,
        "Complained": 0,
        "Unsubscribed": 0,
        "NotMatched": 0
    }
    
    ## CONNECT TO LOCAL DATABASE
    LocalConnection = sqlite3.connect(LOCAL_DB_PATH)
    LocalCursor = LocalConnection.cursor()
    
    for Event in Events:
        MailgunMessageID = Event.get("MailgunMessageID")
        EventType = Event.get("EventType")
        EventTimestamp = Event.get("EventTimestamp")
        
        if not MailgunMessageID:
            Stats["NotMatched"] += 1
            continue
        
        ## FIND MATCHING RECORD IN LOCAL DATABASE
        LocalCursor.execute(
            f"SELECT rowid FROM {TableName} WHERE MailgunMessageID = ?",
            (MailgunMessageID,)
        )
        Result = LocalCursor.fetchone()
        
        if not Result:
            Stats["NotMatched"] += 1
            continue
        
        RowID = Result[0]
        
        ## UPDATE BASED ON EVENT TYPE (OVERWRITE EMAILSTATUS WITH WEBHOOK DATA)
        if EventType == "accepted":
            LocalCursor.execute(
                f"UPDATE {TableName} SET EmailAcceptedDateTime = ?, EmailStatus = ? WHERE rowid = ?",
                (str(EventTimestamp), EventType, RowID)
            )
            Stats["Accepted"] += 1
        
        elif EventType == "delivered":
            LocalCursor.execute(
                f"UPDATE {TableName} SET EmailDelivered = 1, EmailDeliveredDateTime = ?, EmailStatus = ? WHERE rowid = ?",
                (str(EventTimestamp), EventType, RowID)
            )
            Stats["Delivered"] += 1
        
        elif EventType == "opened":
            LocalCursor.execute(
                f"UPDATE {TableName} SET EmailOpened = 1, EmailStatus = ? WHERE rowid = ?",
                (EventType, RowID)
            )
            Stats["Opened"] += 1
        
        elif EventType == "clicked":
            LocalCursor.execute(
                f"UPDATE {TableName} SET EmailClicked = 1, EmailStatus = ? WHERE rowid = ?",
                (EventType, RowID)
            )
            Stats["Clicked"] += 1
        
        elif EventType == "failed":
            LocalCursor.execute(
                f"UPDATE {TableName} SET EmailBounced = 1, EmailStatus = ? WHERE rowid = ?",
                (EventType, RowID)
            )
            Stats["Failed"] += 1
        
        elif EventType == "bounced":
            LocalCursor.execute(
                f"UPDATE {TableName} SET EmailBounced = 1, EmailStatus = ? WHERE rowid = ?",
                (EventType, RowID)
            )
            Stats["Bounced"] += 1
        
        elif EventType == "complained":
            LocalCursor.execute(
                f"UPDATE {TableName} SET EmailComplained = 1, EmailStatus = ? WHERE rowid = ?",
                (EventType, RowID)
            )
            Stats["Complained"] += 1
        
        elif EventType == "unsubscribed":
            LocalCursor.execute(
                f"UPDATE {TableName} SET EmailUnsubscribed = 1, EmailStatus = ? WHERE rowid = ?",
                (EventType, RowID)
            )
            Stats["Unsubscribed"] += 1
    
    ## COMMIT CHANGES
    LocalConnection.commit()
    LocalConnection.close()
    
    return Stats

def fn_DisplayTableMenu():
    """
    ## DISPLAY NUMBERED LIST OF AVAILABLE TABLES
    """
    print("\n" + "="*50)
    print("AVAILABLE TABLES:")
    print("="*50)
    for Index, TableName in enumerate(TABLE_NAMES, start=1):
        print(f"  {Index}. {TableName}")
    print("="*50)

def fn_GetTableSelection():
    """
    ## PROMPT USER TO SELECT A TABLE BY NUMBER
    ## RETURNS: SELECTED TABLE NAME OR NONE IF INVALID
    """
    while True:
        try:
            fn_DisplayTableMenu()
            Choice = input("\nSELECT TABLE NUMBER TO SYNC (OR 'Q' TO QUIT): ").strip().upper()
            
            if Choice == 'Q':
                return None
            
            Choice = int(Choice)
            
            if 1 <= Choice <= len(TABLE_NAMES):
                SelectedTable = TABLE_NAMES[Choice - 1]
                print(f"\nSELECTED: {SelectedTable}")
                return SelectedTable
            else:
                print(f"\nINVALID CHOICE. PLEASE SELECT 1-{len(TABLE_NAMES)}")
        
        except ValueError:
            print("\nINVALID INPUT. PLEASE ENTER A NUMBER.")

## MAIN SCRIPT
if __name__ == "__main__":
    
    print("="*50)
    print("WEBHOOK EVENT SYNC UTILITY")
    print("="*50)
    
    ## GET TABLE SELECTION
    SelectedTable = fn_GetTableSelection()
    
    if SelectedTable is None:
        print("\nEXITING PROGRAM.")
        exit()
    
    ## CONNECT TO WEBHOOK DATABASE
    print("\n## CONNECTING TO WEBHOOK DATABASE...")
    WebhookConnection = fn_ConnectWebhookDB()
    
    if not WebhookConnection:
        print("## FAILED TO CONNECT TO WEBHOOK DATABASE")
        exit()
    
    print("## CONNECTED SUCCESSFULLY")
    
    ## GET UNPROCESSED EVENTS
    print("## FETCHING WEBHOOK EVENTS...")
    Events = fn_GetUnprocessedEvents(WebhookConnection)
    
    if not Events:
        print("## NO EVENTS FOUND")
        WebhookConnection.close()
        exit()
    
    print(f"## FOUND {len(Events)} EVENTS")
    
    ## UPDATE LOCAL DATABASE
    print(f"## SYNCING EVENTS TO TABLE: {SelectedTable}...")
    Stats = fn_UpdateLocalDatabase(Events, SelectedTable)
    
    ## CLOSE WEBHOOK CONNECTION
    WebhookConnection.close()
    
    ## DISPLAY RESULTS
    print("\n" + "="*50)
    print("SYNC COMPLETE")
    print("="*50)
    print(f"  Accepted: {Stats['Accepted']}")
    print(f"  Delivered: {Stats['Delivered']}")
    print(f"  Bounced: {Stats['Bounced']}")
    print(f"  Failed: {Stats['Failed']}")
    print(f"  Opened: {Stats['Opened']}")
    print(f"  Clicked: {Stats['Clicked']}")
    print(f"  Complained: {Stats['Complained']}")
    print(f"  Unsubscribed: {Stats['Unsubscribed']}")
    print(f"  Not Matched: {Stats['NotMatched']}")
    print("="*50)