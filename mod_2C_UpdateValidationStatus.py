## MODULE: MOD_2C_UPDATEVALIDATIONSTATUS.PY
## PURPOSE: UPDATE DB WITH EMAIL VALIDATION RESULTS

import sqlite3
from datetime import datetime
from config import DB_PATH

def fn_UpdateValidationStatus(TableName, RowID, ValidationData):
    """
    ## UPDATE DATABASE WITH EMAIL VALIDATION RESULTS
    ## INPUT: TABLENAME (STRING), ROWID (INTEGER), VALIDATIONDATA (DICT)
    ## OUTPUT: SUCCESS BOOLEAN
    """
    
    try:
        Connection = sqlite3.connect(DB_PATH)
        Cursor = Connection.cursor()
        
        ## EXTRACT VALIDATION DATA FROM DICTIONARY
        ValidationSyntax = ValidationData.get("ValidationSyntax")
        ValidationDomainExists = ValidationData.get("ValidationDomainExists")
        ValidationMxRecords = ValidationData.get("ValidationMxRecords")
        ValidationMailboxExists = ValidationData.get("ValidationMailboxExists")
        ValidationIsDisposable = ValidationData.get("ValidationIsDisposable")
        ValidationIsRoleBased = ValidationData.get("ValidationIsRoleBased")
        ValidationScore = ValidationData.get("ValidationScore")
        ValidationStatus = ValidationData.get("ValidationStatus")
        ValidationDateTime = ValidationData.get("ValidationDateTime")
        ValidationAttempts = ValidationData.get("ValidationAttempts")
        ValidationErrorMessage = ValidationData.get("ValidationErrorMessage")
        
        ## UPDATE DATABASE RECORD
        SqlUpdate = f"""
            UPDATE {TableName}
            SET ValidationSyntax = ?,
                ValidationDomainExists = ?,
                ValidationMxRecords = ?,
                ValidationMailboxExists = ?,
                ValidationIsDisposable = ?,
                ValidationIsRoleBased = ?,
                ValidationScore = ?,
                ValidationStatus = ?,
                ValidationDateTime = ?,
                ValidationAttempts = ?,
                ValidationErrorMessage = ?
            WHERE rowid = ?
        """
        
        Cursor.execute(SqlUpdate, (
            ValidationSyntax,
            ValidationDomainExists,
            ValidationMxRecords,
            ValidationMailboxExists,
            ValidationIsDisposable,
            ValidationIsRoleBased,
            ValidationScore,
            ValidationStatus,
            ValidationDateTime,
            ValidationAttempts,
            ValidationErrorMessage,
            RowID
        ))
        
        Connection.commit()
        Connection.close()
        return True
        
    except sqlite3.Error as E:
        print(f"## DATABASE ERROR: {E}")
        return False
    except Exception as E:
        print(f"## UNEXPECTED ERROR: {E}")
        return False