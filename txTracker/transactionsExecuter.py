from cashBackSender import cashbackSender
import model
import time
import cashBackSender
import operationsVisualizer
import sys
import smtplib

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_USERNAME = "talao.analytics@gmail.com"
SMTP_PASSWORD = "Talao123"
EMAIL_FROM = "talao.analytics@gmail.com"
EMAIL_TO = "achillemarseille@gmail.com"
EMAIL_SUBJECT = "Attention: 50 xtz left"
EMAIL_MESSAGE = "The message here"


while True:
    payementToExecute=model.getPayementPrio()
    if(payementToExecute!=None):
        print("going to pay "+str(payementToExecute))
        sys.stdout.flush()
        hash=cashBackSender.cashbackSender(payementToExecute[1],payementToExecute[0])
        time.sleep(10)
        status=operationsVisualizer.getOperationStatus(hash)
        print("status : "+str(status))
        sys.stdout.flush()
        while(status!="applied"):
            time.sleep(10)
            status=operationsVisualizer.getOperationStatus(hash)
            print("status : "+str(status))
            sys.stdout.flush()
        #test balance
        s = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        s.starttls()
        s.login(SMTP_USERNAME, SMTP_PASSWORD)
        message = 'Subject: {}\n\n{}'.format(EMAIL_SUBJECT, EMAIL_MESSAGE)
        s.sendmail(EMAIL_FROM, EMAIL_TO, message)
        s.quit()

        model.setPayementDone(payementToExecute[3],hash,"date")
    if(payementToExecute==None):
        time.sleep(3)
    
