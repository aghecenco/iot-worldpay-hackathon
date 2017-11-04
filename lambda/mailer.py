import smtplib
import time
import imaplib
import email
import sys

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
            mail.select('inbox')
            previous_latest_email_id = latest_email_id
            
            type, data = mail.search(None, 'ALL')
            mail_ids = data[0]
        
            id_list = mail_ids.split()   
            first_email_id = int(id_list[0])
            latest_email_id = int(id_list[-1])
            # print 'first: ' + str(first_email_id)
            # print 'latest: ' + str(latest_email_id)
            print 'ids: ' + str(id_list)
            
            if previous_latest_email_id != latest_email_id:
                typ, data = mail.fetch(latest_email_id, '(RFC822)' )

                for response_part in data:
                    if isinstance(response_part, tuple):
                        msg = email.message_from_string(response_part[1])
                        email_subject = msg['subject']
                        email_from = msg['from']
                        print 'From : ' + email_from + '\n'
                        print 'Subject : ' + email_subject + '\n'

                        if 'funpay' in email_subject.lower():
                            event_name = msg.get_payload().split('\n')[0]
                            print "will purchase " + event_name
                            run_consumer(event_name)

            time.sleep(5)

    except Exception, e:
        print str(e)

def main():
    read_email_from_gmail()

if __name__ == "__main__":
    main()