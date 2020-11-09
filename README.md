# EVOLVING
TRADING ENGINE `evolving`. MacOSX ONLY.
<img src="http://latex.codecogs.com/gif.latex?S_T=S_0\int_Te^{r(t)}du"/>

## PROJECT STRUCTURE
```bash
tree evolving 
    # evolving
    # ├── LICENSE
    # ├── README.md
    # ├── evolving
    # │   ├── __init__.py
    # │   ├── ascmds.py
    # │   ├── evolving.py
    # │   └── helper.py
    # ├── requirements.txt
    # ├── setup.py
    # └── tests
    #     ├── __init__.py
    #     ├── evolving.py
    #     └── helper.py

tree ~/.config/evolving
    # /Users/xxxx/.config/evolving
    # └── config.xml
```

- REQUIREMENTS
    python >= 3.8.5

- DEPENDENCIES
    ```bash
    brew install cliclick
    cliclick -V
        # cliclick 4.0.1, 2018-04-10
    which cliclick
        # /usr/local/bin/cliclick
    ```

- CLONE PROJECT FROM GITHUB
    ```bash
    cd; git clone git@github.com:zetatez/evolving.git; cd evolving; pip install -r requirements.txt
    ```
    
- CONFIGURATION
    ```bash
    cd; mkdir -p .config/evolving; cd ~/.config/evolving; touch config.xml
    vi config.xml
    # -------------------
    <evolving>
        <trading>
            <userid>77777777777</userid>
            <password>123456</password>
            <broker_code>PAZQ</broker_code>
            <broker_account>66666666</broker_account>
            <broker_password>123456</broker_password>
            <bank_name>工商银行</bank_name>
            <bank_account>666666666666666666</bank_account>
            <bank_password>123456</bank_password>
        </trading>
        <mail>
            <mail_host>smtp.163.com</mail_host>
            <mail_sender>mailAddress@163.com</mail_sender>
            <mail_license>SNRRQOKFKEUNNSFT</mail_license>
            <mail_receivers>mailAddress@163.com</mail_receivers>
        </mail>
    </evolving>
    # -------------------
    ```

## GET START WITH `evolving`
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
