from cashBackSender import cashbackSender
import model
import time
import cashBackSender
import operationsVisualizer
while True:
    payementToExecute=model.getPayementPrio()
    if(payementToExecute!=None):
        print("going to pay "+str(payementToExecute))
        hash=cashBackSender.cashbackSender(payementToExecute[1],payementToExecute[0])
        time.sleep(10)
        status=operationsVisualizer.getOperationStatus(hash)
        print("status : "+str(status))
        while(status!="applied"):
            time.sleep(10)
            status=operationsVisualizer.getOperationStatus(hash)
            print("status : "+str(status))
        model.setPayementDone(payementToExecute[3],hash,"date")

    
