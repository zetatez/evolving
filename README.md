# Darwin
Darwin Trading Engine.

<img src="http://latex.codecogs.com/gif.latex?S_T=S_0\int_Te^{r(t)}du"/>

## Project Structure
```bash


```

Note: Mac OS only.

- requirements
    python >= 3.8.5

- dependencies

    a. install required packages

    ```bash
    brew install cliclick
    brew install ta-lib
    brew install npm
    npm install node
    ```

    b. install and configure mongoDB

    ```bash
    brew tap mongodb/brew
    brew install mongodb-community@4.2
    
    brew services start mongodb-community
    
    mongo
    use admin
    db.createUser({user:"root",pwd:"passw0rd",roles:[{role:'root',db:'admin'}]})
    db.auth("root","passw0rd")
    
    # Configure
    cp /usr/local/etc/mongod.conf /usr/local/etc/mongod.conf.bk
    vi /usr/local/etc/mongod.conf
    # -----------------------------------
    systemLog:
      destination: file
      path: /usr/local/var/log/mongodb/mongo.log
      logAppend: true
    storage:
      dbPath: /usr/local/var/mongodb
    net:
      bindIp: 127.0.0.1
    security:
      authorization: enabled
    # -----------------------------------
    
    brew services restart mongodb-community
    
    ```

- clone project from github
    ```bash
    cd
    git clone git@github.com:zetatez/darwin.git
    cd darwin
    pip install -r requirements.txt
    ```
    
- modify configuration
    ```bash
    tree darwin/configs 
        darwin/configs
        ├── config.json
        ├── dbConfig.json
        ├── infos.md
        ├── mailConfig.json
        ├── portfolio.json
        └── stockpools.json
    ```

1. config.json
    ```json
    {
        "userid": "xxx",
        "password": "xxxxxx",
        "broker": "PAZQ",
        "broker_account": "xxxxxxxxxxxx",
        "broker_password": "xxxxxx",
        "bank_name": "工商银行",
        "bank_account": "xxxxxxxxxxxxxxxxxxx",
        "bank_password": "xxxxxx"
    }
    ```

2. dbConfig.json
    ```json
    {
        "DB": "MongoDB",
        "host": "127.0.0.1",
        "port": 27017,
        "user": "root",
        "password": "passw0rd"
    }
    ```

3. mailConfig.json
    ```json
    {
        "mail_host": "smtp.163.com",
        "mail_sender": "xxxxxxxx@163.com",
        "mail_license": "xxxxxxxx",
        "mail_receivers": ["xxxxxxxx@163.com"]
    }
    ```

## Get Start with Darwin
```python
from darwin import Service, Darwin
svc = Service()
dw = Darwin()
dw.keepInformed = True

svc.loginClient()
dw.loginBroker()

accountInfo = dw.getAccountInfo()
show(accountInfo)

status = dw.transfer(transferType = "bank2broker", amount = 100000)
show(status)

status = dw.transfer(transferType = "broker2bank", amount = 10000)
show(status)

status, contractNo = dw.issuingEntrust(stockCode = '002241', amount = 100, price = 37.01, tradingAction = 'buy')
show(status)
show(contractNo)

status, contractNo = dw.issuingEntrust(stockCode = '002241', amount = 100, price = 40.01, tradingAction = 'sell')
show(status)
show(contractNo)

status = dw.revokeAllEntrust()
show(status)

dw.logoutBroker()
svc.logoutClient()
```


## Tutorials
### Use Darwin in Scripts
- Service()
    - isClientLoggedIn()
    - loginClient()
    - logoutClient()
    - reLoginClient()
