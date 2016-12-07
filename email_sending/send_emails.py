import smtplib

SMTP_SERVER = 'mail.netsteps.gr'
SMTP_PORT = 587

user_name = 'a.m@novascientia.net'
password = '$M1Aqzecx'

sender_address = 'a.m@novascientia.net'
reciever_adress = 'a.m@novascientia.net'

smtpObj = smtplib.SMTP(host=SMTP_SERVER, port=SMTP_PORT)
smtpObj.starttls()
smtpObj.login(user=user_name, password=password)

reciever_name = 'Rene Woszidlo'
reciever_work = 'Boeing'


subject = 'Subject: Nova-Patent\n'
message_body = 'Dear ' + reciever_name
try:
    smtpObj.sendmail(from_addr=sender_address,
                     to_addrs=reciever_adress,
                     msg='Subject: Test!!!\nautomated mail')
except:
    try:
        smtpObj.sendmail('a.m@novascientia.net', 'a.m@novascientia.net',
                         'Subject: Test\nautomated mail')
    except:
        pass
smtpObj.close()


