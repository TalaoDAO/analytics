To work on the mainnet, this project needs 4 permanents running services:
- main.py , that is the main file for the analytics dashboard website
- txtracker/txTrackerMain.py , that is the the file that receive from tzkt.io with a websocket the operations made by gamers on artifact and tezotops minted in the starbase (https://tezotopia.com/starbase/builder)
- txtracker/primarySalesTrackerMain.py , that is the file that receive from tzkt.io with a websocket the operations made by gamers on all others nfts in the drops space (https://tezotopia.com/marketplace/drops)
- txtracker/transactionsExecuterMain.py , that is the file that pays gamers. It receive payment from the file txtracker/model.py that is connected to the database.

To work on this project on your machine, you will need all of this python libraries:
-pytezos
-decimal
-pprint
-sys
-json
-os
-requests
-sqlite3
-traceback
-datetime
-http.client
-signalrcore.hub_connection_builder
-time
-flask
-flask_qrcode
-didkit
-redis
-socket
-uuid
-flask_mobility.decorators
-flask_mobility