- Darwin()
    - isBrokerLoggedIn()
    - loginBroker()
    - logoutBroker()
    - getAccountInfo()
    - transfer(transferType = "bank2broker", amount = 100000)
    - transfer_bank2broker(amount = 100000)
    - transfer_broker2bank(amount = 100000)
    - getTransferRecords(dateRange = "thisWeek")
    - getAssetType(stockCode)
    - getBids(stockCode = "600030", assetType = None)
    - issuingEntrust(stockCode, amount, price = None, tradingAction = 'buy', assetType = None)
    - buy(stockCode, amount, price = None)
    - sell(stockCode, amount, price = None)
    - buyStock(stockCode, amount, price = None)
    - sellStock(stockCode, amount, price = None)
    - buySciTech(stockCode, amount, price = None)
    - sellSciTech(stockCode, amount, price = None)
    - buyGem(stockCode, amount, price = None)
    - sellGem(stockCode, amount, price = None)
    - getTodayIPO()
    - oneKeyIPO()
    - revokeEntrust(revokeType = "allBuyAndSell", assetType = "stock", contractNo = None)
    - revokeAllBuyEntrust()
    - revokeAllSellEntrust()
    - revokeAllEntrust()
    - revokeContractNoEntrust(assetType = "stock",  contractNo = "N8743678")
    - getHoldingShares(assetType = 'stock')
    - getAllHoldingShares()
    - getEntrust(assetType = 'stock', dateRange = 'today', isRevocable = True)
    - getTodayAllRevocableEntrust()
    - getClosedDeals(assetType = 'stock', dateRange = 'today')
    - getCapitalDetails(assetType = 'stock', dateRange = 'thisSeason')
    - getIPO(queryType = "entrust", dateRange = "today")
    - getIPOentrust(dateRange = "today")
    - getIPOallotmentNo(dateRange = "today")
    - getIPOwinningLots(dateRange = "today")
    - liquidating()
    - entrustPortfolio(StockCodeAmountPriceList = [])

### Build Your Timed Tasks
```python
import os
import getpass
import time
from datetime import datetime
from crontab import CronTab
from darwin import Service, Darwin
from helper import BASE_DIR

svc = Service()
dw = Darwin()

if not svc.isClientLoggedIn():
    svc.loginClient()

if not dw.isBrokerLoggedIn():
    dw.loginBroker()

# clean crontab
# -------------------------------------------
user = getpass.getuser()
cron = CronTab(user=user)
cron.remove_all(comment='darwin news')
cron.remove_all(comment='darwin reports')

cron.remove_all(comment='darwin daemon')
cron.remove_all(comment='darwin login')
cron.remove_all(comment='darwin logout')
cron.remove_all(comment='darwin relogin')
cron.remove_all(comment='darwin risk')
cron.remove_all(comment='darwin strategy')

cron.write()

## -----------------------------------------------------------
## SUPPLEMENTARY
## -----------------------------------------------------------
## news
## ---------------------------
cmd = 'nohup /Library/Frameworks/Python.framework/Versions/3.8/bin/python3 ' + os.path.join(BASE_DIR, 'darwin', 'z_cron_x_news.py') + ' >> /dev/null 2>&1 &'
job = cron.new(command=cmd, comment='darwin news')
job.minute.every(30)
cron.write()

## reports
## ---------------------------
cmd = 'nohup /Library/Frameworks/Python.framework/Versions/3.8/bin/python3 ' + os.path.join(BASE_DIR, 'darwin', 'z_cron_x_daily_closing_report.py') + ' >> /dev/null 2>&1 &'
job = cron.new(command=cmd, comment='darwin reports')
job.minute.on(0)
job.hour.on(16)
job.dow.on('MON', 'TUE', 'WED', 'THU', 'FRI')
cron.write()

## -----------------------------------------------------------
## KEY
## -----------------------------------------------------------
## daemon: check every 15 min
cmd = 'nohup /Library/Frameworks/Python.framework/Versions/3.8/bin/python3 ' + os.path.join(BASE_DIR, 'darwin', 'z_cron_service_daemon.py') + ' >> /dev/null 2>&1 &'
job = cron.new(command=cmd, comment='darwin daemon')
job.minute.every(15)
job.hour.on(9,10,11,13,14)
job.dow.on('MON', 'TUE', 'WED', 'THU', 'FRI')
cron.write()

## login
## ---------------------------
cmd = 'nohup /Library/Frameworks/Python.framework/Versions/3.8/bin/python3 ' + os.path.join(BASE_DIR, 'darwin', 'z_cron_service_daemon.py') + ' >> /dev/null 2>&1 &'
job = cron.new(command=cmd, comment='darwin login')
job.minute.on(0,3)
job.hour.on(9)
job.dow.on('MON', 'TUE', 'WED', 'THU', 'FRI')
cron.write()

## logout
## ---------------------------
cmd = 'nohup /Library/Frameworks/Python.framework/Versions/3.8/bin/python3 ' + os.path.join(BASE_DIR, 'darwin', 'z_cron_service_logoutClient.py') + ' >> /dev/null 2>&1 &'
job = cron.new(command=cmd, comment='darwin logout')
job.minute.on(3)
job.hour.on(15)
job.dow.on('MON', 'TUE', 'WED', 'THU', 'FRI')
cron.write()

## relogin every 20 min to clear error
## ---------------------------
cmd = 'nohup /Library/Frameworks/Python.framework/Versions/3.8/bin/python3 ' + os.path.join(BASE_DIR, 'darwin', 'z_cron_service_relogin.py') + ' >> /dev/null 2>&1 &'
job = cron.new(command=cmd, comment='darwin relogin')
job.minute.every(20)
job.hour.on(9,10,11,13,14)
job.dow.on('MON', 'TUE', 'WED', 'THU', 'FRI')
cron.write()

## risk
## ---------------------------
cmd = 'nohup /Library/Frameworks/Python.framework/Versions/3.8/bin/python3 ' + os.path.join(BASE_DIR, 'darwin', 'risk.py') + ' >> /dev/null 2>&1 &'
job = cron.new(command=cmd, comment='darwin risk')
job.minute.every(5)
job.hour.on(9,10,11,13,14)
job.dow.on('MON', 'TUE', 'WED', 'THU', 'FRI')
cron.write()

## strategies
# ---------------------------
cmd = 'nohup /Library/Frameworks/Python.framework/Versions/3.8/bin/python3 ' + os.path.join(BASE_DIR, 'darwin', 'z_cron_001.py') + ' >> /dev/null 2>&1 &'
job = cron.new(command=cmd, comment='darwin strategy')
job.minute.on(10)
job.hour.on(9)
job.dow.on('MON', 'TUE', 'WED', 'THU', 'FRI')
cron.write()

cmd = 'nohup /Library/Frameworks/Python.framework/Versions/3.8/bin/python3 ' + os.path.join(BASE_DIR, 'darwin', 'z_cron_002.py') + ' >> /dev/null 2>&1 &'
job = cron.new(command=cmd, comment='darwin strategy')
job.minute.on(10)
job.hour.on(9)
job.dow.on('MON', 'TUE', 'WED', 'THU', 'FRI')
cron.write()
```

