## MODULE: MOD_4_SENDEMAILVIAMAILGUN.PY
## PURPOSE: SEND TEXT-ONLY EMAIL VIA MAILGUN API WITH CLICK TRACKING

import requests
import uuid
from datetime import datetime

def fn_SendEmailViaMailgun(ToEmail, Subject, TextBody, MailgunConfig):
    """
    ## SEND TEXT-ONLY EMAIL VIA MAILGUN API
    ## INPUT: TOEMAIL (STRING), SUBJECT (STRING), TEXTBODY (STRING), MAILGUNCONFIG (DICT)
    ## OUTPUT: DICTIONARY WITH SUCCESS, MAILGUNMESSAGEID, STATUS, ERRORMESSAGE
    """
    
    ## INITIALIZE OUTPUT
    Result = {
        "Success": False,
        "MailgunMessageID": None,
        "Status": "failed",
        "ErrorMessage": None
    }
    
    ## EXTRACT CONFIG VALUES
    SendingKey = MailgunConfig.get("SENDING_KEY")
    Domain = MailgunConfig.get("DOMAIN")
    FromEmail = MailgunConfig.get("FROM_EMAIL")
    FromName = MailgunConfig.get("FROM_NAME")
    
    ## BUILD FROM ADDRESS
    FromAddress = f"{FromName} <{FromEmail}>"
    
    ## BUILD MAILGUN API URL
    ApiUrl = f"https://api.mailgun.net/v3/{Domain}/messages"
    
    ## GENERATE UNIQUE MESSAGE ID
    UniqueId = uuid.uuid4().hex
    Timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    MessageId = f"<{Timestamp}.{UniqueId}@{Domain}>"
    
    ## BUILD REQUEST DATA (TEXT-ONLY, NO HTML)
    RequestData = {
        "from": FromAddress,
        "to": ToEmail,
        "subject": Subject,
        "text": TextBody,
        "h:Reply-To": "info@zzfinancing.com",
        "h:Message-ID": MessageId,
        "o:envelope-sender": "bounce@zzfinancing.com",
        "h:List-Unsubscribe": "<mailto:info@zzfinancing.com?subject=unsubscribe>",
        "h:List-Unsubscribe-Post": "List-Unsubscribe=One-Click",
        "h:X-Priority": "3",
        "o:tracking-clicks": "no"
    }
    
    ## SEND REQUEST TO MAILGUN API
    try:
        Response = requests.post(
            ApiUrl,
            auth=("api", SendingKey),
            data=RequestData,
            timeout=30
        )
        
        ## PARSE RESPONSE
        if Response.status_code == 200:
            ## SUCCESS - EMAIL ACCEPTED
            ResponseJson = Response.json()
            Result["Success"] = True
            Result["MailgunMessageID"] = ResponseJson.get("id")
            Result["Status"] = "accepted"
        elif Response.status_code == 401:
            ## AUTHENTICATION ERROR
            Result["Status"] = "failed"
            Result["ErrorMessage"] = "Authentication failed - check API key"
        elif Response.status_code == 400:
            ## BAD REQUEST - LIKELY INVALID EMAIL
            ResponseJson = Response.json()
            Result["Status"] = "rejected"
            Result["ErrorMessage"] = ResponseJson.get("message", "Bad request")
        else:
            ## OTHER ERROR
            Result["Status"] = "failed"
            Result["ErrorMessage"] = f"HTTP {Response.status_code}: {Response.text}"
            
    except requests.exceptions.Timeout:
        Result["Status"] = "failed"
        Result["ErrorMessage"] = "Request timed out"
    except requests.exceptions.ConnectionError:
        Result["Status"] = "failed"
        Result["ErrorMessage"] = "Connection error"
    except requests.exceptions.RequestException as E:
        Result["Status"] = "failed"
        Result["ErrorMessage"] = f"Request error: {str(E)}"
    except Exception as E:
        Result["Status"] = "failed"
        Result["ErrorMessage"] = f"Unexpected error: {str(E)}"
    
    return Result