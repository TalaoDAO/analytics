3 services make analytics work:

- analytics.service, the flask server used for the ui. The file for this service is analytics/main.py

- txTracker.service, the service tracking transactions of players having a valid voucher. This service update the db.  The file for this service is analytics/txTracker/txTracker.py

- transactionsExecuter.service, the service paying players and affiliates.  The file for this service is analytics/txTracker/transactionsExecuter.py . This service uses a pile/stack of paiements waiting to pay players in order. 