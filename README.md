# Email Verification Tool

This Python script verifies the syntax and existence of email addresses against a specified domain using SMTP. It performs the following actions:

- **Syntax Verification**: Checks the syntax of email addresses using a lenient regular expression.
- **SMTP Verification**: Connects to the SMTP server of the recipient domain and verifies the existence of each email address.
- **MX Record Lookup**: Retrieves the MX (Mail Exchange) records of the recipient domain to determine the existance of the recipient SMTP server.

## Usage

```bash
python3 email_verification.py -c <credentials list> -s <smtp server> -e <email list> -d <domain>
```

## Arguments

- `-c`: Sender email credentials file.
- `-s`: Sender SMTP server address.
- `-e`: File containing recipient emails separated by \n.
- `-d`: Domain to which the recipient emails belong.

## Requirements

- Python 3.x
- dnspython library

## Installation

### Linux Virtual Environment

1. Create virtual Python environment:
```bash
python3 -m venv venv
```

2. Activate virtual environment:
```bash
source venv/bin/activate
```

3. Install required library:
```bash
python3 -m pip install dnspython
```

4. Clone repository and change directory:
```bash
git clone https://github.com/CyberneticOps/EmailVerification.git
cd EmailVerification
```

## Running the Script
```bash
python3 verifyemails.py -c sender_creds.txt -s smtp.sender.com -e recipient_emails.txt -d recipient.com
```

The script will generate three output files:
- `invalidEmails.txt`: Contains email addresses with invalid syntax.
- `trashEmails.txt`: Contains email addresses that do not exists.
- `verifiedEmails.txt`: Contains verified email addresses.

## Notes
- Ensure that the credentials file (`sender_creds.txt`) follows the format: `<sender_email>:<password>`.
- Make sure to replace `smtp.sender.com` with the correct SMTP server address.


## Additional Notes
- `SMTP Connection`: The script connects to the SMTP server using SSL on port 465. Make sure the SMTP server supports SSL connections.
- `CATCH ALL Check`: It checks if the recipient SMTP server has a CATCH ALL configuration. If it does, the script exits to prevent indiscriminate email verification.
- `Delay`: To avoid overwhelming the SMTP server, the script introduces a delay of 1 second between each email verification.

## Contribution
Contributions are welcome! Feel free to open an issue or submit a pull request with any improvements or bug fixes.

## Licence
This project is licensed under the MIT License. See the [[LICENSE]](https://github.com/CyberneticOps/EmailVerification/blob/main/LICENSE) file for details.
