import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

SMTP_SERVER = 'mail.server'
SMTP_PORT = 587

user_name = 'my_mail'
password = 'pswd'

sender_address = 'my_mail'
reciever_adress = 'your_mail'

smtpObj = smtplib.SMTP(host=SMTP_SERVER, port=SMTP_PORT)
smtpObj.starttls()
smtpObj.login(user=user_name, password=password)

msg = MIMEMultipart('alternative')
msg['Subject'] = "Link"
msg['From'] = sender_address
msg['To'] = reciever_adress

html = """\
<html>
  <head></head>
  <body>
    <p>Hi!<br>
       How are you?<br>
       Here is the <a href="http://www.python.org">link</a> you wanted.
    </p>
  </body>
</html>
"""

part2 = MIMEText(html, 'html')
msg.attach(part2)


smtpObj.sendmail(from_addr=sender_address,
                     to_addrs=reciever_adress,
                     msg=msg.as_string())
# except:
#     try:
#         smtpObj.sendmail('a.m@novascientia.net', 'a.m@novascientia.net',
#                          'Subject: Test\nautomated mail')
#     except:
#         pass
smtpObj.close()


