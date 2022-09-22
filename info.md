4 services make analytics works on the MAINNET:

- analytics.service, the flask server used for the ui. The file for this service is analytics/main.py

- txTrackerMain.service, the service tracking transactions of players having a valid voucher. This service update the db.  The file for this service is analytics/txTracker/txTracker.py

- primarySalesTrackerMain.service, the service tracking transactions of players having a valid voucher. This service update the db.  The file for this service is analytics/txTracker/primarySalesTrackerMain.py

- transactionsExecuterMain.service, the service paying players and affiliates.  The file for this service is analytics/txTracker/transactionsExecuterMain.py . This service uses a pile/stack of paiements waiting to pay players in order. 

If a gamer has a valid voucher and a new one is added for him, the one with the biggest discount will be applied.



