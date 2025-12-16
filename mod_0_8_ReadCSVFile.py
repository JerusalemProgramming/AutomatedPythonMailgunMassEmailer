## IMPORT MODULES
import csv

## BEGIN DEFINE FUNCTION
def fn_ReadCSVFile(FilePath):
    
    ## READ CSV FILE AND GROUP CONTACTS BY OFFICENUMBER
    
    ## DECLARE VARIABLES
    OfficeData = {}
    CurrentOfficeNumber = None
    
    ## OPEN CSV FILE WITH SEMICOLON DELIMITER
    with open(FilePath, 'r', encoding='utf-8') as CsvFile:
        
        Reader = csv.DictReader(CsvFile, delimiter=';')
        
        for Row in Reader:
            OfficeNum = Row.get('OfficeNumber', '').strip()
            
            ## UPDATE CURRENT OFFICE NUMBER IF NOT BLANK
            if OfficeNum:
                CurrentOfficeNumber = OfficeNum
            
            ## SKIP ROW IF NO CURRENT OFFICE NUMBER
            if not CurrentOfficeNumber:
                continue
            
            ## CREATE CONTACT DICTIONARY WITH ALL FIELDS
            Contact = {
                'OfficeNumber': CurrentOfficeNumber,
                'FirmName': Row.get('FirmName', ''),
                'ContactName_First': Row.get('ContactName_First', ''),
                'ContactName_Last': Row.get('ContactName_Last', ''),
                'Contact_TitlePosition': Row.get('Contact_TitlePosition', ''),
                'NumberPhone': Row.get('NumberPhone', ''),
                'EmailOfContact': Row.get('EmailOfContact', ''),
                'EmailOfCompany': Row.get('EmailOfCompany', ''),
                'AddressOfCompany': Row.get('AddressOfCompany', ''),
                'City': Row.get('City', ''),
                'State_Province': Row.get('State_Province', ''),
                'PostalZipCode': Row.get('PostalZipCode', ''),
                'Country': Row.get('Country', ''),
                'AUM_USD_MIL_UnlessNoted': Row.get('AUM_USD_MIL_UnlessNoted', ''),
                'Website': Row.get('Website', ''),
                'Notes': Row.get('Notes', '')
            }
            
            ## INITIALIZE LIST IF NEW OFFICE NUMBER
            if CurrentOfficeNumber not in OfficeData:
                OfficeData[CurrentOfficeNumber] = []
            
            ## APPEND CONTACT TO OFFICE
            OfficeData[CurrentOfficeNumber].append(Contact)
    
    ## RETURN VARIABLES
    return(OfficeData)

## END DEFINE FUNCTION