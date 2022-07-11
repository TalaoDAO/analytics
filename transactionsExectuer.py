from cashBackSender import cashbackSender
import model
import time
import cashBackSender
import operationsVisualizer
while True: #test if there is payement to execute
    payementToExecute=model.getPayementPrio() #the db tell us wich payement execute
    if(payementToExecute!=None):
        print("going to pay "+str(payementToExecute))
        hash=cashBackSender.cashbackSender(payementToExecute[1],payementToExecute[0])
        time.sleep(10)
        status=operationsVisualizer.getOperationStatus(hash)
        print("status : "+str(status))
        while(status!="applied"):#test each 10 seconds if the transaction is applied because we only can send 1 transaction per block
            time.sleep(10)
            status=operationsVisualizer.getOperationStatus(hash)
            print("status : "+str(status))
        model.setPayementDone(payementToExecute[3],hash,"date")
    if(payementToExecute==None):
        time.sleep(3)
    
