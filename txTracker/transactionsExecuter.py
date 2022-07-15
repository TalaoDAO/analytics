from cashBackSender import cashbackSender
import model
import time
import cashBackSender
import operationsVisualizer
import sys



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
        
        model.setPayementDone(payementToExecute[3],hash,"date")
    if(payementToExecute==None):
        time.sleep(3)
    