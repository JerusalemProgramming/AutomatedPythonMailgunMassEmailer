## TEST SCRIPT: TEST_CHECK_DNS_RECORDS.PY
## PURPOSE: TEST DNS RECORD CHECK FOR ZZFINANCING.COM

from mod_x_CheckDNSRecords import fn_CheckDnsRecords

def main():
    ## DEFINE DOMAINS
    Domain = "zzfinancing.com"
    MailgunDomain = "mailg.zzfinancing.com"
    
    ## RUN DNS CHECK
    print(f"CHECKING DNS RECORDS FOR {Domain} AND {MailgunDomain}...")
    print("-" * 50)
    
    Result = fn_CheckDnsRecords(Domain, MailgunDomain)
    
    ## DISPLAY SPF RESULT
    print("\nSPF RECORD:")
    if Result["SPF"]["Found"]:
        print(f"  STATUS: FOUND")
        print(f"  RECORD: {Result['SPF']['Record']}")
    else:
        print(f"  STATUS: NOT FOUND")
        print(f"  ERROR: {Result['SPF']['Error']}")
    
    ## DISPLAY DKIM RESULT
    print("\nDKIM RECORD:")
    if Result["DKIM"]["Found"]:
        print(f"  STATUS: FOUND")
        print(f"  RECORD: {Result['DKIM']['Record']}")
    else:
        print(f"  STATUS: NOT FOUND")
        print(f"  ERROR: {Result['DKIM']['Error']}")
    
    ## DISPLAY DMARC RESULT
    print("\nDMARC RECORD:")
    if Result["DMARC"]["Found"]:
        print(f"  STATUS: FOUND")
        print(f"  RECORD: {Result['DMARC']['Record']}")
    else:
        print(f"  STATUS: NOT FOUND")
        print(f"  ERROR: {Result['DMARC']['Error']}")
    
    print("-" * 50)
    print("DNS CHECK COMPLETE")

if __name__ == "__main__":
    main()