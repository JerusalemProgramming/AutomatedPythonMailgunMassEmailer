## IMPORT MODULES
import sqlite3

## BEGIN DEFINE FUNCTION
def fn_NormalizeDataWebsitesInDB(DbPath="data.db"):

    # NORMALIZE WEBSITE COLUMN ACROSS ALL TABLES
    
    ## CONNECT TO DATABASE
    Connection = sqlite3.connect(DbPath)
    Cursor = Connection.cursor()
    
    ## GET ALL TABLE NAMES
    Cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    Tables = Cursor.fetchall()
    
    TotalUpdated = 0
    
    ## LOOP THROUGH EACH TABLE
    for TableTuple in Tables:
        TableName = TableTuple[0]
        
        ## CHECK IF TABLE HAS WEBSITE COLUMN
        Cursor.execute(f"PRAGMA table_info({TableName})")
        Columns = [col[1] for col in Cursor.fetchall()]
        
        if "Website" not in Columns:
            print(f"DEBUG: {TableName} - No Website column")
            continue
        else:
            print(f"DEBUG: {TableName} - Has Website column")
        
        ## GET ALL ROWS WITH WEBSITE
        Cursor.execute(f"SELECT rowid, Website FROM {TableName} WHERE Website IS NOT NULL AND Website != ''")
        Rows = Cursor.fetchall()
        print(f"DEBUG: {TableName} - Found {len(Rows)} websites")
        
        ## NORMALIZE EACH WEBSITE
        for RowID, Website in Rows:
            OriginalWebsite = Website
            NormalizedWebsite = Website.strip()
            
            ## REMOVE HTTP://
            if NormalizedWebsite.lower().startswith("http://"):
                NormalizedWebsite = NormalizedWebsite[7:]
            
            ## REMOVE HTTPS://
            if NormalizedWebsite.lower().startswith("https://"):
                NormalizedWebsite = NormalizedWebsite[8:]
            
            ## REMOVE WWW.
            if NormalizedWebsite.lower().startswith("www."):
                NormalizedWebsite = NormalizedWebsite[4:]
            
            ## REMOVE FIRST TRAILING SLASH AND EVERYTHING AFTER
            SlashIndex = NormalizedWebsite.find("/")
            if SlashIndex != -1:
                NormalizedWebsite = NormalizedWebsite[:SlashIndex]
            
            ## UPDATE IF CHANGED
            if NormalizedWebsite != OriginalWebsite:
                Cursor.execute(f"UPDATE {TableName} SET Website = ? WHERE rowid = ?", (NormalizedWebsite, RowID))
                TotalUpdated += 1
    
    ## COMMIT AND CLOSE
    Connection.commit()
    Connection.close()
    
    ## RETURN RESULT
    return f"Website normalization complete: {TotalUpdated} records updated across all tables"
## END DEFINE FUNCTION

## TESTING
if __name__ == "__main__":
    
    # TEST THE NORMALIZATION
    print(fn_NormalizeDataWebsitesInDB("data.db"))