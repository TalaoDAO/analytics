import cashBackSenderMain
import modelMain
import time
import operationsVisualizerMain
import logging
logging.basicConfig(level=logging.INFO)
import message
import os 
import json

script_dir = os.path.dirname(__file__)
script_dir = os.path.dirname(script_dir)
file_path = os.path.join(script_dir, 'keys.json')

with open(file_path) as mon_fichier:
    data = json.load(mon_fichier)
    smtp_password = data["smtp_password"]

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
            message_text = str(payementToExecute[1])+" "+payementToExecute[4]+" sent for cashback. https://tzkt.io/" +str(payementToExecute[3])
            message.message("New Tezotopia transaction", "thierry@altme.io", message_text, smtp_password)
            message.message("New Tezotopia transaction", "hugo@altme.io", message_text, smtp_password)
    else :
        time.sleep(3)
    