### Use Darwin Command Line


- Darwin shell
```bash
 ./darwin -h

        # NAME:
        #         darwin

        # SYNOPSIS:
        #         darwin -u userid -p password
        #         darwin -u userid -p password -k
        #         darwin -[qsjh]

        # OPTIONS:
        #         -u  userid
        #         -p  password
        #         -q  quit client
        #         -s  start darwin shell
        #         -h  help

        # AUTHOR:
        #         F. F
        #         Email: fromfairest@icloud.com

        # Ex:
        #         1. To login client
        #                 darwin -u userid -p password

        #         2. To logout client
        #                 darwin -q

        #         3. To use darwin shell
        #                 darwin -s

        #         4. login client, start darwin shell
        #                 darwin -u userid -p password -s

# to login in client
./darwin -u <useid> -p <password>

# to start darwin shell
./darwin -s
    # 16:34:46: savvy . .. ...
    # Python 3.8.5 (v3.8.5:580fbb018f, Jul 20 2020, 12:11:27) 
    # Type 'copyright', 'credits' or 'license' for more information
    # IPython 7.17.0 -- An enhanced Interactive Python. Type '?' for help.

    # ## SAVVY SHELL:

    # import os
    # import sys
    # import time
    # from datetime import datetime
    # import numpy as np
    # import pandas as pd
    # from matplotlib.pyplot import *
    # from pprint import pprint as show
    # from darwin import Tlog, Service, Darwin, DarwinSim
    # from helper import BASE_DIR, Config, Msg, Mail, Logging


```









