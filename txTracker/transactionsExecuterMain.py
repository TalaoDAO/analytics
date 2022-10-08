import cashBackSenderMain
import modelMain
import time
import operationsVisualizerMain
import logging
logging.basicConfig(level=logging.INFO)


while True:
    payementToExecute=modelMain.getPayementPrio()
    if payementToExecute :
        logging.info("going to pay %s", str(payementToExecute))
        logging.info(payementToExecute[0])
        if len(payementToExecute[0])==36 or not payementToExecute[0] :
            hash=""
            if payementToExecute[4]=="UNO" :  
                hash=cashBackSenderMain.sendUNO(payementToExecute[1],payementToExecute[0])
            elif payementToExecute[4]=="XTZ" :
                hash=cashBackSenderMain.cashbackSender(payementToExecute[1],payementToExecute[0])
            else :
                logging.info("currency = %s", payementToExecute[4] )
            time.sleep(10)
            status=operationsVisualizerMain.getOperationStatus(hash)
            logging.info("status = %s", str(status))
            while status != "applied" :
                time.sleep(10)
                status=operationsVisualizerMain.getOperationStatus(hash)
                logging.info("status = %s", str(status))
            #test balance
            modelMain.setPayementDone(payementToExecute[3],hash,"date")
    else :
        time.sleep(3)
    
