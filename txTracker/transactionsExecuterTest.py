from cashBackSenderTest import cashbackSender
import modelTest as modelTest
import time
import cashBackSenderTest as cashBackSenderTest
import operationsVisualizerTest as operationsVisualizerTest
import sys

from decimal import Decimal


while True:
    payementToExecute=modelTest.getPayementPrio()
    if(payementToExecute!=None):
        print("going to pay "+str(payementToExecute))
        sys.stdout.flush()
        print(payementToExecute[0])
        sys.stdout.flush()

        if(len(payementToExecute[0])==36 or payementToExecute[0]==None):
            print(Decimal(payementToExecute[1]))
            sys.stdout.flush()
            
            hash=cashBackSenderTest.sendUNO(payementToExecute[1],payementToExecute[0])
            time.sleep(10)
            status=operationsVisualizerTest.getOperationStatus(hash)
            print("status : "+str(status))
            sys.stdout.flush()
            while(status!="applied"):
                time.sleep(10)
                status=operationsVisualizerTest.getOperationStatus(hash)
                print("status : "+str(status))
                sys.stdout.flush()
            #test balance
            modelTest.setPayementDone(payementToExecute[3],hash,"date")
    if(payementToExecute==None):
        time.sleep(3)
    
