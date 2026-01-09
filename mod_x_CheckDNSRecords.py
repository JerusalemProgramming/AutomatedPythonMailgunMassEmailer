## MODULE: MOD_CHECK_DNS_RECORDS.PY
## PURPOSE: CHECK SPF, DKIM, AND DMARC RECORDS FOR EMAIL DOMAIN

import dns.resolver

def fn_CheckDnsRecords(Domain, MailgunDomain):
    """
    ## CHECK SPF, DKIM, AND DMARC RECORDS FOR EMAIL DELIVERABILITY
    ## INPUT: DOMAIN (STRING), MAILGUNDOMAIN (STRING)
    ## OUTPUT: DICTIONARY WITH RESULTS FOR EACH RECORD TYPE
    """
    
    ## INITIALIZE OUTPUT
    Result = {
        "SPF": {"Found": False, "Record": None, "Error": None},
        "DKIM": {"Found": False, "Record": None, "Error": None},
        "DMARC": {"Found": False, "Record": None, "Error": None}
    }
    
    ## CHECK SPF RECORD FOR MAILGUN DOMAIN
    try:
        SpfAnswers = dns.resolver.resolve(MailgunDomain, "TXT")
        for Rdata in SpfAnswers:
            RecordText = str(Rdata).strip('"')
            if "v=spf1" in RecordText:
                Result["SPF"]["Found"] = True
                Result["SPF"]["Record"] = RecordText
                break
        if not Result["SPF"]["Found"]:
            Result["SPF"]["Error"] = "NO SPF RECORD FOUND"
    except dns.resolver.NXDOMAIN:
        Result["SPF"]["Error"] = "DOMAIN NOT FOUND"
    except dns.resolver.NoAnswer:
        Result["SPF"]["Error"] = "NO TXT RECORDS FOUND"
    except Exception as E:
        Result["SPF"]["Error"] = str(E)
    
    ## CHECK DKIM RECORD FOR MAILGUN (STANDARD MAILGUN SELECTOR)
    DkimHost = f"pdk1._domainkey.{MailgunDomain}"
    try:
        DkimAnswers = dns.resolver.resolve(DkimHost, "TXT")
        for Rdata in DkimAnswers:
            RecordText = str(Rdata).strip('"')
            if "v=DKIM1" in RecordText or "k=rsa" in RecordText:
                Result["DKIM"]["Found"] = True
                Result["DKIM"]["Record"] = RecordText
                break
        if not Result["DKIM"]["Found"]:
            Result["DKIM"]["Error"] = "NO DKIM RECORD FOUND"
    except dns.resolver.NXDOMAIN:
        Result["DKIM"]["Error"] = "DKIM HOST NOT FOUND"
    except dns.resolver.NoAnswer:
        Result["DKIM"]["Error"] = "NO DKIM TXT RECORDS FOUND"
    except Exception as E:
        Result["DKIM"]["Error"] = str(E)
    
    ## CHECK DMARC RECORD FOR MAIN DOMAIN
    DmarcHost = f"_dmarc.{Domain}"
    try:
        DmarcAnswers = dns.resolver.resolve(DmarcHost, "TXT")
        for Rdata in DmarcAnswers:
            RecordText = str(Rdata).strip('"')
            if "v=DMARC1" in RecordText:
                Result["DMARC"]["Found"] = True
                Result["DMARC"]["Record"] = RecordText
                break
        if not Result["DMARC"]["Found"]:
            Result["DMARC"]["Error"] = "NO DMARC RECORD FOUND"
    except dns.resolver.NXDOMAIN:
        Result["DMARC"]["Error"] = "DMARC HOST NOT FOUND"
    except dns.resolver.NoAnswer:
        Result["DMARC"]["Error"] = "NO DMARC TXT RECORDS FOUND"
    except Exception as E:
        Result["DMARC"]["Error"] = str(E)
    
    return Result
