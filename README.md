# Evolving
Trading engine `evolving`. Only Mac OSX is supported.

<img src="http://latex.codecogs.com/gif.latex?S_T=S_0\int_Te^{r(t)}du"/>


## INSTALLATION GUIDE
- PROJECT STRUCTURE
    ```bash
    tree evolving 
        evolving
        ├── LICENSE
        ├── README.md
        ├── evolving
        │   ├── __init__.py
        │   ├── ascmds.py
        │   ├── evolving.py
        │   └── helper.py
        ├── requirements.txt
        ├── setup.py
        └── tests
            ├── __init__.py
            ├── evolving.py
            └── helper.py

    tree ~/.config/evolving
        ~/.config/evolving
        └── config.xml
    ```

- REQUIREMENTS
    python >= 3.8.5

- DEPENDENCIES
    ```bash
    brew install cliclick
    cliclick -V             # cliclick 4.0.1, 2018-04-10
    which cliclick          # /usr/local/bin/cliclick

    pip install `curl -fsSL https://raw.githubusercontent.com/zetatez/evolving/main/requirements.txt`
    ```

- Building `evolving` from pip
    ```bash
    pip install evolving
    ```

- Building `evolving` from source
    ```bash
    git clone git@github.com:zetatez/evolving.git ~/evolving; cd ~/evolving; python setup.py install
    ```
    
- CONFIGURATION
    ```bash
    mkdir -p ~/.config/evolving

    echo """
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
    """ > ~/.config/evolving/config.xml
    ```

## GET START WITH `evolving`
    ```python

    import evolving.evolving as evo
    from pprint import pprint as show

    s = evo.Service()
    e = evo.Evolving()

    status = s.loginClient()
    print(status)

    e.keepInformed = True

    status = e.isBrokerLoggedIn()
    print(status)

    status = e.loginBroker()
    print(status)

    status = e.isBrokerLoggedIn()
    print(status)

    accountInfo = e.getAccountInfo()
    show(accountInfo)

    status = e.transfer(transferType = "bank2broker", amount = 1000)
    show(status)

    status = e.transfer(transferType = "broker2bank", amount = 1000)
    show(status)

    status = e.transfer_broker2bank(amount = 10000)
    show(status)

    status = e.transfer_bank2broker(amount = 10000)
    show(status)

    transferRecords = e.getTransferRecords(dateRange = "thisYear")
    show(transferRecords)

    bids = e.getBids(stockCode = "600030")
    show(bids)
    bids = e.getBids(stockCode = "600030", assetType = 'stock')
    show(bids)

    bids = e.getBids(stockCode = "688055")
    show(bids)
    bids = e.getBids(stockCode = "688055", assetType = 'sciTech')
    show(bids)

    bids = e.getBids(stockCode = "300750")
    show(bids)
    bids = e.getBids(stockCode = "300750", assetType = 'gem')
    show(bids)

    status, contractNo = e.issuingEntrust(stockCode = '002241', amount = 100, price = 37.01, tradingAction = 'buy')
    show(status)
    show(contractNo)
    status, contractNo = e.issuingEntrust(stockCode = '002241', amount = 100, price = 40.01, tradingAction = 'sell')
    show(status)
    show(contractNo)
    status, contractNo = e.issuingEntrust(stockCode = '002241', amount = 100, tradingAction = 'buy')
    show(status)
    show(contractNo)
    status, contractNo = e.issuingEntrust(stockCode = '002241', amount = 100, tradingAction = 'sell')
    show(status)
    show(contractNo)

    status, contractNo = e.issuingEntrust(stockCode = '688050', amount = 200, price = 220.01, tradingAction = 'buy')
    show(status)
    show(contractNo)
    status, contractNo = e.issuingEntrust(stockCode = '688050', amount = 200, price = 225.01, tradingAction = 'sell')
    show(status)
    show(contractNo)
    status, contractNo = e.issuingEntrust(stockCode = '688050', amount = 200, tradingAction = 'buy')
    show(status)
    show(contractNo)
    status, contractNo = e.issuingEntrust(stockCode = '688050', amount = 200, tradingAction = 'sell')
    show(status)
    show(contractNo)

    status, contractNo = e.issuingEntrust(stockCode = '300474', amount = 200, price = 72.54, tradingAction = 'buy')
    show(status)
    show(contractNo)
    status, contractNo = e.issuingEntrust(stockCode = '300474', amount = 200, price = 78.41, tradingAction = 'sell')
    show(status)
    show(contractNo)
    status, contractNo = e.issuingEntrust(stockCode = '300474', amount = 200, tradingAction = 'buy')
    show(status)
    show(contractNo)
    status, contractNo = e.issuingEntrust(stockCode = '300474', amount = 200, tradingAction = 'sell')
    show(status)
    show(contractNo)

    status, contractNo = e.buy(stockCode = '002241', amount = 100)
    show(status)
    show(contractNo)
    status, contractNo = e.buy(stockCode = '002241', amount = 100, price = 37.01)
    show(status)
    show(contractNo)
    status, contractNo = e.buy(stockCode = '688050', amount = 200, price = 220.01)
    show(status)
    show(contractNo)
    status, contractNo = e.buy(stockCode = '300474', amount = 200, price = 72.54)
    show(status)
    show(contractNo)

    status, contractNo = e.sell(stockCode = '002241', amount = 100)
    show(status)
    show(contractNo)
    status, contractNo = e.sell(stockCode = '002241', amount = 100, price = 37.01)
    show(status)
    show(contractNo)
    status, contractNo = e.sell(stockCode = '688050', amount = 200, price = 220.01)
    show(status)
    show(contractNo)
    status, contractNo = e.sell(stockCode = '300474', amount = 200, price = 72.54)
    show(status)
    show(contractNo)

    status, contractNo = e.buyStock(stockCode = '002241', amount = 100, price = 37.01)
    show(status)
    show(contractNo)
    status, contractNo = e.sellStock(stockCode = '002241', amount = 100, price = 40.01)
    show(status)
    show(contractNo)
    status, contractNo = e.buyStock(stockCode = '002241', amount = 100)
    show(status)
    show(contractNo)
    status, contractNo = e.sellStock(stockCode = '002241', amount = 100)
    show(status)
    show(contractNo)

    status, contractNo = e.buySciTech(stockCode = '688050', amount = 200, price = 225.01)
    show(status)
    show(contractNo)
    status, contractNo = e.sellSciTech(stockCode = '688050', amount = 200, price = 220.01)
    show(status)
    show(contractNo)
    status, contractNo = e.buySciTech(stockCode = '688050', amount = 200)
    show(status)
    show(contractNo)
    status, contractNo = e.sellSciTech(stockCode = '688050', amount = 200)
    show(status)
    show(contractNo)

    status, contractNo = e.buyGem(stockCode = '300474', amount = 200, price = 72.54)
    show(status)
    show(contractNo)
    status, contractNo = e.sellGem(stockCode = '300474', amount = 200, price = 78.41)
    show(status)
    show(contractNo)
    status, contractNo = e.buyGem(stockCode = '300474', amount = 200)
    show(status)
    show(contractNo)
    status, contractNo = e.sellGem(stockCode = '300474', amount = 200)
    show(status)
    show(contractNo)

    todayIPO = e.getTodayIPO()
    show(todayIPO)

    status = e.oneKeyIPO()
    print(status)

    status = e.revokeEntrust(revokeType = "allBuyAndSell", assetType = "stock", contractNo = None)
    show(status)
    status = e.revokeEntrust(revokeType = "allBuy", assetType = "stock", contractNo = None)
    show(status)
    status = e.revokeEntrust(revokeType = "allSell", assetType = "stock", contractNo = None)
    show(status)

    status = e.revokeContractNoEntrust(assetType = "stock",  contractNo = "N8536587")
    show(status)

    status = e.revokeAllEntrust()
    show(status)
    status = e.revokeAllBuyEntrust()
    show(status)
    status = e.revokeAllSellEntrust()
    show(status)

    holdingShares = e.getHoldingShares(assetType = 'stock')
    show(holdingShares)

    allholdingShares = e.getAllHoldingShares()
    show(allholdingShares)

    entrust = e.getEntrust(assetType = 'stock', dateRange = 'today', isRevocable = True)
    show(entrust)

    entrust = e.getEntrust(assetType = 'stock', dateRange = 'today', isRevocable = False)
    show(entrust)

    entrust = e.getEntrust(assetType = 'stock', dateRange = 'thisWeek', isRevocable = False)
    show(entrust)
    print(len(entrust.get('data')))

    entrust = e.getEntrust(assetType = 'stock', dateRange = 'thisYear', isRevocable = False)
    show(entrust)

    res = e.getTodayAllRevocableEntrust()
    show(res)

    closedDeals = e.getClosedDeals(assetType = 'stock', dateRange = 'thisSeason')
    show(closedDeals)

    closedDeals = e.getClosedDeals(assetType = 'stock', dateRange = 'today')
    show(closedDeals)

    capitalDetails = e.getCapitalDetails(assetType = 'stock', dateRange = 'thisSeason')
    show(capitalDetails)

    capitalDetails = e.getCapitalDetails(assetType = 'stock', dateRange = 'today')
    show(capitalDetails)

    res = e.getIPO(queryType = "entrust", dateRange = "today")
    show(res)

    res = e.getIPO(queryType = "allotmentNo", dateRange = "thisMonth")
    show(res)

    res = e.getIPO(queryType = "winningLots", dateRange = "thisSeason")
    show(res)

    status = e.liquidating()
    show(status)

    StockCodeAmountPriceList = [['512290', '1000', '2.169'], ['512290', '1000', '2.171'], ['688050', '200', '225.01']]
    statusList = e.entrustPortfolio(StockCodeAmountPriceList)
    show(statusList)

    status = e.revokeAllEntrust()
    show(status)

    s.logoutClient()
    ```


## API
- Service
    - isClientLoggedIn()
    - loginClient()
    - logoutClient()
    - reLoginClient()

- Evolving
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

- EvolvingSim
    - getAccountInfo()
    - issuingEntrust(stockCode, amount, price = None, tradingAction = 'buy')
    - buy(stockCode, amount, price = None)
    - sell(stockCode, amount, price = None)
    - revokeEntrust(revokeType = "allBuyAndSell", contractNo = None)
    - getHoldingShares()
    - getEntrust(dateRange = 'today', isRevocable = True)
    - getClosedDeals(dateRange = 'today')
    - getCapitalDetails(dateRange = 'thisSeason')
    - liquidating()
    - entrustPortfolio(stockCodeAmountPriceList = [])

