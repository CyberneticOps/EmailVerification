import re
import sys
import time
import string
import random
import smtplib
import argparse
import dns.resolver # dnspython

def parseArgs():
    parser = argparse.ArgumentParser(f"python3 {sys.argv[0]} -c <credentials list> -s <smtp server> -e <email list> -d <domain>")
    parser.add_argument("-c", dest="creds", help="Sender email credentials")
    parser.add_argument("-s", dest="smtp", help="Sender SMPT server address")
    parser.add_argument("-e", dest="emails", help="Recipient emails separated by \\n")
    parser.add_argument("-d", dest="domain", help="Domain to which the recipient emails belong")
    if len(sys.argv) != 2 and len(sys.argv) != 9:
        parser.print_usage(file=sys.stderr)
        sys.exit(1)
    return parser.parse_args()

def mxLookup(domain):
    # MX record lookup
    try:
        mxRecords = dns.resolver.resolve(domain, "MX")
        exchange = mxRecords[0].exchange
        exchange = str(exchange)
        return exchange
    except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN, dns.resolver.NoNameservers):
        return None

def randomString(length):
    letters = string.ascii_lowercase
    resultStr = ''.join(random.choice(letters) for i in range(length - 1))
    return resultStr

def syntaxVerification(email):
    # Simple Lenient Regex for syntax checking
    regex = '^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,})$'

    # Syntax check
    match = re.match(regex, email)
    return False if match == None else True

def smtpVerification(sndrEmail, password, rcptEmail, smtp):
    # Start SMTP conversation
    try:
        print("Connecting to SMTP server")
        with smtplib.SMTP_SSL(smtp, 465) as server:
            server.login(sndrEmail, password)
            server.mail(sndrEmail)
            print("MAIL FROM command sent")
            code, message = server.rcpt(rcptEmail)
            print("RCPT TO command sent")
            # Assume SMTP response 250 as success
            return True if code == 250 else False
    except Exception as error:
        return error

def main():
    args = parseArgs()
    creds = open(args.creds, "r").read().strip().split(":")

    # Search DNS MX (Mail Exchange) records
    exchange = mxLookup(args.domain)
    print(f"Recipient SMTP server: {exchange}")
    if exchange == None:
        print("[!] MX records not found, exiting\n")
        sys.exit(1)

    # Check if CATCH ALL is set in recipient SMTP server
    string = randomString(20)
    randEmail = string + f"@{args.domain}"
    catchAllVerif = smtpVerification(creds[0], creds[1], randEmail, args.smtp)
    if catchAllVerif != (True or False):
        print(f"[!] SMTP connection error: {catchAllVerif}\n")
        sys.exit(1)
    elif catchAllVerif:
        print("[-] CATCH ALL is set in recipient SMTP server, exiting\n")
        sys.exit(1)
    else:
        print("[+] CATCH ALL is not set in SMTP server, continuing")

    emails = open(args.emails, "r").readlines()
    invalidEmails = open("invalidEmails.txt", "a")
    trashEmails = open("trashEmails.txt", "a")
    verifiedEmails = open("verifiedEmails.txt", "a")

    # Validate syntax and existence of each email against the mail exchange
    errCount = 0
    for email in emails:
        if not syntaxVerification(email):
            print(f"[!] {email} - Invalid email address syntax")
            invalidEmails.write(email)

        emailVerif = smtpVerification(creds[0], creds[1], email, exchange)
        if emailVerif != (True and False):
            print(f"[!] SMTP connection error: {emailVerif}\n")
            sys.exit(1)
        elif not emailVerif:
            print(f"[!] {email} - Non-existent email address")
            trashEmails.write(email)
        else:
            print(f"[+] {email} - Verified email address")
            verifiedEmails.write(email)
        time.sleep(1)

if __name__ == "__main__":
    main()