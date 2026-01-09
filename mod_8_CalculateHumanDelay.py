## MODULE: mod_8_CalculateHumanDelay.py
## PURPOSE: CALCULATE HUMAN-LIKE DELAYS BETWEEN EMAILS AND OFFICES

import random

def fn_CalculateEmailDelay():
    """
    ## CALCULATE RANDOM DELAY BETWEEN INDIVIDUAL EMAILS
    ## RETURNS: DELAY IN SECONDS (30-90 SECONDS)
    """
    DelaySeconds = random.uniform(30, 90)
    return DelaySeconds

def fn_CalculateOfficeBreak():
    """
    ## CALCULATE RANDOM BREAK BETWEEN OFFICES
    ## RETURNS: DELAY IN SECONDS (90-180 SECONDS)
    """
    BreakSeconds = random.uniform(90, 180)
    return BreakSeconds