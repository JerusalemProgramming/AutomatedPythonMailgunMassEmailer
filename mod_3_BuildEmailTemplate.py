## MODULE: MOD_3_BUILDEMAILTEMPLATE.PY
## PURPOSE: BUILD PERSONALIZED TEXT-ONLY EMAIL BY IMPORTING TEMPLATE MODULES

import templates.contact_email_template as mod_00A
import templates.company_email_template as mod_00B

def fn_BuildEmailTemplate(TemplateType, TemplateData):
    """
    ## BUILD PERSONALIZED TEXT-ONLY EMAIL USING TEMPLATE MODULES
    ## INPUT: TEMPLATETYPE ("contact" OR "company"), TEMPLATEDATA (DICT WITH PLACEHOLDER VALUES)
    ## OUTPUT: DICTIONARY WITH SUBJECT AND TEXTBODY
    """
    
    ## INITIALIZE OUTPUT
    Result = {
        "Subject": "",
        "TextBody": ""
    }
    
    if TemplateType == "contact":
        ## EXTRACT CONTACT VALUES FROM TEMPLATE DATA
        ContactName_First = TemplateData.get("ContactName_First") or ""
        ContactName_Last = TemplateData.get("ContactName_Last") or ""
        Contact_TitlePosition = TemplateData.get("Contact_TitlePosition") or ""
        NumberPhone = TemplateData.get("NumberPhone") or ""
        EmailOfContact = TemplateData.get("EmailOfContact") or ""
        FirmName = TemplateData.get("FirmName") or ""
        AddressOfCompany = TemplateData.get("AddressOfCompany") or ""
        City = TemplateData.get("City") or ""
        State_Province = TemplateData.get("State_Province") or ""
        PostalZipCode = TemplateData.get("PostalZipCode") or ""
        Country = TemplateData.get("Country") or ""
        Website = TemplateData.get("Website") or ""
        
        ## BUILD CONTACT EMAIL
        Result["Subject"] = mod_00A.fn_GetContactEmailSubject()
        Result["TextBody"] = mod_00A.fn_GetContactEmailBody(
            ContactName_First,
            ContactName_Last,
            Contact_TitlePosition,
            NumberPhone,
            EmailOfContact,
            FirmName,
            AddressOfCompany,
            City,
            State_Province,
            PostalZipCode,
            Country,
            Website
        )
    
    elif TemplateType == "company":
        ## EXTRACT COMPANY VALUES FROM TEMPLATE DATA
        FirmName = TemplateData.get("FirmName") or ""
        AddressOfCompany = TemplateData.get("AddressOfCompany") or ""
        City = TemplateData.get("City") or ""
        State_Province = TemplateData.get("State_Province") or ""
        PostalZipCode = TemplateData.get("PostalZipCode") or ""
        Country = TemplateData.get("Country") or ""
        Website = TemplateData.get("Website") or ""
        EmailOfCompany = TemplateData.get("EmailOfCompany") or ""
        
        ## BUILD COMPANY EMAIL
        Result["Subject"] = mod_00B.fn_GetCompanyEmailSubject()
        Result["TextBody"] = mod_00B.fn_GetCompanyEmailBody(
            FirmName,
            AddressOfCompany,
            City,
            State_Province,
            PostalZipCode,
            Country,
            Website,
            EmailOfCompany
        )
    
    else:
        print(f"## ERROR: UNKNOWN TEMPLATE TYPE: {TemplateType}")
    
    return Result