
'''
1. Go to following link:
    https://www.google.com/settings/security/lesssecureapps?rfn=27&rfnc=1&et=0&asae=2&anexp=ire-control
2. Turn on access
3. Download file from drive
4. Enter password
5. Modify message
6. Run this script
7. Go back to above link and turn off access
Currently supported for Gmail sender
Note: This program contains parts taken from various blogs on the web. I do not claim this as my original work.
'''

import smtplib
from os.path import basename
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formatdate
from email.MIMEBase import MIMEBase
from email import Encoders

def send_email(server, user, recipient, subject, body,files=None):
  FROM = user
  TO = recipient
  SUBJECT = subject
  TEXT = body

  # Prepare actual message
  message=MIMEMultipart()
  message['From']=FROM
  message['TO']=TO
  message['Date']=formatdate(localtime=True)
  message['Subject']=SUBJECT
  message.attach(MIMEText(TEXT))
  #message.attach(MIMEText(TEXT))
  for f in files or []:
    print f
    part = MIMEBase('application', "octet-stream")
    part.set_payload( open(f,"rb").read() )
    Encoders.encode_base64(part)
    part.add_header('Content-Disposition', 'attachment; filename="%s"' % basename(f))
    message.attach(part)
  try:
    server.sendmail(FROM, TO, message.as_string())
    print 'successfully sent the mail to ',TO
  except:
    print "failed to send mail to ",TO

def makeConnection(user,pwd):
  try:
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.ehlo()
    server.starttls()
    server.login(user, pwd)
    return server
  except:
    print "Failed to make connection"
    return 0

user       = "<account from which email to be sent>" #Adviced to make a separate account
pwd        = "<password123456>" #Enter password
subject    ="ML Log" #Enter subject of email
server     = makeConnection(user,pwd)
attachment = ["sample_log1","sample_log2"] #Name of log files
if server:
  print attachment
  recipientName  = "<Your_name>"
  recipientEmail = "<Your_email_address>"
  recipient      = recipientEmail
  body           = "Hi {0},\nLogs for ___ run attached.\nRegards,\nAlfred".format(str(recipientName)) #Enter message body here
  send_email(server,user,recipient,subject,body,attachment)
  server.close()