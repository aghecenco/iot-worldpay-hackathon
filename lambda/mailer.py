import smtplib
import time
import imaplib
import email

from runConsumerOWP import run_consumer

ORG_EMAIL   = "@gmail.com"
FROM_EMAIL  = "funpay.hackathon" + ORG_EMAIL
FROM_PWD    = "h4ck4th0n"
SMTP_SERVER = "imap.gmail.com"
SMTP_PORT   = 993

def read_email_from_gmail():
    try:
        mail = imaplib.IMAP4_SSL(SMTP_SERVER)
        mail.login(FROM_EMAIL,FROM_PWD)
        mail.select('inbox')

        type, data = mail.search(None, 'ALL')
        mail_ids = data[0]
        
        id_list = mail_ids.split()   
        first_email_id = int(id_list[0])
        latest_email_id = int(id_list[-1])

        while True:
            previous_latest_email_id = latest_email_id
            
            type, data = mail.search(None, 'ALL')
            mail_ids = data[0]
        
            id_list = mail_ids.split()   
            first_email_id = int(id_list[0])
            latest_email_id = int(id_list[-1])
            
            if previous_latest_email_id != latest_email_id:
                typ, data = mail.fetch(latest_email_id, '(RFC822)' )

                for response_part in data:
                    if isinstance(response_part, tuple):
                        msg = email.message_from_string(response_part[1])
                        email_subject = msg['subject']
                        email_from = msg['from']
                        print 'From : ' + email_from + '\n'
                        print 'Subject : ' + email_subject + '\n'

                        if 'funpay' in email_subject:
                            event_price = msg.get_payload().split()[0]

                                
            time.sleep(5)

    except Exception, e:
        print str(e)

def main():
    read_email_from_gmail()

if __name__ == "__main__":
    main()