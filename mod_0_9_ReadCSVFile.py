## IMPORT MODULES
import csv

## BEGIN DEFINE FUNCTION
def fn_ReadCSVFile(FilePath):
    
    ## READ CSV FILE AND ASSIGN INCREMENTAL OFFICE NUMBERS
    
    ## DECLARE VARIABLES
    OfficeData = {}
    OfficeCounter = 1
    
    ## OPEN CSV FILE WITH SEMICOLON DELIMITER
    with open(FilePath, 'r', encoding='utf-8') as CsvFile:
        
        Reader = csv.DictReader(CsvFile, delimiter=';')
        
        for Row in Reader:
            
            ## ASSIGN INCREMENTAL OFFICE NUMBER AS STRING
            CurrentOfficeNumber = str(OfficeCounter)
            
            ## CREATE PRIMARY CONTACT DICTIONARY
            Contact = {
                'OfficeNumber': CurrentOfficeNumber,
                'FirmName': Row.get('FirmName', ''),
                'ContactName_First': '',
                'ContactName_Last': Row.get('Contact_Name', ''),
                'Contact_TitlePosition': Row.get('Contact_TitlePosition', ''),
                'NumberPhone': Row.get('NumberPhone', ''),
                'EmailOfContact': Row.get('EmailOfContact', ''),
                'EmailOfCompany': '',
                'AddressOfCompany': Row.get('AddressOfCompany', ''),
                'City': Row.get('City', ''),
                'State_Province': Row.get('State_Province', ''),
                'PostalZipCode': Row.get('PostalZipCode', ''),
                'Country': Row.get('Country', ''),
                'AUM_USD_MIL_UnlessNoted': Row.get('AUM_USD_MIL_UnlessNoted', ''),
                'Website': Row.get('Website', ''),
                'Notes': Row.get('Notes', '')
            }
            
            ## INITIALIZE LIST FOR NEW OFFICE NUMBER
            OfficeData[CurrentOfficeNumber] = [Contact]
            
            ## ADD SECONDARY CONTACT IF EXISTS
            if Row.get('SecondaryContact_Name', '').strip():
                SecondaryContact = {
                    'OfficeNumber': CurrentOfficeNumber,
                    'FirmName': Row.get('FirmName', ''),
                    'ContactName_First': '',
                    'ContactName_Last': Row.get('SecondaryContact_Name', ''),
                    'Contact_TitlePosition': Row.get('SecondaryContact_TitlePosition', ''),
                    'NumberPhone': Row.get('SecondaryContact_NumberPhone', ''),
                    'EmailOfContact': Row.get('SecondaryContact_EmailOfContact', ''),
                    'EmailOfCompany': '',
                    'AddressOfCompany': Row.get('AddressOfCompany', ''),
                    'City': Row.get('City', ''),
                    'State_Province': Row.get('State_Province', ''),
                    'PostalZipCode': Row.get('PostalZipCode', ''),
                    'Country': Row.get('Country', ''),
                    'AUM_USD_MIL_UnlessNoted': Row.get('AUM_USD_MIL_UnlessNoted', ''),
                    'Website': Row.get('Website', ''),
                    'Notes': Row.get('Notes', '')
                }
                OfficeData[CurrentOfficeNumber].append(SecondaryContact)
            
            ## INCREMENT OFFICE COUNTER
            OfficeCounter += 1
    
    ## RETURN VARIABLES
    return(OfficeData)

## END DEFINE FUNCTION