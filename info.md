3 services make analytics work:

- analytics.service, the flask server used for the ui. The file for this service is analytics/main.py

- txTracker.service, the service tracking transactions of players having a valid voucher. This service update the db.  The file for this service is analytics/txTracker/txTracker.py

- transactionsExecuter.service, the service paying players and affiliates.  The file for this service is analytics/txTracker/transactionsExecuter.py . This service uses a pile/stack of paiements waiting to pay players in order. 

Si un gamer a un voucher actif et qu'on lui ajoute un nouveau voucher, c'est le plus ancien voucher actif qui sera appliqué. 

Si besoin de réinitialiser la base (pour tester un nouveau voucher avec une même adresse par exemple), arrêter chaque service avec ces commandes :

sudo systemctl stop analytics.service
sudo systemctl stop txTracker.service
sudo systemctl stop transactionsExecuter.service

puis supprimer /home/achille/analytics/database.db

et relancer chaque service 

sudo systemctl start analytics.service
sudo systemctl start txTracker.service
sudo systemctl start transactionsExecuter.service

et lancer le fichier model.py

python3 /home/achille/analytics/txTracker/model.py



