#!/usr/bin/python3

import smtplib
#from email.mime.text import MIMEText
#from email.mime.multipart import MIMEMultipart

"""address_book = ['']
msg = MIMEMultipart()    
sender = ''
subject = 'Test Run'
body = "Body of test run"

msg['From'] = sender
msg['To'] = ','.join(address_book)
msg['Subject'] = subject
msg.attach(MIMEText(body, 'plain'))
text=msg.as_string()
#print text
# Send the message via our SMTP server
s = smtplib.SMTP('our.exchangeserver.com')
s.sendmail(sender,address_book, text)
s.quit()    """  


mailserver = smtplib.SMTP('smtp.office365.com',587)
mailserver.ehlo()
mailserver.starttls()
mailserver.login('---', '---')
#Adding a newline before the body text fixes the missing message body
mailserver.sendmail('---','---','\nhi there')
mailserver.quit()