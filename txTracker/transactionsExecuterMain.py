import cashBackSenderMain
import modelMain
import time
import cashBackSenderMain
import operationsVisualizerMain
import sys

from decimal import Decimal


while True:
    payementToExecute=modelMain.getPayementPrio()
    if(payementToExecute!=None):
        print("going to pay "+str(payementToExecute))
        sys.stdout.flush()
        print(payementToExecute[0])
        sys.stdout.flush()

        if(len(payementToExecute[0])==36 or payementToExecute[0]==None):
            print(Decimal(payementToExecute[1]))
            sys.stdout.flush()
            hash=""
            if(payementToExecute[4]=="UNO"):
                hash=cashBackSenderMain.sendUNO(payementToExecute[1],payementToExecute[0])
            if(payementToExecute[4]=="XTZ"):
                hash=cashBackSenderMain.cashbackSender(payementToExecute[1,payementToExecute[0]])
            time.sleep(10)
            status=operationsVisualizerMain.getOperationStatus(hash)
            print("status : "+str(status))
            sys.stdout.flush()
            while(status!="applied"):
                time.sleep(10)
                status=operationsVisualizerMain.getOperationStatus(hash)
                print("status : "+str(status))
                sys.stdout.flush()
            #test balance
            modelMain.setPayementDone(payementToExecute[3],hash,"date")
    if(payementToExecute==None):
        time.sleep(3)
    
