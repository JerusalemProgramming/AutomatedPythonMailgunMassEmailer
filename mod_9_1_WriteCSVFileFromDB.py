## IMPORT MODULES
import sqlite3
import csv
import os

## DECLARE VARIABLES
DBPath = "data.db"

## BEGIN DEFINE FUNCTION
def fn_WriteCSVFileFromDB(TableName, OutputFilePath):
    ## EXPORT SINGLE TABLE FROM DB TO CSV FILE
    
    ## CREATE OUTPUT DIRECTORY IF NOT EXISTS
    OutputDir = os.path.dirname(OutputFilePath)
    if OutputDir and not os.path.exists(OutputDir):
        os.makedirs(OutputDir)
    
    ## CONNECT TO DATABASE
    Connection = sqlite3.connect(DBPath)
    Cursor = Connection.cursor()
    
    ## GET ALL DATA FROM TABLE
    Cursor.execute(f"SELECT * FROM {TableName}")
    Rows = Cursor.fetchall()
    
    ## GET COLUMN NAMES
    ColumnNames = [Description[0] for Description in Cursor.description]
    
    ## CLOSE CONNECTION
    Connection.close()
    
    ## WRITE TO CSV
    with open(OutputFilePath, 'w', newline='', encoding='utf-8') as CsvFile:
        Writer = csv.writer(CsvFile, delimiter=';')
        
        ## WRITE HEADER
        Writer.writerow(ColumnNames)
        
        ## WRITE DATA ROWS
        Writer.writerows(Rows)
    
    ## RETURN RESULT
    return f"Exported {len(Rows)} rows to {OutputFilePath}"
## END DEFINE FUNCTION