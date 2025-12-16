## IMPORT MODULES
import mod_1_0_NormalizeDataWebsitesInDB as mod_10
import mod_1_1_NormalizeDataEmailsInDB as mod_11
import mod_1_2_NormalizeDataPhoneFaxNumbersInDB as mod_12

## DEFINE FUNCTION
def fn_NormalizeDataInDB():
    ## DECLARE VARIABLES
    
    ## BUILD REPORT
    Report = "\n" + "="*60 + "\n"
    Report += "DATA NORMALIZATION REPORT\n"
    Report += "="*60 + "\n\n"
    
    ## NORMALIZE WEBSITES
    WebsiteResult = mod_10.fn_NormalizeDataWebsitesInDB()
    Report += f"1. {WebsiteResult}\n\n"

    ## NORMALIZE EMAILS:
    EmailResult = mod_11.fn_NormalizeDataEmailsInDB()
    Report += f"2. {EmailResult}\n\n"
    
    ## NORMALIZE PHONE/FAX NUMBERS
    PhoneFaxResult = mod_12.fn_NormalizeDataPhoneFaxNumbersInDB()
    Report += f"3. {PhoneFaxResult}\n\n"
    
    ## FINAL STATUS
    Report += "="*60 + "\n"
    Report += "DATA NORMALIZATION COMPLETED\n"
    Report += "="*60 + "\n"
    
    ## RETURN REPORT
    return Report