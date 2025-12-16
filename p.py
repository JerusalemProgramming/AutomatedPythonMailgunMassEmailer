## IMPORT MODULES

## INPUT: READ CSV FILES
import core_0_0_ReadCSVFiles as core_00

## CREATE SQLITE DB
import core_0_1_CreateDB as core_01

## VERIFY SQLITE DB
import core_0_2_VerifyDB as core_02

## COMPARE DB VS. CSV
import core_0_3_CompareDB2CSVs as core_03

## ADD EMAIL + PRENORMALIZE OLD DATA COLUMNS TO DB
import core_0_4_AddNewColumns2DB as core_04

## VERIFY EMAIL + PRENORMALIZE OLD DATA COLUMNS TO DB
import core_0_5_VerifyNewColumns2DB as core_05

## VERIFY TEMPLATE + PRENORMALIZE OLD DATA COLUMNS
import core_0_6_VerifyTemplateColumnsInDB as core_06

## CLEAN (NORMALIZE) DATA IN DB (URLS, EMAILS, TELEPHONE, FAX)
import core_1_0_NormalizeDataInDB as core_10

##################### BEGIN CORE 20 - REDACTED PROPRIETARY CODE #####################
##################### END CORE 20 - REDACTED PROPRIETARY CODE #####################

## OUTPUT: WRITE CSV FILES FROM EXTRACTED CSV DATA IN PYTHON DICT
import core_9_0_WriteCSVFilesFromCSV as core_90

## OUTPUT: WRITE CSV FILES FROM SQLITE DB
import core_9_1_WriteAllCSVFilesFromDB as core_91

## DECLARE VARIABLES

## BEGIN MAIN PROGRAM

##################### BEGIN CORE 00 - READ ALL CSV FILES #####################
## BEGIN READ ALL CSV FILES
ListOfPythonDicts = core_00.fn_ReadAllCSVFiles()
## END READ ALL CSV FILES
##################### END CORE 00 - READ ALL CSV FILES #####################

##################### BEGIN CORE 01 - CREATE DB #####################
## AFTER READING CSV FILES
Result = core_01.fn_CreateDB(ListOfPythonDicts)
## TEST PRINT OUTPUT
print(Result)
##################### END CORE 01 - CREATE DB #####################

##################### BEGIN CORE 02 - VERIFY DB #####################
VerifyReport = core_02.fn_VerifyDB()
## TEST PRINT OUTPUT
print(VerifyReport)
##################### END CORE 02 - VERIFY DB #####################

##################### BEGIN CORE 03 - COMPARE DB 2 CSVs #####################
CompareReport = core_03.fn_CompareDB2CSVs()
## TEST PRINT OUTPUT
print(CompareReport)
##################### END CORE 03 - COMPARE DB 2 CSVs #####################

##################### BEGIN CORE 04 - ADD EMAIL COLUMNS + PRENORMALIZE OLD DATA COLUMNS 2 DB #####################
ColumnsResult = core_04.fn_AddNewColumns2DB()
## TEST PRINT OUTPUT
print(ColumnsResult)
##################### END CORE 04 - ADD EMAIL COLUMNS + PRENORMALIZE OLD DATA COLUMNS 2 DB #####################

##################### BEGIN CORE 05 - VERIFY EMAIL COLUMNS + PRENORMALIZE OLD DATA COLUMNS 2 DB #####################
VerifyColumnsReport = core_05.fn_VerifyNewColumnsInDB()
print(VerifyColumnsReport)
##################### END CORE -5 - VERIFY EMAIL COLUMNS + PRENORMALIZE OLD DATA COLUMNS 2 DB #####################

##################### BEGIN CORE -6 - VERIFY TEMPLATE COLUMNS + PRENORMALIZE OLD DATA COLUMNS IN DB #####################
VerifyTemplateReport = core_06.fn_VerifyTemplateColumnsInDB()
print(VerifyTemplateReport)
##################### BEGIN CORE 06 - VERIFY TEMPLATE COLUMNS + PRENORMALIZE OLD DATA COLUMNS IN DB #####################

##################### BEGIN CORE 10 - NORMALIZE DATA IN DB #####################
NormalizeReport = core_10.fn_NormalizeDataInDB()
## TEST PRINT OUTPUT
print(NormalizeReport)
##################### END CORE 10 - NORMALIZE DATA IN DB #####################

##################### BEGIN CORE 20 - REDACTED PROPRIETARY CODE #####################
##################### END CORE 20 - REDACTED PROPRIETARY CODE #####################

##################### BEGIN CORE 90 - WRITE ALL CSV FILES #####################
## BEGIN WRITE ALL CSV FILES
_ = core_90.fn_WriteAllCSVFilesFromCSV(ListOfPythonDicts)
## END WRITE ALL CSV FILES
##################### END CORE 90 - WRITE ALL CSV FILES #####################

##################### BEGIN CORE 91 - WRITE ALL CSV FILES FROM EXTRACTED CSV DATA IN PYTHON DICT #####################
## BEGIN WRITE ALL CSV FILES
_ = core_91.fn_WriteAllCSVFilesFromDB()
## END WRITE ALL CSV FILES
##################### END CORE 91 - WRITE ALL CSV FILES FROM EXTRACTED CSV DATA IN PYTHON DICT ####################

## END MAIN PROGRAM

