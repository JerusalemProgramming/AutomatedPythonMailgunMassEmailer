## MODULE: MOD_2_EXTRACTUNIQUEEMAILSFROMOFFICE.PY
## PURPOSE: DEDUPLICATE EMAILS WITHIN OFFICE, SEPARATE CONTACT VS COMPANY

def fn_ExtractUniqueEmailsFromOffice(OfficeData):
    """
    ## EXTRACT UNIQUE EMAILS FROM OFFICE DATA, SEPARATING CONTACT AND COMPANY EMAILS
    ## INPUT: LIST OF CONTACT ROW DICTIONARIES
    ## OUTPUT: DICTIONARY WITH CONTACTEMAILS, COMPANYEMAILS, AND OFFICEINFO
    """
    
    ## INITIALIZE OUTPUT STRUCTURE
    Result = {
        "ContactEmails": {},
        "CompanyEmails": {},
        "OfficeInfo": {}
    }
    
    ## RETURN EMPTY RESULT IF NO DATA
    if not OfficeData:
        return Result
    
    ## EXTRACT OFFICE-LEVEL INFO FROM FIRST ROW
    FirstRow = OfficeData[0]
    Result["OfficeInfo"] = {
        "OfficeNumber": FirstRow.get("OfficeNumber"),
        "FirmName": FirstRow.get("FirmName"),
        "AddressOfCompany": FirstRow.get("AddressOfCompany"),
        "City": FirstRow.get("City"),
        "State_Province": FirstRow.get("State_Province"),
        "PostalZipCode": FirstRow.get("PostalZipCode"),
        "Website": FirstRow.get("Website")
    }
    
    ## PROCESS EACH ROW
    for Row in OfficeData:
        
        ContactEmail = Row.get("EmailOfContact")
        CompanyEmail = Row.get("EmailOfCompany")
        RowId = Row.get("rowid")
        
        ## CHECK IF THIS IS A COMPANY-ONLY ROW (NO CONTACT EMAIL)
        if not ContactEmail or not ContactEmail.strip():
            ## THIS IS A COMPANY-ONLY ROW
            if CompanyEmail and CompanyEmail.strip():
                CompanyEmail = CompanyEmail.strip().lower()
                
                ## CHECK IF THIS ROW HAS CONTACT INFO
                HasContactName = (
                    (Row.get("ContactName_First") and Row.get("ContactName_First").strip()) or
                    (Row.get("ContactName_Last") and Row.get("ContactName_Last").strip())
                )
                
                ## ONLY ADD IF NOT ALREADY IN DICT OR IF THIS IS A BETTER MATCH
                if CompanyEmail not in Result["CompanyEmails"]:
                    ## FIRST OCCURRENCE - ADD IT
                    Result["CompanyEmails"][CompanyEmail] = {
                        "rowid": RowId,
                        "EmailAttempts": Row.get("EmailAttempts")
                    }
                elif not HasContactName:
                    ## COMPANY EMAIL ALREADY EXISTS, BUT THIS ROW HAS NO CONTACT NAME
                    ## REPLACE WITH THIS ROWID (PREFER COMPANY-ONLY ROWS)
                    Result["CompanyEmails"][CompanyEmail] = {
                        "rowid": RowId,
                        "EmailAttempts": Row.get("EmailAttempts")
                    }
        else:
            ## THIS IS A CONTACT ROW
            ContactEmail = ContactEmail.strip().lower()
            ## ONLY ADD IF NOT ALREADY IN DICT (FIRST OCCURRENCE WINS)
            if ContactEmail not in Result["ContactEmails"]:
                Result["ContactEmails"][ContactEmail] = {
                    "rowid": RowId,
                    "ContactName_First": Row.get("ContactName_First"),
                    "ContactName_Last": Row.get("ContactName_Last"),
                    "Contact_TitlePosition": Row.get("Contact_TitlePosition"),
                    "NumberPhone": Row.get("NumberPhone"),
                    "EmailOfContact": ContactEmail,
                    "EmailAttempts": Row.get("EmailAttempts")
                }
    
    return Result