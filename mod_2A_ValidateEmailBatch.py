## MODULE: MOD_2A_VALIDATEEMAILBATCH.PY
## PURPOSE: VALIDATE ALL EMAILS IN BATCH AND FILTER OUT INVALID ONES

import time
from mod_2B_ValidateEmail import fn_ValidateEmail
from mod_2C_UpdateValidationStatus import fn_UpdateValidationStatus

def fn_ValidateEmailBatch(EmailData, TableName):
    """
    ## VALIDATES ALL EMAILS IN EMAILDATA DICTIONARY
    ## UPDATES DATABASE WITH VALIDATION RESULTS
    ## REMOVES INVALID EMAILS FROM DICTIONARY
    ## INPUT: EMAILDATA (DICT), TABLENAME (STRING)
    ## OUTPUT: FILTERED EMAILDATA (DICT), VALIDATIONSTATS (DICT)
    """
    
    ## INITIALIZE VALIDATION STATS
    ValidationStats = {
        "TotalContactEmails": len(EmailData["ContactEmails"]),
        "TotalCompanyEmails": len(EmailData["CompanyEmails"]),
        "ValidContactEmails": 0,
        "ValidCompanyEmails": 0,
        "InvalidContactEmails": 0,
        "InvalidCompanyEmails": 0,
        "ContactReasons": {},
        "CompanyReasons": {}
    }
    
    ## LISTS TO TRACK EMAILS TO REMOVE
    InvalidContactEmails = []
    InvalidCompanyEmails = []
    
    ## VALIDATE CONTACT EMAILS
    print(f"\n  Validating {ValidationStats['TotalContactEmails']} contact emails...")
    
    for ContactEmail, ContactData in EmailData["ContactEmails"].items():
        
        ## CHECK IF ALREADY VALIDATED (SKIP IF VALIDATION EXISTS)
        if ContactData.get("ValidationStatus") is not None:
            print(f"    Skipping {ContactEmail} (already validated)")
            
            ## CHECK IF PREVIOUSLY MARKED INVALID
            if ContactData.get("ValidationStatus") == "INVALID":
                InvalidContactEmails.append(ContactEmail)
                ValidationStats["InvalidContactEmails"] += 1
            else:
                ValidationStats["ValidContactEmails"] += 1
            continue
        
        ## VALIDATE EMAIL
        print(f"    Validating {ContactEmail}...")
        ValidationResult = fn_ValidateEmail(ContactEmail)
        
        ## UPDATE DATABASE WITH VALIDATION RESULTS
        RowId = ContactData.get("rowid")
        fn_UpdateValidationStatus(TableName, RowId, ValidationResult)
        
        ## CHECK IF EMAIL IS VALID BASED ON CRITERIA
        IsValid = fn_CheckValidationCriteria(ValidationResult)
        
        if not IsValid:
            ## MARK FOR REMOVAL
            InvalidContactEmails.append(ContactEmail)
            ValidationStats["InvalidContactEmails"] += 1
            
            ## TRACK REJECTION REASON
            Reason = fn_GetRejectionReason(ValidationResult)
            ValidationStats["ContactReasons"][Reason] = ValidationStats["ContactReasons"].get(Reason, 0) + 1
            
            print(f"      INVALID: {Reason}")
        else:
            ValidationStats["ValidContactEmails"] += 1
            print(f"      VALID")
        
        ## RATE LIMIT DELAY (0.5 SECONDS BETWEEN API CALLS)
        time.sleep(0.5)
    
    ## VALIDATE COMPANY EMAILS
    print(f"\n  Validating {ValidationStats['TotalCompanyEmails']} company emails...")
    
    for CompanyEmail, CompanyData in EmailData["CompanyEmails"].items():
        
        ## CHECK IF ALREADY VALIDATED (SKIP IF VALIDATION EXISTS)
        if CompanyData.get("ValidationStatus") is not None:
            print(f"    Skipping {CompanyEmail} (already validated)")
            
            ## CHECK IF PREVIOUSLY MARKED INVALID
            if CompanyData.get("ValidationStatus") == "INVALID":
                InvalidCompanyEmails.append(CompanyEmail)
                ValidationStats["InvalidCompanyEmails"] += 1
            else:
                ValidationStats["ValidCompanyEmails"] += 1
            continue
        
        ## VALIDATE EMAIL
        print(f"    Validating {CompanyEmail}...")
        ValidationResult = fn_ValidateEmail(CompanyEmail)
        
        ## UPDATE DATABASE WITH VALIDATION RESULTS
        RowId = CompanyData.get("rowid")
        fn_UpdateValidationStatus(TableName, RowId, ValidationResult)
        
        ## CHECK IF EMAIL IS VALID BASED ON CRITERIA
        IsValid = fn_CheckValidationCriteria(ValidationResult)
        
        if not IsValid:
            ## MARK FOR REMOVAL
            InvalidCompanyEmails.append(CompanyEmail)
            ValidationStats["InvalidCompanyEmails"] += 1
            
            ## TRACK REJECTION REASON
            Reason = fn_GetRejectionReason(ValidationResult)
            ValidationStats["CompanyReasons"][Reason] = ValidationStats["CompanyReasons"].get(Reason, 0) + 1
            
            print(f"      INVALID: {Reason}")
        else:
            ValidationStats["ValidCompanyEmails"] += 1
            print(f"      VALID")
        
        ## RATE LIMIT DELAY (0.5 SECONDS BETWEEN API CALLS)
        time.sleep(0.5)
    
    ## REMOVE INVALID EMAILS FROM EMAILDATA
    for InvalidEmail in InvalidContactEmails:
        del EmailData["ContactEmails"][InvalidEmail]
    
    for InvalidEmail in InvalidCompanyEmails:
        del EmailData["CompanyEmails"][InvalidEmail]
    
    ## PRINT VALIDATION SUMMARY
    print(f"\n  Validation Summary:")
    print(f"    Contact Emails: {ValidationStats['ValidContactEmails']} valid, {ValidationStats['InvalidContactEmails']} invalid")
    print(f"    Company Emails: {ValidationStats['ValidCompanyEmails']} valid, {ValidationStats['InvalidCompanyEmails']} invalid")
    
    if ValidationStats["ContactReasons"]:
        print(f"    Contact Rejection Reasons:")
        for Reason, Count in ValidationStats["ContactReasons"].items():
            print(f"      {Reason}: {Count}")
    
    if ValidationStats["CompanyReasons"]:
        print(f"    Company Rejection Reasons:")
        for Reason, Count in ValidationStats["CompanyReasons"].items():
            print(f"      {Reason}: {Count}")
    
    return EmailData, ValidationStats


