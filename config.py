## CONFIG.PY
## PURPOSE: CENTRAL CONFIGURATION FOR ALL MODULES

import os
from dotenv import load_dotenv

## LOAD ENVIRONMENT VARIABLES FROM .ENV FILE
load_dotenv()

## DATABASE
DB_PATH = "data.db"

## TABLE NAMES (9 TABLES)
TABLE_NAMES = [
    "FamilyOffices",
    "WealthManagement",
    "Endowments",
    "InstitutionalInvestment",
    "InvestmentBanking",
    "PrivateBanks",
    "MerchantBanks",
    "PensionFunds",
    "FundOfFund"
]

## MAILGUN CREDENTIALS (LOADED FROM .ENV)
MAILGUN_CONFIG = {
    "SENDING_KEY": os.getenv("MAILGUN_SENDING_KEY"),
    "DOMAIN": os.getenv("MAILGUN_DOMAIN"),
    "FROM_EMAIL": os.getenv("MAILGUN_FROM_EMAIL"),
    "FROM_NAME": os.getenv("MAILGUN_FROM_NAME")
}

## LOGGING
LOG_DIR = "logs"

## MAXIMUM OFFICES PER SESSION
MAX_OFFICES_PER_SESSION = 10 ## CLI ARGUMENT --max-offices 12

## RETRY SETTINGS
MAX_ATTEMPTS = 6  ## MAXIMUM RETRY ATTEMPTS PER EMAIL