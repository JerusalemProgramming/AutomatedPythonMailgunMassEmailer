## MODULE: MOD_2B_VALIDATEEMAILBATCH.PY
## PURPOSE: VALIDATE INDIVIDUAL EMAIL AND FILTER OUT INVALID ONES

import requests
import json
from datetime import datetime

def fn_ValidateEmail(Email):
    """
    ## VALIDATES AN EMAIL ADDRESS USING RAPID-EMAIL-VERIFIER API
    ## RETURNS A DICTIONARY WITH VALIDATION RESULTS
    """
    
    ## API ENDPOINT
    ApiUrl = "https://rapid-email-verifier.fly.dev/api/validate"
    
    ## INITIALIZE RESULT DICTIONARY WITH DEFAULT VALUES
    Result = {
        "ValidationSyntax": None,
        "ValidationDomainExists": None,
        "ValidationMxRecords": None,
        "ValidationMailboxExists": None,
        "ValidationIsDisposable": None,
        "ValidationIsRoleBased": None,
        "ValidationScore": None,
        "ValidationStatus": None,
        "ValidationDateTime": None,
        "ValidationAttempts": 1,
        "ValidationErrorMessage": None
    }
    
    try:
        ## PREPARE REQUEST PAYLOAD
        Payload = {"email": Email}
        
        ## MAKE API REQUEST
        Response = requests.post(ApiUrl, json=Payload, timeout=30)
        
        ## CHECK IF REQUEST WAS SUCCESSFUL
        if Response.status_code == 200:
            Data = Response.json()
            
            ## EXTRACT VALIDATION RESULTS
            Validations = Data.get("validations", {})
            
            ## MAP API RESPONSE TO DATABASE COLUMNS (1=TRUE, 0=FALSE)
            Result["ValidationSyntax"] = 1 if Validations.get("syntax") else 0
            Result["ValidationDomainExists"] = 1 if Validations.get("domain_exists") else 0
            Result["ValidationMxRecords"] = 1 if Validations.get("mx_records") else 0
            Result["ValidationMailboxExists"] = 1 if Validations.get("mailbox_exists") else 0
            Result["ValidationIsDisposable"] = 1 if Validations.get("is_disposable") else 0
            Result["ValidationIsRoleBased"] = 1 if Validations.get("is_role_based") else 0
            
            ## GET STATUS
            Result["ValidationStatus"] = Data.get("status", "UNKNOWN")
            
            ## CALCULATE SCORE (0-100 BASED ON VALIDATION CHECKS)
            Score = 0
            if Result["ValidationSyntax"] == 1:
                Score += 20
            if Result["ValidationDomainExists"] == 1:
                Score += 20
            if Result["ValidationMxRecords"] == 1:
                Score += 20
            if Result["ValidationMailboxExists"] == 1:
                Score += 20
            if Result["ValidationIsDisposable"] == 0:
                Score += 10
            if Result["ValidationIsRoleBased"] == 0:
                Score += 10
            
            Result["ValidationScore"] = Score
            
            ## SET VALIDATION TIMESTAMP
            Result["ValidationDateTime"] = datetime.now().isoformat()
            
        else:
            ## REQUEST FAILED
            Result["ValidationErrorMessage"] = f"API returned status code {Response.status_code}"
            Result["ValidationDateTime"] = datetime.now().isoformat()
            
    except requests.exceptions.Timeout:
        Result["ValidationErrorMessage"] = "Request timeout"
        Result["ValidationDateTime"] = datetime.now().isoformat()
        
    except requests.exceptions.RequestException as E:
        Result["ValidationErrorMessage"] = f"Request error: {str(E)}"
        Result["ValidationDateTime"] = datetime.now().isoformat()
        
    except Exception as E:
        Result["ValidationErrorMessage"] = f"Unexpected error: {str(E)}"
        Result["ValidationDateTime"] = datetime.now().isoformat()
    
    return Result