def fn_CheckValidationCriteria(ValidationResult):
    """
    ## CHECK IF EMAIL MEETS VALIDATION CRITERIA
    ## REQUIRED: SYNTAX=1, DOMAIN_EXISTS=1, MX_RECORDS=1, IS_DISPOSABLE=0
    ## INPUT: VALIDATIONRESULT (DICT)
    ## OUTPUT: ISVALID (BOOLEAN)
    """
    
    ## CHECK FOR API ERROR
    if ValidationResult.get("ValidationErrorMessage") is not None:
        return False
    
    ## CHECK REQUIRED FIELDS
    if ValidationResult.get("ValidationSyntax") != 1:
        return False
    
    if ValidationResult.get("ValidationDomainExists") != 1:
        return False
    
    if ValidationResult.get("ValidationMxRecords") != 1:
        return False
    
    ## CHECK DISPOSABLE (MUST BE 0 = FALSE)
    if ValidationResult.get("ValidationIsDisposable") == 1:
        return False
    
    ## ALL CRITERIA MET
    return True


def fn_GetRejectionReason(ValidationResult):
    """
    ## DETERMINE WHY EMAIL WAS REJECTED
    ## INPUT: VALIDATIONRESULT (DICT)
    ## OUTPUT: REASON (STRING)
    """
    
    ## CHECK FOR API ERROR FIRST
    if ValidationResult.get("ValidationErrorMessage") is not None:
        return f"API Error: {ValidationResult.get('ValidationErrorMessage')}"
    
    ## CHECK EACH CRITERION
    if ValidationResult.get("ValidationSyntax") != 1:
        return "Invalid Syntax"
    
    if ValidationResult.get("ValidationDomainExists") != 1:
        return "Domain Does Not Exist"
    
    if ValidationResult.get("ValidationMxRecords") != 1:
        return "No MX Records"
    
    if ValidationResult.get("ValidationIsDisposable") == 1:
        return "Disposable Email"
    
    ## UNKNOWN REASON
    return "Unknown"