## MODULE: mod_00_GetUserInput.py
## PURPOSE: HANDLE USER INPUT FOR INTERACTIVE MODE

from config import TABLE_NAMES

def fn_DisplayTableMenu():
    """
    ## DISPLAY NUMBERED LIST OF AVAILABLE TABLES
    """
    print("\n" + "="*50)
    print("AVAILABLE TABLES:")
    print("="*50)
    for Index, TableName in enumerate(TABLE_NAMES, start=1):
        print(f"  {Index}. {TableName}")
    print("="*50)

def fn_GetTableSelection():
    """
    ## PROMPT USER TO SELECT A TABLE BY NUMBER
    ## RETURNS: SELECTED TABLE NAME OR NONE IF INVALID
    """
    while True:
        try:
            fn_DisplayTableMenu()
            Choice = input("\nSELECT TABLE NUMBER (OR 'Q' TO QUIT): ").strip().upper()
            
            if Choice == 'Q':
                return None
            
            Choice = int(Choice)
            
            if 1 <= Choice <= len(TABLE_NAMES):
                SelectedTable = TABLE_NAMES[Choice - 1]
                print(f"\nSELECTED: {SelectedTable}")
                return SelectedTable
            else:
                print(f"\nINVALID CHOICE. PLEASE SELECT 1-{len(TABLE_NAMES)}")
        
        except ValueError:
            print("\nINVALID INPUT. PLEASE ENTER A NUMBER.")

def fn_GetRetryFailedInput():
    """
    ## PROMPT USER IF THEY WANT TO RETRY FAILED EMAILS
    ## RETURNS: BOOLEAN (TRUE TO RETRY FAILED, FALSE FOR NEW ONLY)
    """
    while True:
        Response = input("\nINCLUDE FAILED EMAILS FOR RETRY? (Y/N): ").strip().upper()
        
        if Response == 'Y':
            print("RETRY MODE: Will include failed and rejected emails")
            return True
        elif Response == 'N':
            print("NORMAL MODE: Will only process new unsent emails")
            return False
        else:
            print("INVALID INPUT. PLEASE ENTER 'Y' OR 'N'.")

def fn_GetOfficeInput():
    """
    ## PROMPT USER FOR OFFICE RANGE OR COUNT
    ## RETURNS: DICT WITH TYPE ("count" OR "range") AND VALUES
    ## EXAMPLES: 
    ##   INPUT "25" -> {"type": "count", "value": 25}
    ##   INPUT "1-50" -> {"type": "range", "start": 1, "end": 50}
    """
    while True:
        try:
            UserInput = input("\nENTER OFFICE RANGE (e.g., 1-50) OR NUMBER OF OFFICES (e.g., 25): ").strip()
            
            ## CHECK IF INPUT IS A RANGE (CONTAINS HYPHEN)
            if '-' in UserInput:
                ## PARSE RANGE
                Parts = UserInput.split('-')
                
                if len(Parts) != 2:
                    print("\nINVALID RANGE FORMAT. USE FORMAT: START-END (e.g., 1-50)")
                    continue
                
                Start = int(Parts[0].strip())
                End = int(Parts[1].strip())
                
                if Start <= 0 or End <= 0:
                    print("\nOFFICE NUMBERS MUST BE POSITIVE.")
                    continue
                
                if Start > End:
                    print("\nSTART OFFICE MUST BE LESS THAN OR EQUAL TO END OFFICE.")
                    continue
                
                return {
                    "type": "range",
                    "start": Start,
                    "end": End
                }
            
            else:
                ## PARSE COUNT
                Count = int(UserInput)
                
                if Count <= 0:
                    print("\nPLEASE ENTER A POSITIVE NUMBER.")
                    continue
                
                return {
                    "type": "count",
                    "value": Count
                }
        
        except ValueError:
            print("\nINVALID INPUT. PLEASE ENTER A NUMBER OR RANGE (e.g., 1-50).")

def fn_Ask2Continue():
    """
    ## ASK USER IF THEY WANT TO PROCESS ANOTHER BATCH
    ## RETURNS: TRUE TO CONTINUE, FALSE TO EXIT
    """
    while True:
        Response = input("\nPROCESS ANOTHER BATCH? (Y/N): ").strip().upper()
        
        if Response == 'Y':
            return True
        elif Response == 'N':
            return False
        else:
            print("INVALID INPUT. PLEASE ENTER 'Y' OR 'N'.")