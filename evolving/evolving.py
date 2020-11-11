# -*- coding: utf-8 -*-

import abc, os, sys, json, time
from pprint import pprint as show
from . import ascmds
from . import helper

class Lock(object):
    """ Lock: lock maintainer
    """
    def __init__(self):
        self._lockFilePath = os.path.join('/tmp/', 'lock.json')
        self.unlock()

    def lock(self):
        try:
            info = {"lock": 1}
            s = json.dumps(info, ensure_ascii=False, sort_keys=True, indent = 4)                
            with open(self._lockFilePath, 'w+') as fh:
                fh.write(s)
            return True
        except Exception:
            return False

    def unlock(self):
        try:
            info = {"lock": 0}
            s = json.dumps(info, ensure_ascii=False, sort_keys=True, indent = 4)                
            with open(self._lockFilePath, 'w+') as fh:
                fh.write(s)
            return True
        except Exception:
            return False

    def requestLock(self):
        def islocked():
            islock = 0
            with open(self._lockFilePath, 'r', encoding='utf8') as fp:
                islock = json.load(fp).get("lock")
            return islock

        islock = islocked()
        tolerance = 15    # 15 sec
        elapsedTime = 0
        delta = 0.05
        while islock and elapsedTime < tolerance:
            time.sleep(delta)
            elapsedTime += delta
            islock = islocked()
        if islock:
            return False
        self.lock()
        return True

class Service(object):
    """ THS service. up and down daemons, login client, logout client, is client logged in
    """
    def __init__(self):
        self._config = helper.Config()
        self.__logging = helper.Logging(logType='service')
        self.__lock = Lock()

    def isClientLoggedIn(self):
        """ is client logged in: 选择不加锁, 加不加锁都会产生影响
        Args:
        Returns:
            True/False
        Raises:
        """
        status = False
        cmd = ascmds.asisClientLoggedIn
        res = os.popen(cmd).read().strip()
        if res == "true":
            status = True
        return status

    def loginClient(self):
        """ login client
        Args:
        Returns:
            True/False
        Raises:
        """
        status = False

        res = 'failed'
        if self.isClientLoggedIn():
            res = "successed"
        else:
            cmd = ascmds.asloginClient + ' ' + self._config.userid + ' ' + self._config.password
            res = os.popen(cmd).read().strip()

        if res == "successed":
            self.__logging.info("login client: " + res)
            status = True
            self.__lock.unlock()
        else:
            self.__logging.error("login client: " + res)
        return status

    def logoutClient(self):
        """ logout client
        Args:
        Returns:
            True/False
        Raises:
        """
        cmd = ascmds.aslogoutClient
        res = os.popen(cmd).read().strip()

        status = False
        if res == "successed":
            self.__logging.info("logout client: " + res)
            status = True
            self.__lock.lock()
        else:
            self.__logging.error("logout client: " + res)
        return status

    def reLoginClient(self):
        """ relogin client
        Args:
        Returns:
            True/False
        Raises:
        """
        self.logoutClient()
        time.sleep(1)
        return self.loginClient()

class Base(metaclass = abc.ABCMeta):
    def __init__(self):
        self._config = helper.Config()
        
    @abc.abstractmethod
    def isBrokerLoggedIn(self):
        pass

    @abc.abstractmethod
    def loginBroker(self):
        pass

    @abc.abstractmethod
    def logoutBroker(self):
        pass

    @abc.abstractmethod
    def getAccountInfo(self):
        pass

    @abc.abstractmethod
    def transfer(self):
        pass

    @abc.abstractmethod
    def issuingEntrust(self):
        pass

    @abc.abstractmethod
    def buy(self):
        pass

    @abc.abstractmethod
    def sell(self):
        pass

    @abc.abstractmethod
    def oneKeyIPO(self):
        pass

class Evolving(Base):
    """ Evolving: trading engine
    """
    def __init__(self):
        super(Evolving, self).__init__()
        self.__logging = helper.Logging(logType = 'env_prod')
        self.__keepInformed = False                             # mail me
        self.__lock = Lock()
        
    @property
    def keepInformed(self):
        return self.__keepInformed

    @keepInformed.setter
    def keepInformed(self, val = True):
        self.__keepInformed = val

    def isBrokerLoggedIn(self):
        """ is broker logged in
        Args:
        Returns:
            True/False
        Raises:
        """
        status = False
        if not self.__lock.requestLock():
            return status

        cmd = ascmds.asisBrokerLoggedIn + ' ' + self._config.broker_code + ' ' + self._config.broker_account + ' ' + self._config.broker_password
        res = os.popen(cmd).read().strip()
        status = True if res == "true" else False
        self.__lock.unlock()
        return status

    def loginBroker(self):
        """ loggin broker
        Args:
        Returns:
            True/False
        Raises:
        """
        status = False
        if not self.__lock.requestLock():
            return status

        cmd = ascmds.asloginBroker + ' ' + self._config.broker_code + ' ' + self._config.broker_account + ' ' + self._config.broker_password
        res = os.popen(cmd).read().strip()
        if res == "successed":
            self.__logging.info("login broker: " + res)
            status = True
        else:
            self.__logging.error("login broker: " + res)
        self.__lock.unlock()
        return status

    def logoutBroker(self):
        """ logout broker
        Args:
        Returns:
            True/False
        Raises:
        """
        status = False
        if not self.__lock.requestLock():
            return status

        cmd = ascmds.aslogoutBroker
        res = os.popen(cmd).read().strip()
        if res == "successed":
            self.__logging.info("logout broker: " + res)
            status = True
        else:
            self.__logging.error("login broker: " + res)
        self.__lock.unlock()
        return status

    def getAccountInfo(self):
        """
        Args:
        Returns:
            info = {
                    'data': {
                        '可取金额': 'xx',
                        '可用金额': ',
                        '当日盈亏': '--',
                        '总市值': 'xx',
                        '总盈亏': 'xx',
                        '总资产': 'xx',
                        '账户设置': 'xx',
                        '资金余额': 'xx',
                        '银证转账': 'xx',
                        '风险测评': 'xx'
                    },
                    'info': None,
                    'status': True}
        Raises:
        """
        accountInfo = {}
        if not self.__lock.requestLock():
            return accountInfo

        try:
            cmd = ascmds.asgetAccountInfo
            res = os.popen(cmd).read().strip()
            ls = [x.strip() for x in res.split(',')]
            flag = ls.pop(0)
            if flag == "successed":
                accountInfo.update({'status': True})
            else:
                accountInfo.update({'status': False})

            doc = {}
            if accountInfo.get("status"):
                while len(ls)>1:
                    doc.update({ls.pop(0): ls.pop(0)})
                accountInfo.update({'data': doc})
                accountInfo.update({'info': None})
                self.__logging.info("get account info successed")
            else:
                accountInfo.update({'status': False})
                accountInfo.update({'data': doc})
                accountInfo.update({'info': ' '.join(ls)})
                self.__logging.error("get account info failed: " + accountInfo.get('info'))
        except Exception as e:
            self.__logging.error("get account info failed: " + str(e))
        self.__lock.unlock()
        return accountInfo


    def transfer(self, transferType = "bank2broker", amount = 100000):
        """ transfer
        Args:
            transferType: "bank2broker", "broker2bank"
            amount:
        Returns:
            True/False
        Raises:
        """
        def mailMe(action = '', assetsName = '', assetsCode = '', price = '', amount = '', status = '', comments = ''):
            try:
                if self.__keepInformed:
                    tlog = helper.Tlog(action = action, assetsName = assetsName, assetsCode = assetsCode, price = price, amount = amount, status = status, comments = comments)
                    helper.Mail(tlog)
            except Exception as e:
                self.__logging.error("mailing failed with error: " + str(e))
            return

        status = False
        if not self.__lock.requestLock():
            return status

        try:
            cmd = ascmds.astransfer + ' ' + transferType + ' ' + str(amount) + ' ' + self._config.bank_password + ' ' + self._config.broker_password
            res = os.popen(cmd).read().strip()
            ls = [x.strip() for x in res.split(',')]

            flag = ls.pop(0)
            info = None
            if flag == "successed":
                status = True
                self.__logging.info("transfer successed: " + transferType + ' ' + str(amount))
                mailMe(action = "transfer", assetsName = transferType, assetsCode = '', price = '', amount = amount, status = "successed")
            else:
                info = ' '.join(ls)
                self.__logging.error("transfer failed: " + transferType + ' ' + str(amount) + '. Err: ' + info)
                mailMe(action = "transfer", assetsName = transferType, assetsCode = '', price = '', amount = amount, status = "failed")
        except Exception as e:
            self.__logging.error("transfer failed: " + transferType + ' ' + str(amount) + '. Err: ' + str(e))
            mailMe(action = "transfer", assetsName = transferType, assetsCode = '', price = '', amount = amount, status = "failed")
        self.__lock.unlock()
        return status

    def transfer_bank2broker(self, amount = 100000):
        """ transfer
        Args:
            amount:
        Returns:
            True/False
        Raises:
        """
        return self.transfer(transferType = "bank2broker", amount = amount)

    def transfer_broker2bank(self, amount = 100000):
        """ transfer
        Args:
            amount:
        Returns:
            True/False
        Raises:
        """
        return self.transfer(transferType = "broker2bank", amount = amount)

    def getTransferRecords(self, dateRange = "thisWeek"):
        """
        Args:
            range: "today", "thisWeek", "thisMonth", "thisSeason", "thisYear" 
        Returns:
            {'comment': ['日期', '货币单位', '发生金额', '合同编号', '银行名称', '操作', '备注'],
            'data': [['20200206', '人民币', '10000.000', '38534275', '工商银行存管', '银行转证券', '异步处理:10000.000交易成功'], ['20200814', '人民币', '10000.000', '42703579', '工商银行存管', '银行转证券', '异步处理(失败):10000.000银行账户余额不足']],
            'status': True}
        Raises:
        """
        transferRecords = {}
        if not self.__lock.requestLock():
            return transferRecords

        try:
            cmd = ascmds.asgetTransferRecords + ' ' + dateRange
            res = os.popen(cmd).read().strip()
            ls = [x.strip() for x in res.split(',')]

            flag = ls.pop(0)
            if flag == "successed":
                transferRecords.update({'status': True})
            else:
                transferRecords.update({'status': False})
            
            if transferRecords.get('status'):
                length = 7
                transferRecords.update({'comment': [ls.pop(0) for x in range(length) if ls]})
                transferRecords.update({'data': []})
                while ls:
                    transferRecords['data'].append([ls.pop(0) for x in range(length) if ls])
                self.__logging.info("get transfer records successed")
            else:
                transferRecords.update({'comment': ''})
                transferRecords.update({'data': []})
                transferRecords.update({'info': ' '.join(ls)})
                self.__logging.error("get transfer records failed: " + transferRecords.get('info'))
        except Exception as e:
            self.__logging.error("get transfer records failed: " + str(e))
        self.__lock.unlock()
        return transferRecords

    def getAssetType(self, stockCode):
        """ get asset type
        Args:
            stockCode:
        Returns:
            assetType
        Raises:
        """
        if stockCode.startswith('688'):
            assetType = 'sciTech'
        elif stockCode.startswith('300'):
            assetType = 'gem'
        else:
            assetType = 'stock'
        return assetType

    def getBids(self, stockCode = "600030", assetType = None):
        """
        Args:
            stockCode:
            assetType: "stock", "sciTech", "gem"
        Returns:
            {
                'data': {
                    'buy_1': {'price': '11.02', 'vol': '409'},
                    'buy_2': {'price': '11.01', 'vol': '1561'},
                    'buy_3': {'price': '11.00', 'vol': '6981'},
                    'buy_4': {'price': '10.99', 'vol': '936'},
                    'buy_5': {'price': '10.98', 'vol': '842'},
                    'sell_1': {'price': '11.03', 'vol': '119'},
                    'sell_2': {'price': '11.04', 'vol': '25'},
                    'sell_3': {'price': '11.05', 'vol': '86'},
                    'sell_4': {'price': '11.06', 'vol': '5'},
                    'sell_5': {'price': '11.08', 'vol': '83'}
                },
                'info': '',
                'status': True
            }
        Raises:
        """
        bids = {}
        if not self.__lock.requestLock():
            return bids

        if assetType is None:
            assetType = self.getAssetType(stockCode)

        try:
            cmd = ascmds.asgetBids + ' ' + assetType + ' ' + stockCode
            res = os.popen(cmd).read().strip()
            ls = [x.strip() for x in res.split(',')]
            flag = ls.pop(0)
            if flag == "successed":
                bids.update({'status': True})
            else:
                bids.update({'status': False})

            doc = {}
            if bids.get('status'):
                length = 5
                bidsPrice = [ls.pop(0) for x in range(10)]
                ct = 1
                while ct <= length:
                    x = length - ct + 1
                    k = (ls.pop(0) + '_' + str(x)).replace('卖', 'sell')
                    v =  {'price': bidsPrice.pop(0), 'vol': ls.pop(0)}
                    doc.update({k: v})
                    ct = ct + 1

                ct = 1
                while ct <= length:
                    x = ct
                    k = (ls.pop(0) + '_' + str(x)).replace('买', 'buy')
                    v =  {'price': bidsPrice.pop(0), 'vol': ls.pop(0)}
                    doc.update({k: v})
                    ct = ct + 1
                bids.update({'data': doc})
                bids.update({'info': ''})
                self.__logging.info("get bids successed")
            else:
                bids.update({'data': doc})
                bids.update({'info': ' '.join(ls)})
                self.__logging.error("get bids failed: " + bids.get('info'))
        except Exception as e:
            self.__logging.error("get bids failed: " + str(e))
        self.__lock.unlock()
        return bids
 
    def issuingEntrust(self, stockCode, amount, price = None, tradingAction = 'buy', assetType = None):
        """
        Args:
            stockCode:
            amount:
            price:          # None -> default price: 买时为 卖5; 卖时为 买5, 撮合时按 价, 时, 量排序, 会以最优价成交, 如果成功率还是低, 则直接改成涨跌停价格委托
            tradingAction:  # "buy", "sell"
            assetType:      # None, "stock", "sciTech", "gem"
        Returns:
            (status, contractNo)
        Raises:
        """
        def mailMe(action = '', assetsName = '', assetsCode = '', price = '', amount = '', status = '', comments = ''):
            try:
                if self.__keepInformed:
                    action = 'entrust ' + action
                    priceLogged = 'best price' if price is None else price
                    tlog = helper.Tlog(action = action, assetsName = assetsName, assetsCode = assetsCode, price = priceLogged, amount = amount, status = status, comments = '')
                    helper.Mail(tlog)
            except Exception as e:
                self.__logging.error("mailing failed with error: " + str(e))
            return
        
        status = False
        contractNo = None
        if not self.__lock.requestLock():
            return status, contractNo

        if assetType is None:
            assetType = self.getAssetType(stockCode)

        try:
            # 价格须保留两位小数, etf 保留三位小数
            # price 为 None 时取 None
            if price is not None:
                price = "{:.2f}".format(float(price)) if not len(str(price).split(".")[1]) > 2 else price

            if assetType == "sciTech" :
                assert not (int(amount) < 200)
            else:
                assert not (int(amount) < 100)

            cmd = ascmds.asissuingEntrust + ' ' + tradingAction + ' ' + assetType + ' ' + str(stockCode) + ' ' + str(price) + ' ' + str(amount)
            res = os.popen(cmd).read().strip()
            ls = [x.strip() for x in res.split(',')]

            flag = ls.pop(0)
            info = None
            if flag == "successed":
                status = True
                contractNo = ls.pop(0)
                self.__logging.info("issuing entrust successed: " + tradingAction + ' ' + assetType + ' ' + str(stockCode) + ' ' + str(price) + ' ' + str(amount))
                mailMe(action = tradingAction, assetsName = assetType, assetsCode = stockCode, price = price, amount = amount, status = "successed")
            else:
                info = ' '.join(ls)
                self.__logging.error("issuing entrust failed: " + tradingAction + ' ' + assetType + ' ' + str(stockCode) + ' ' + str(price) + ' ' + str(amount) + '. Err: ' + info)
                mailMe(action = tradingAction, assetsName = assetType, assetsCode = stockCode, price = price, amount = amount, status = "failed")
        except Exception as e:
            self.__logging.error("issuing entrust failed: " + tradingAction + ' ' + assetType + ' ' + str(stockCode) + ' ' + str(price) + ' ' + str(amount) + '. Err: ' + str(e))
            mailMe(action = tradingAction, assetsName = assetType, assetsCode = stockCode, price = price, amount = amount, status = "failed")
        self.__lock.unlock()
        return status, contractNo

    def buy(self, stockCode, amount, price = None):
        """
        Args:
            stockCode:
            amount:
            price:
        Returns:
            (status, contractNo)
        Raises:
        """
        return self.issuingEntrust(stockCode = stockCode, amount = amount, price = price, tradingAction = 'buy')

    def sell(self, stockCode, amount, price = None):
        """
        Args:
            stockCode:
            amount:
            price:
        Returns:
            (status, contractNo)
        Raises:
        """
        return self.issuingEntrust(stockCode = stockCode, amount = amount, price = price, tradingAction = 'sell')

    def buyStock(self, stockCode, amount, price = None):
        """
        Args:
            stockCode:
            amount:
            price:
        Returns:
            (status, contractNo)
        Raises:
        """
        return self.issuingEntrust(stockCode, amount, price = price, tradingAction = 'buy', assetType = 'stock')

    def sellStock(self, stockCode, amount, price = None):
        """
        Args:
            stockCode:
            amount:
            price:
        Returns:
            (status, contractNo)
        Raises:
        """
        return self.issuingEntrust(stockCode, amount, price = price, tradingAction = 'sell', assetType = 'stock')

    def buySciTech(self, stockCode, amount, price = None):
        """
        Args:
            stockCode:
            amount:
            price:
        Returns:
            (status, contractNo)
        Raises:
        """
        return self.issuingEntrust(stockCode, amount, price = price, tradingAction = 'buy', assetType = 'sciTech')

    def sellSciTech(self, stockCode, amount, price = None):
        """
        Args:
            stockCode:
            amount:
            price:
        Returns:
            (status, contractNo)
        Raises:
        """
        return self.issuingEntrust(stockCode, amount, price = price, tradingAction = 'sell', assetType = 'sciTech')
   
    def buyGem(self, stockCode, amount, price = None):
        """
        Args:
            stockCode:
            amount:
            price:
        Returns:
            (status, contractNo)
        Raises:
        """
        return self.issuingEntrust(stockCode, amount, price = price, tradingAction = 'buy', assetType = 'gem')

    def sellGem(self, stockCode, amount, price = None):
        """
        Args:
            stockCode:
            amount:
            price:
        Returns:
            (status, contractNo)
        Raises:
        """
        return self.issuingEntrust(stockCode, amount, price = price, tradingAction = 'sell', assetType = 'gem')

    def getTodayIPO(self):
        """
        Args:
        Returns:
            {
                'comment': ['证券名称', '申购代码', '可申购数量', '申购数量'],
                'data': [['']],
                'info': '',
                'status': True
            }
            
        Raises:
        """
        todayIPO = {}
        if not self.__lock.requestLock():
            return todayIPO

        try:
            cmd = ascmds.asgetTodayIPO
            res = os.popen(cmd).read().strip()
            ls = [x.strip() for x in res.split(',')]

            flag = ls.pop(0)
            if flag == "successed":
                todayIPO.update({'status': True})
            else:
                todayIPO.update({'status': False})

            if todayIPO.get("status"):
                length = 4
                todayIPO.update({'comment': [ls.pop(0) for x in range(length) if ls]})
                todayIPO.update({'data': []})
                while ls:
                    todayIPO['data'].append([ls.pop(0) for x in range(length) if ls])
                todayIPO.update({'info': ''})
                self.__logging.info("get today IPO successed")
            else:
                todayIPO.update({'comment': ''})
                todayIPO.update({'data': []})
                todayIPO.update({'info': ' '.join(ls)})
                self.__logging.error("get today IPO failed: " + todayIPO.get('info'))
        except Exception as e:
            self.__logging.error("get today IPO failed: " + str(e))
        self.__lock.unlock()
        return todayIPO

    def oneKeyIPO(self):
        """ one key IPO, auto IPO
        Args:
        Returns:
            True or False
        Raises:
        """
        def mailMe(action = '', assetsName = '', assetsCode = '', price = '', amount = '', status = '', comments = ''):
            try:
                if self.__keepInformed:
                    tlog = helper.Tlog(action = action, assetsName = assetsName, assetsCode = assetsCode, price = price, amount = amount, status = status, comments = '')
                    helper.Mail(tlog)
            except Exception as e:
                self.__logging.error("mailing failed with error: " + str(e))
            return

        status = False
        if not self.__lock.requestLock():
            return status

        try:
            cmd = ascmds.asoneKeyIPO
            res = os.popen(cmd).read().strip()
            ls = [x.strip() for x in res.split(',')]
            
            flag = ls.pop(0)
            info = None
            if flag == "successed":
                status = True
                self.__logging.info("auto IPO successed")
                mailMe(action = "auto IPO", assetsName = '', assetsCode = '', price = '', amount = '', status = "successed")
            else:
                info = ' '.join(ls)
                self.__logging.error("auto IPO failed: " + info)
                mailMe(action = "auto IPO", assetsName = '', assetsCode = '', price = '', amount = '', status = "failed")
        except Exception as e:
            self.__logging.error("IPO failed: " + str(e))
            mailMe(action = "IPO", assetsName = '', assetsCode = '', price = '', amount = '', status = "failed")
        self.__lock.unlock()
        return status

    def revokeEntrust(self, revokeType = "allBuyAndSell", assetType = "stock", contractNo = None):
        """
        Args:
            revokeType:     # "allBuy", "allSell", "allBuyAndSell", "contractNo"
            assetType:      # "stock", "sciTech", "gem"
            contractNo:     # "N8743678"
        Returns: 
            True or False
        Raises:
        """
        def mailMe(action = '', assetsName = '', assetsCode = '', price = '', amount = '', status = '', comments = ''):
            try:
                if self.__keepInformed:
                    assetsCodeLogged = '' if assetsCode is None else assetsCode
                    tlog = helper.Tlog(action = action, assetsName = assetsName, assetsCode = assetsCodeLogged, price = price, amount = amount, status = status, comments = comments)
                    helper.Mail(tlog)
            except Exception as e:
                self.__logging.error("mailing failed with error: " + str(e))
            return

        status = False
        if not self.__lock.requestLock():
            return status

        try:
            cmd = ascmds.asrevokeEntrust + " " + revokeType + " " + assetType + " " + str(contractNo)
            res = os.popen(cmd).read().strip()
            ls = [x.strip() for x in res.split(',')]

            flag = ls.pop(0)
            info = ls.pop(0)
            if flag == "successed":
                status = True
                self.__logging.info("revoke entrust successed: " + revokeType + " " + assetType + " " + str(contractNo) + ". Info: " + info)
                mailMe(action = "revoke entrust " + revokeType, assetsName = assetType, assetsCode = contractNo, price = '', amount = '', status = "successed")
            else:
                self.__logging.error("revoke entrust failed: " + revokeType + " " + assetType + " " + str(contractNo) + ". Err: " + info)
                mailMe(action = "revoke entrust " + revokeType, assetsName = assetType, assetsCode = contractNo, price = '', amount = '', status = "failed")
        except Exception as e:
            self.__logging.error("revoke entrust failed: " + revokeType + " " + assetType + " " + str(contractNo) + ". Err: "+ str(e))
            mailMe(action = "revoke entrust " + revokeType, assetsName = assetType, assetsCode = contractNo, price = '', amount = '', status = "failed")
        self.__lock.unlock()
        return status

    # 优化, 单独写一个文件
    def revokeAllBuyEntrust(self):
        """
        Args:
        Returns:
            True or False
        Raises:
        """
        def mailMe(action = '', assetsName = '', assetsCode = '', price = '', amount = '', status = '', comments = ''):
            if self.__keepInformed:
                tlog = helper.Tlog(action = action, assetsName = assetsName, assetsCode = assetsCode, price = price, amount = amount, status = status, comments = comments)
                helper.Mail(tlog)
            return

        status = False
        if not self.__lock.requestLock():
            return status

        try:
            cmd = ascmds.asrevokeAllBuyEntrust
            res = os.popen(cmd).read().strip()
            ls = [x.strip() for x in res.split(',')]

            flag = ls.pop(0)
            if flag == "successed":
                status = True
                self.__logging.info("revoke all sell entrust successed")
                mailMe(action = "revoke all sell entrust", status='successed')
            else:
                self.__logging.error("revoke all sell entrust failed")
                mailMe(action = "revoke all sell entrust", status = "failed")
        except Exception as e:
            self.__logging.error("revoke all sell entrust failed Err: "+ str(e))
            mailMe(action = "revoke all sell entrust", status = "failed")
        self.__lock.unlock()
        return status

    # 优化, 单独写一个文件
    def revokeAllSellEntrust(self):
        """
        Args:
        Returns:
            True or False
        Raises:
        """
        def mailMe(action = '', assetsName = '', assetsCode = '', price = '', amount = '', status = '', comments = ''):
            if self.__keepInformed:
                tlog = helper.Tlog(action = action, assetsName = assetsName, assetsCode = assetsCode, price = price, amount = amount, status = status, comments = comments)
                helper.Mail(tlog)
            return

        status = False
        if not self.__lock.requestLock():
            return status

        try:
            cmd = ascmds.asrevokeAllSellEntrust
            res = os.popen(cmd).read().strip()
            ls = [x.strip() for x in res.split(',')]

            flag = ls.pop(0)
            if flag == "successed":
                status = True
                self.__logging.info("revoke all buy entrust successed")
                mailMe(action = "revoke all buy entrust", status='successed')
            else:
                self.__logging.error("revoke all buy entrust failed")
                mailMe(action = "revoke all buy entrust", status = "failed")
        except Exception as e:
            self.__logging.error("revoke all buy entrust failed Err: "+ str(e))
            mailMe(action = "revoke all buy entrust", status = "failed")
        self.__lock.unlock()
        return status

    # 优化, 单独写一个文件
    def revokeAllEntrust(self):
        """
        Args:
        Returns:
            True or False
        Raises:
        """
        def mailMe(action = '', assetsName = '', assetsCode = '', price = '', amount = '', status = '', comments = ''):
            if self.__keepInformed:
                tlog = helper.Tlog(action = action, assetsName = assetsName, assetsCode = assetsCode, price = price, amount = amount, status = status, comments = comments)
                helper.Mail(tlog)
            return

        status = False
        if not self.__lock.requestLock():
            return status

        try:
            cmd = ascmds.asrevokeAllEntrust
            res = os.popen(cmd).read().strip()
            ls = [x.strip() for x in res.split(',')]

            flag = ls.pop(0)
            if flag == "successed":
                status = True
                self.__logging.info("revoke all entrust successed")
                mailMe(action = "revoke all entrust", status='successed')
            else:
                self.__logging.error("revoke all entrust failed")
                mailMe(action = "revoke all entrust", status = "failed")
        except Exception as e:
            self.__logging.error("revoke all entrust failed Err: "+ str(e))
            mailMe(action = "revoke all entrust", status = "failed")
        self.__lock.unlock()
        return status

    def revokeContractNoEntrust(self, assetType = "stock",  contractNo = "N8743678"):
        """
        Args:
            assetType:          # "stock", "sciTech", "gem"
            contractNo:         # N8743678
        Returns:
            True or False
        Raises:
        """
        return self.revokeEntrust(revokeType = "contractNo", assetType = assetType, contractNo = contractNo)

    def getHoldingShares(self, assetType = 'stock'):
        """
        Args:
            assetType: "stock", "sciTech"
        Returns:
            {
                'comment': ['证券代码', '证券名称', '市价', '盈亏', '浮动盈亏比(%)', '实际数量', '股票余额', '可用余额', '冻结数量', '成本价', '市值', '交易市场', '股东账户'],
                'data': [
                    ['512290', '生物医药', '2.154', '-36.000', '-0.420', '4000', '4000', '4000', '0', '2.163', '8616.000', '上海Ａ股', 'A639487384'],
                    ['600703', '三安光电', '26.560', '-1126.300', '-9.590', '400', '400', '400', '0', '29.376', '10624.000', '上海Ａ股', 'A639487384']
                ],
                'info': '',
                'status': True
            }
        Raises:
        """
        holdingShares = {}
        if not self.__lock.requestLock():
            return holdingShares

        try:
            cmd = ascmds.asgetHoldingShares + ' ' + assetType
            res = os.popen(cmd).read().strip()
            ls = [x.strip() for x in res.split(',')]

            flag = ls.pop(0)
            if flag == "successed":
                holdingShares.update({'status': True})
            else:
                holdingShares.update({'status': False})

            if holdingShares.get("status"):
                if assetType in ['stock']:
                    length = 15
                else:
                    length = 13
                holdingShares.update({'comment': [ls.pop(0) for x in range(length) if ls]})
                holdingShares.update({'data': []})
                while ls:
                    holdingShares['data'].append([ls.pop(0) for x in range(length) if ls])
                holdingShares.update({'info': ''})
                self.__logging.info("get holding shares successed")
            else:
                holdingShares.update({'comment': ''})
                holdingShares.update({'data': []})
                holdingShares.update({'info': ' '.join(ls)})
                self.__logging.error("get holding shares failed: " + holdingShares.get('info'))
        except Exception as e:
            self.__logging.error("get holding shares failed: " + str(e))
        self.__lock.unlock()
        return holdingShares

    def getAllHoldingShares(self):
        """
        Args:
        Returns:
            {
                'gem': {
                    'comment': ['证券代码', '证券名称', '市价', '盈亏', '浮动盈亏比(%)', '实际数量', '股票余额', '可用余额', '冻结数量', '成本价', '市值', '交易市场', '股东账户'],
                    'data': [['']],
                    'info': '',
                    'status': True
                },
                'sciTech': {
                    'comment': ['证券代码', '证券名称', '市价', '盈亏', '浮动盈亏比(%)', '实际数量', '股票余额', '可用余额', '冻结数量', '成本价', '市值', '交易市场', '股东账户'],
                    'data': [['']],
                    'info': '',
                    'status': True
                },
                'stock': {
                    'comment': ['证券代码', '证券名称', '市价', '盈亏', '浮动盈亏比(%)', '实际数量', '股票余额', '可用余额', '冻结数量', '成本价', '市值', '交易市场', '股东账户'],
                    'data': [
                        ['512290','生物医药','2.154','-36.000','-0.420','4000','4000','4000','0','2.163','8616.000','上海Ａ股','A639487384'],
                        ['600703','三安光电','26.560','-1126.300','-9.590','400','400','400','0','29.376','10624.000','上海Ａ股','A639487384']
                    ],
                    'info': '',
                    'status': True
                }
            }
        Raises:
        """
        # assetType: "stock", "sciTech"
        res1 = self.getHoldingShares(assetType = 'stock')
        res2 = self.getHoldingShares(assetType = 'sciTech')
        res3 = self.getHoldingShares(assetType = 'gem')
        allHoldingShares = {"stock": res1, "sciTech": res2, "gem": res3}
        return allHoldingShares

    def getEntrust(self, assetType = 'stock', dateRange = 'today', isRevocable = True):
        """
        Args:
            assetType:      # "stock", "sciTech", "gem"
            dateRange:      # "today", "thisWeek", "thisMonth", "thisSeason", "thisYear"
            isRevocable:    # True, False -> true, false
        Returns:
            {
                'comment': ['委托日期', '委托时间', '证券代码', '证券名称', '操作', '备注', '委托数量', '撤销数量', '委托价格', '成交价格', '合同编号', '委托属性'],
                'data': [['']],
                'info': '',
                'status': True
            }
        Raises:
        """
        entrust = {}
        if not self.__lock.requestLock():
            return entrust

        try:
            cmd = ascmds.asgetEntrust + ' ' +  assetType + ' ' + dateRange + ' ' + str(isRevocable).lower()
            res = os.popen(cmd).read().strip()
            ls = [x.strip() for x in res.split(',')]

            flag = ls.pop(0)
            if flag == "successed":
                entrust.update({'status': True})
            else:
                entrust.update({'status': False})

            if entrust.get('status'):
                if assetType in ['sciTech', 'gem']:
                    length = 13
                elif assetType in ['stock']:
                    length =11

                entrust.update({'comment': [ls.pop(0) for x in range(length) if ls]})
                entrust.update({'data': []})
                while ls:
                    entrust['data'].append([ls.pop(0) for x in range(length) if ls])
                entrust.update({'info': ''})
                self.__logging.info("get entrust successed")
            else:
                entrust.update({'comment': ''})
                entrust.update({'data': []})
                entrust.update({'info': ' '.join(ls)})
                self.__logging.error("get entrust failed: " + entrust.get('info'))
        except Exception as e:
            self.__logging.error("get entrust failed: " + str(e))
        self.__lock.unlock()
        return entrust

    def getTodayAllRevocableEntrust(self):
        """
        Args:
        Returns:
            {
                'gem': {
                    'comment': ['委托日期', '委托时间', '证券代码', '证券名称', '操作', '备注', '委托数量', '撤销数量', '委托价格', '成交价格', '合同编号', '申报编号', '委托属性'],
                    'data': [['']],
                    'info': '',
                    'status': True
                },
                'sciTech': {
                    'comment': ['委托日期', '委托时间', '证券代码', '证券名称', '操作', '备注', '委托数量', '撤销数量', '委托价格', '成交价格', '合同编号', '申报编号', '委托属性'],
                    'data': [['']],
                    'info': '',
                    'status': True
                },
                'stock': {
                    'comment': ['委托日期', '委托时间', '证券代码', '证券名称', '操作', '备注', '委托数量', '撤销数量', '委托价格', '成交价格', '合同编号', '委托属性'],
                    'data': [['']],
                    'info': '',
                    'status': True
                }
            }
        Raises:
        """
        res1 = self.getEntrust(assetType = 'stock', dateRange = 'today', isRevocable = True)
        res2 = self.getEntrust(assetType = 'sciTech', dateRange = 'today', isRevocable = True)
        res3 = self.getEntrust(assetType = 'gem', dateRange = 'today', isRevocable = True)
        todayAllRevocableEntrustments = {"stock": res1, "sciTech": res2, "gem": res3}
        return todayAllRevocableEntrustments


    def getClosedDeals(self, assetType = 'stock', dateRange = 'today'):
        """
        Args:
            assetType: "stock", "sciTech"
            dateRange: "today", "thisWeek", "thisMonth", "thisSeason", "thisYear"
        Returns:
            {
                'comment': ['成交日期', '成交时间', '证券代码', '证券名称', '操作', '成交数量', '成交均价', '成交金额', '合同编号', '成交编号'],
                'data': [['']],
                'info': None,
                'status': True
            }
        Raises:
        """
        closedDeals = {}
        if not self.__lock.requestLock():
            return closedDeals

        try:
            cmd = ascmds.asgetClosedDeals + ' ' +  assetType + ' ' + dateRange
            res = os.popen(cmd).read().strip()
            ls = [x.strip() for x in res.split(',')]
            
            flag = ls.pop(0)
            if flag == "successed":
                closedDeals.update({'status': True})
            else:
                closedDeals.update({'status': False})

            if closedDeals.get("status"):
                length = 10
                closedDeals.update({'comment': [ls.pop(0) for x in range(length) if ls]})
                closedDeals.update({'data': []})
                while ls:
                    closedDeals['data'].append([ls.pop(0) for x in range(length) if ls])
                closedDeals.update({'info': None})
                self.__logging.info("get closed deals successed")
            else:
                closedDeals.update({'comment': ''})
                closedDeals.update({'data': []})
                closedDeals.update({'info': ' '.join(ls)})
                self.__logging.error("get closed deals failed: " + closedDeals.get('info'))
        except Exception as e:
            self.__logging.error("get closed deals failed: " + str(e))
        self.__lock.unlock()
        return closedDeals

    def getCapitalDetails(self, assetType = 'stock', dateRange = 'thisSeason'):
        """
        Args:
            assetType: "stock", "sciTech"
            dateRange: "today", "thisWeek", "thisMonth", "thisSeason", "thisYear"
        Returns:
            {
                'comment': ['成交日期', '证券代码', '证券名称', '操作', '成交数量', '成交均价', '发生金额', '本次金额', '交易市场', '股东账户', '成交时间'],
                'data': [['']],
                'info': '',
                'status': True
            }
        Raises:
        """
        capitalDetails = {}
        if not self.__lock.requestLock():
            return capitalDetails

        try:
            cmd = ascmds.asgetCapitalDetails + ' ' +  assetType + ' ' + dateRange
            res = os.popen(cmd).read().strip()
            ls = [x.strip() for x in res.split(',')]
            
            flag = ls.pop(0)

            if flag == "successed":
                capitalDetails.update({'status': True})
            else:
                capitalDetails.update({'status': False})

            if capitalDetails.get("status"):
                length = 11
                capitalDetails.update({'comment': [ls.pop(0) for x in range(length) if ls]})
                capitalDetails.update({'data': []})
                while ls:
                    capitalDetails['data'].append([ls.pop(0) for x in range(length) if ls])
                capitalDetails.update({'info': ''})
                self.__logging.info("get capital details successed")
            else:
                capitalDetails.update({'comment': ''})
                capitalDetails.update({'data': []})
                capitalDetails.update({'info': ' '.join(ls)})
                self.__logging.error("get capital details failed: " + capitalDetails.get('info'))
        except Exception as e:
            self.__logging.error("get capital details failed: " + str(e))
        self.__lock.unlock()
        return capitalDetails


    def getIPO(self, queryType = "entrust", dateRange = "today"):
        """
        Note: queryType entrust only supports dateRange today
        Args:
            queryType:      # entrust, allotmentNo, winningLots
            dateRange:      # today, thisWeek, thisMonth, thisSeason, thisYear
        Returns:
            {
                'comment': ['委托日期', '委托时间', '证券代码', '证券名称', '操作', '备注', '委托数量', '撤销数量', '委托价格', '成交价格', '合同编号', '申报编号'],
                'data': [['']],
                'info': '',
                'status': True
            }
        Raises:
        """
        result = {}
        if not self.__lock.requestLock():
            return result

        try:
            cmd = ascmds.asgetIPO + ' ' + queryType + ' ' + dateRange 
            res = os.popen(cmd).read().strip()
            ls = [x.strip() for x in res.split(',')]

            flag = ls.pop(0)
            if flag == "successed":
                result.update({'status': True})
            else:
                result.update({'status': False})

            if result.get("status"):
                if queryType == "entrust":
                    length = 12
                elif queryType == "allotmentNo":
                    length = 7
                elif queryType == "winningLots":
                    length = 9
                else:
                    result.update({'comment': ''})
                    result.update({'data': []})
                    result.update({'info': ' '.join(ls)})
                    self.__logging.error("get IPO failed: " + queryType + " " + dateRange +  ". Err: "  + result.get('info'))

                result.update({'comment': [ls.pop(0) for x in range(length) if ls]})
                result.update({'data': []})
                while ls:
                    result['data'].append([ls.pop(0) for x in range(length) if ls])
                result.update({'info': ''})
                self.__logging.info("get IPO failed successed: " + queryType + " " + dateRange)
            else:
                result.update({'comment': ''})
                result.update({'data': []})
                result.update({'info': ' '.join(ls)})
                self.__logging.error("get IPO failed: " + queryType + " " + dateRange +  ". Err: "  + result.get('info'))
        except Exception as e:
            self.__logging.error("get IPO failed: " + queryType + " " + dateRange +  ". Err: "  + str(e))
        self.__lock.unlock()
        return result

    def getIPOentrust(self, dateRange = "today"):
        """
        Note: queryType entrust only supports dateRange today
        Args:
            dateRange:      # today, thisWeek, thisMonth, thisSeason, thisYear
        Returns:
        Raises:
        """
        return self.getIPO(queryType = "entrust", dateRange = "today")

    def getIPOallotmentNo(self, dateRange = "today"):
        """
        Args:
            dateRange:      # today, thisWeek, thisMonth, thisSeason, thisYear
        Returns:
        Raises:
        """
        return self.getIPO(queryType = "allotmentNo", dateRange = "today")

    def getIPOwinningLots(self, dateRange = "today"):
        """
        Args:
            dateRange:      # today, thisWeek, thisMonth, thisSeason, thisYear
        Returns:
        Raises:
        """
        return self.getIPO(queryType = "winningLots", dateRange = "today")

    def liquidating(self):
        """ 清仓: 卖出所有可用份额, 因 T+1, 当天买入的无法当天卖出
        Args:
        Returns:
        Raises:
        """
        try:
            # 至多尝试 3 次, 不要使用递归, 可失败再发起
            for _ in range(3):
                # 撤销所有委托: buy and sell
                self.revokeAllEntrust()
                # 获取当前持仓
                allHoldingShares = self.getAllHoldingShares()
                show(allHoldingShares)
                if allHoldingShares.get("stock").get("status") and allHoldingShares.get("sciTech").get("status") and allHoldingShares.get("gem").get("status"):
                    l = []
                    for assetType in ["stock", "sciTech", "gem"]:
                        dt = allHoldingShares.get(assetType).get("data")
                        if dt[0][0]:
                            l.extend([[assetType, x[0], x[7]] for x in dt if int(x[7])])   # a list of [资产类型, 股票代码, 可用数量], 过滤掉可用为 0 的资产
                    # if l is not [] or [[]]
                    if l and l[0]:
                        for assetType, stockCode, availableQuantity in l:
                            if assetType == "stock":
                                self.sellStock(stockCode, availableQuantity)               # 当前最优价 委托卖出
                            if assetType == "sciTech":
                                self.sellSciTech(stockCode, availableQuantity)             # 当前最优价 委托卖出
                            if assetType == "gem":
                                self.sellGem(stockCode, availableQuantity)                 # 当前最优价 委托卖出
                        # 等待成交, 不成交则撤单重新委托
                        time.sleep(3.5)
                    else:
                        # when l is empty
                        self.__logging.info("liquidating successed")
                        return True
        except Exception as e:
            self.__logging.error("liquidating failed: " + str(e))
        return False
    
    def entrustPortfolio(self, StockCodeAmountPriceList = []):
        """ 委托买入股票组合, price 可为 None, 以最优价买入. 如设置了价格还是以最优价买入， 则调整 applescript 代码延时, 视机器性能调整
        Args: 
            StockCodeAmountPriceList = [['512290', '1000', '2.169']]
        Returns:
            {'512290': True}
        Raises:
        """
        statusList = []
        for stockCode, amount, price in StockCodeAmountPriceList:
            try:
                status, contractNo = self.issuingEntrust(stockCode=stockCode, amount=amount, price=price, tradingAction="buy")
                statusList.append({'stockCode': stockCode, 'status': status, 'contractNo': contractNo})
                self.__logging.info("entrust buy successed")
            except Exception as e:
                self.__logging.error("entrust buy failed: " + str(e))
                statusList.append({'stockCode': stockCode, 'status': 'failed', 'contractNo': None})
        return statusList


class EvolvingSim():
    """ Simulation Trading class
    """
    def __init__(self):
        """
        Args:
        Returns:
        Raises:
        """
        self.__logging = helper.Logging(logType = 'env_simu')
        self._config = helper.Config()
        self.__lock = Lock()

    def getAccountInfo(self):
        """
        Args:
        Returns:
        Raises:
        """
        accountInfo = {}
        if not self.__lock.requestLock():
            return accountInfo

        try:
            cmd = ascmds.asgetAccountInfoSim
            res = os.popen(cmd).read().strip()
            ls = [x.strip() for x in res.split(',')]

            flag = ls.pop(0)
            if flag == "successed":
                accountInfo.update({'status': True})
            else:
                accountInfo.update({'status': False})

            doc = {}
            if accountInfo.get("status"):
                while len(ls)>1:
                    doc.update({ls.pop(0): ls.pop(0)})
                accountInfo.update({'data': doc})
                accountInfo.update({'info': None})
                self.__logging.info("get account info successed")
            else:
                accountInfo.update({'status': False})
                accountInfo.update({'data': doc})
                accountInfo.update({'info': ' '.join(ls)})
                self.__logging.error("get account info failed: " + accountInfo.get('info'))
        except Exception as e:
            self.__logging.error("get account info failed: " + str(e))
        self.__lock.unlock()
        return accountInfo

    def issuingEntrust(self, stockCode, amount, price = None, tradingAction = 'buy'):
        """
        Args:
            action: "buy", "sell"
            assetType: "stock"
        Returns:
        Raises:
        """
        assetType = 'stock'
        status = False
        contractNo = None
        if not self.__lock.requestLock():
            return status, contractNo

        try:
            # 价格须保留两位小数, etf 保留三位小数
            # price 为 None 时取 None
            if price is not None:
                price = "{:.2f}".format(float(price)) if not len(str(price).split(".")[1]) > 2 else price

            assert not (int(amount) < 100)

            cmd = ascmds.asissuingEntrustSim + ' ' + tradingAction + ' ' + assetType + ' ' + str(stockCode) + ' ' + str(price) + ' ' + str(amount)
            res = os.popen(cmd).read().strip()
            ls = [x.strip() for x in res.split(',')]
            
            flag = ls.pop(0)
            info = None
            if flag == "successed":
                status = True
                contractNo = ls.pop(0)
                self.__logging.info("issuing entrust successed: " + tradingAction + ' ' + assetType + ' ' + str(stockCode) + ' ' + str(price) + ' ' + str(amount) + ' contractNo ' + contractNo)
            else:
                info = ' '.join(ls)
                self.__logging.error("issuing entrust failed: " + tradingAction + ' ' + assetType + ' ' + str(stockCode) + ' ' + str(price) + ' ' + str(amount) + '. Err: ' + info)
        except Exception as e:
            self.__logging.error("issuing entrust failed: " + tradingAction + ' ' + assetType + ' ' + str(stockCode) + ' ' + str(price) + ' ' + str(amount) + '. Err: ' + str(e))
        self.__lock.unlock()
        return status, contractNo

    def buy(self, stockCode, amount, price = None):
        """
        Args:
        Returns:
        Raises:
        """
        return self.issuingEntrust(stockCode, amount, price = price, tradingAction = 'buy')

    def sell(self, stockCode, amount, price = None):
        """
        Args:
        Returns:
        Raises:
        """
        return self.issuingEntrust(stockCode, amount, price = price, tradingAction = 'sell')

    def revokeEntrust(self, revokeType = "allBuyAndSell", contractNo = None):
        """
        Args:
        	# revokeType: "allBuy", "allSell", "allBuyAndSell", "contractNo"
	        # assetType: "stock"
	        # contractNo: None, or specify a contractNo, ex. "N8743678"
        Returns:
        Raises:
        """
        assetType = "stock"
        status = False
        info = None
        if not self.__lock.requestLock():
            return status, info

        try:
            cmd = ascmds.asrevokeEntrustSim  + " " + revokeType + " " + assetType + " " + str(contractNo)
            res = os.popen(cmd).read().strip()
            ls = [x.strip() for x in res.split(',')]
            flag = ls.pop(0)
            info = ls.pop(0)      # 成功或失败都返回
            if flag == "successed":
                status = True
                self.__logging.info("revoke entrust successed: " + revokeType + " " + assetType + " " + str(contractNo))
            else:
                self.__logging.error("revoke entrust failed: " + revokeType + " " + assetType + " " + str(contractNo) + ". Err: " + info)
        except Exception as e:
            self.__logging.error("revoke entrust failed: " + revokeType + " " + assetType + " " + str(contractNo) + ". Err: "+ str(e))
        self.__lock.unlock()
        return status, info

    def getHoldingShares(self):
        """
        Args:
            assetType: "stock"
        Returns:
        Raises:
        """
        assetType = 'stock'
        holdingShares = {}
        if not self.__lock.requestLock():
            return holdingShares

        try:
            cmd = ascmds.asgetHoldingSharesSim + ' ' + assetType
            res = os.popen(cmd).read().strip()
            ls = [x.strip() for x in res.split(',')]

            flag = ls.pop(0)
            if flag == "successed":
                holdingShares.update({'status': True})
            else:
                holdingShares.update({'status': False})
            
            if holdingShares.get("status"):
                length = 15
                holdingShares.update({'comment': [y for y in [ls.pop(0) for x in range(length) if ls] if y]})
                holdingShares.update({'data': []})
                while ls:
                    holdingShares['data'].append([ls.pop(0) for x in range(length) if ls])
                holdingShares.update({'info': ''})
                self.__logging.info("get holding shares successed")
            else:
                holdingShares.update({'comment': ''})
                holdingShares.update({'data': []})
                holdingShares.update({'info': ' '.join(ls)})
                self.__logging.error("get holding shares failed: " + holdingShares.get('info'))
        except Exception as e:
            self.__logging.error("get holding shares failed: " + str(e))
        self.__lock.unlock()
        return holdingShares

    def getEntrust(self, dateRange = 'today', isRevocable = True):
        """
        Args:
            dateRange: "today", "thisWeek", "thisMonth", "thisSeason", "thisYear". only "today" is supported by 同花顺 now
            isRevocable: True, False -> true, false
        Returns:
        Raises:
        """
        assetType = 'stock'
        entrust = {}
        if not self.__lock.requestLock():
            return entrust

        try:
            cmd = ascmds.asgetEntrustSim + ' ' +  assetType + ' ' + dateRange + ' ' + str(isRevocable).lower()
            res = os.popen(cmd).read().strip()
            ls = [x.strip() for x in res.split(',')]

            flag = ls.pop(0)
            if flag == "successed":
                entrust.update({'status': True})
            else:
                entrust.update({'status': False})

            if entrust.get('status'):
                length = 12
                entrust.update({'comment': [y for y in [ls.pop(0) for x in range(length) if ls] if y]})
                entrust.update({'data': []})
                while ls:
                    entrust['data'].append([ls.pop(0) for x in range(length) if ls])
                entrust.update({'info': ''})
                self.__logging.info("get entrust successed")
            else:
                entrust.update({'comment': ' '})
                entrust.update({'data': []})
                entrust.update({'info': ' '.join(ls)})
                self.__logging.error("get entrust failed: " + entrust.get('info'))
        except Exception as e:
            self.__logging.error("get entrust failed: " + str(e))
        self.__lock.unlock()
        return entrust

    def getClosedDeals(self, dateRange = 'today'):
        """
        Args:
            dateRange: "today", "thisWeek", "thisMonth", "thisSeason", "thisYear"
        Returns:
        Raises:
        """
        assetType = 'stock'
        closedDeals = {}
        if not self.__lock.requestLock():
            return closedDeals

        try:
            cmd = ascmds.asgetClosedDealsSim + ' ' +  assetType + ' ' + dateRange
            res = os.popen(cmd).read().strip()
            ls = [x.strip() for x in res.split(',')]

            flag = ls.pop(0)
            if flag == "successed":
                closedDeals.update({'status': True})
            else:
                closedDeals.update({'status': False})

            if closedDeals.get('status'):
                length = 10
                closedDeals.update({'comment': [ls.pop(0) for x in range(length) if ls]})
                closedDeals.update({'data': []})
                while ls:
                    closedDeals['data'].append([ls.pop(0) for x in range(length) if ls])
                self.__logging.info("get closed deals successed")
            else:
                closedDeals.update({'comment': ''})
                closedDeals.update({'data': []})
                closedDeals.update({'info': ' '.join(ls)})
                self.__logging.error("get closed deals failed: " + closedDeals.get('info'))
        except Exception as e:
            self.__logging.error("get closed deals failed: " + str(e))
        self.__lock.unlock()
        return closedDeals

    def getCapitalDetails(self, dateRange = 'thisSeason'):
        """
        Args:   
            assetType: "stock"
            dateRange: "today", "thisWeek", "thisMonth", "thisSeason", "thisYear"
        Returns:
        Raises:
        """
        assetType = 'stock'
        capitalDetails = {}
        if not self.__lock.requestLock():
            return capitalDetails

        try:
            cmd = ascmds.asgetCapitalDetailsSim + ' ' +  assetType + ' ' + dateRange
            res = os.popen(cmd).read().strip()
            ls = [x.strip() for x in res.split(',')]

            flag = ls.pop(0)
            if flag == "successed":
                capitalDetails.update({'status': True})
            else:
                capitalDetails.update({'status': False})

            if capitalDetails.get('status'):
                length = 11
                capitalDetails.update({'comment': [ls.pop(0) for x in range(length) if ls]})
                capitalDetails.update({'data': []})
                while ls:
                    capitalDetails['data'].append([ls.pop(0) for x in range(length) if ls])
                capitalDetails.update({'info': ''})
                self.__logging.info("get capital details successed")
            else:
                capitalDetails.update({'comment': ''})
                capitalDetails.update({'data': []})
                capitalDetails.update({'info': ' '.join(ls)})
                self.__logging.error("get capital details failed: " + capitalDetails.get('info'))
        except Exception as e:
            self.__logging.error("get capital details failed: " + str(e))
        self.__lock.unlock()
        return capitalDetails

    def liquidating(self):
        """ 清仓: 卖出所有可用份额, 因 T+1, 当天买入的无法当天卖出
        """
        try:
            # 至多尝试 3 次, 不要使用递归
            for _ in range(3):
                # 撤销所有委托: buy and sell
                self.revokeEntrust(revokeType = "allBuyAndSell", contractNo = None)
                # 获取当前持仓
                allSimHoldingShares = self.getHoldingShares()
                # print(allSimHoldingShares)
                if allSimHoldingShares.get("status"):
                    l = []
                    dt = allSimHoldingShares.get("data")
                    if dt[0][0]:
                        l.extend([[x[0], x[7]] for x in dt if int(x[7])])   # a list of [资产类型, 股票代码, 可用数量], 过滤掉可用为 0 的资产
                    # if l is not [] or [[]]
                    if l and l[0]:
                        for stockCode, availableQuantity in l:
                            status, contractNo = self.issuingEntrust(stockCode = stockCode, amount = availableQuantity, tradingAction = 'sell')
                        # 等待成交
                        time.sleep(8)
                    else:
                        # when l is empty
                        self.__logging.info("liquidating successed")
                        return True
        except Exception as e:
            self.__logging.error("liquidating failed: " + str(e))
        return False

    def entrustPortfolio(self, stockCodeAmountPriceList = []):
        """ 委托买入股票组合, price 可为 None, 以最优价买入. 如设置了价格还是以最优价买入， 则调整 applescript 代码延时, 视机器性能调整
        Args: 
            stockCodeAmountPriceList = [['512290', '1000', '2.169']]
        Returns:
            {'512290': True}
        Raises:
        """
        statuslist = []
        try:
            for stockCode, amount, price in stockCodeAmountPriceList:
                status, contractNo = self.issuingEntrust(stockCode=stockCode, amount=amount, price=price, tradingAction="buy")
                statuslist.append({'stockCode': stockCode, 'status': status, 'contractNo': contractNo})
            self.__logging.info("entrust protfolio successed")
        except Exception as e:
            self.__logging.error("entrust portfolio failed: " + str(e))
            for stockCode, amount, price in stockCodeAmountPriceList:
                statuslist.append({'stockCode': stockCode, 'status': 'failed', 'contractNo': None})
        return statuslist



if __name__== "__main__":
    pass
    # --- Service
    # -----------------------------------------
    # service = Service()

    # status = service.loginClient()
    # print(status)
    # time.sleep(1)

    # status = service.isClientLoggedIn()
    # print(status)
    # time.sleep(1)

    # status = service.logoutClient()
    # print(status)
    # time.sleep(1)

    # status = service.isClientLoggedIn()
    # print(status)
    # time.sleep(1)

    # status = service.reLoginClient()
    # print(status)
    # time.sleep(1)

    # status = service.logoutClient()
    # print(status)
    # time.sleep(1)


    # --- Evolving
    # -----------------------------------------
    # service = Service()

    # status = service.loginClient()
    # print(status)

    # dw = Evolving()
    # dw.keepInformed = True

    # status = dw.isBrokerLoggedIn()
    # print(status)

    # status = dw.loginBroker()
    # print(status)

    # status = dw.isBrokerLoggedIn()
    # print(status)
    
    # accountInfo = dw.getAccountInfo()
    # show(accountInfo)

    # status = dw.transfer(transferType = "broker2bank", amount = 1000)
    # show(status)

    # status = dw.transfer(transferType = "bank2broker", amount = 1000)
    # show(status)

    # status = dw.transfer_broker2bank(amount = 10000)
    # show(status)

    # status = dw.transfer_bank2broker(amount = 10000)
    # show(status)

    # transferRecords = dw.getTransferRecords(dateRange = "thisYear")
    # show(transferRecords)

    # bids = dw.getBids(stockCode = "600030")
    # show(bids)

    # bids = dw.getBids(stockCode = "600030", assetType = 'stock')
    # show(bids)

    # bids = dw.getBids(stockCode = "688055")
    # show(bids)
    # bids = dw.getBids(stockCode = "688055", assetType = 'sciTech')
    # show(bids)

    # bids = dw.getBids(stockCode = "300750", assetType = 'gem')
    # show(bids)
    # bids = dw.getBids(stockCode = "300750")
    # show(bids)

    # status, contractNo = dw.issuingEntrust(stockCode = '002241', amount = 100, price = 37.01, tradingAction = 'buy')
    # show(status)
    # show(contractNo)
    # status, contractNo = dw.issuingEntrust(stockCode = '002241', amount = 100, price = 40.01, tradingAction = 'sell')
    # show(status)
    # show(contractNo)
    # status, contractNo = dw.issuingEntrust(stockCode = '002241', amount = 100, tradingAction = 'buy')
    # show(status)
    # show(contractNo)
    # status, contractNo = dw.issuingEntrust(stockCode = '002241', amount = 100, tradingAction = 'sell')
    # show(status)
    # show(contractNo)

    # status, contractNo = dw.issuingEntrust(stockCode = '688050', amount = 200, price = 220.01, tradingAction = 'buy')
    # show(status)
    # show(contractNo)
    # status, contractNo = dw.issuingEntrust(stockCode = '688050', amount = 200, price = 225.01, tradingAction = 'sell')
    # show(status)
    # show(contractNo)
    # status, contractNo = dw.issuingEntrust(stockCode = '688050', amount = 200, tradingAction = 'buy')
    # show(status)
    # show(contractNo)
    # status, contractNo = dw.issuingEntrust(stockCode = '688050', amount = 200, tradingAction = 'sell')
    # show(status)
    # show(contractNo)

    # status, contractNo = dw.issuingEntrust(stockCode = '300474', amount = 200, price = 72.54, tradingAction = 'buy')
    # show(status)
    # show(contractNo)
    # status, contractNo = dw.issuingEntrust(stockCode = '300474', amount = 200, price = 78.41, tradingAction = 'sell')
    # show(status)
    # show(contractNo)
    # status, contractNo = dw.issuingEntrust(stockCode = '300474', amount = 200, tradingAction = 'buy')
    # show(status)
    # show(contractNo)
    # status, contractNo = dw.issuingEntrust(stockCode = '300474', amount = 200, tradingAction = 'sell')
    # show(status)
    # show(contractNo)

    # status, contractNo = dw.buy(stockCode = '002241', amount = 100)
    # show(status)
    # show(contractNo)
    # status, contractNo = dw.buy(stockCode = '002241', amount = 100, price = 37.01)
    # show(status)
    # show(contractNo)
    # status, contractNo = dw.buy(stockCode = '688050', amount = 200, price = 220.01)
    # show(status)
    # show(contractNo)
    # status, contractNo = dw.buy(stockCode = '300474', amount = 200, price = 72.54)
    # show(status)
    # show(contractNo)

    # status, contractNo = dw.sell(stockCode = '002241', amount = 100)
    # show(status)
    # show(contractNo)
    # status, contractNo = dw.sell(stockCode = '002241', amount = 100, price = 37.01)
    # show(status)
    # show(contractNo)
    # status, contractNo = dw.sell(stockCode = '688050', amount = 200, price = 220.01)
    # show(status)
    # show(contractNo)
    # status, contractNo = dw.sell(stockCode = '300474', amount = 200, price = 72.54)
    # show(status)
    # show(contractNo)

    # status, contractNo = dw.buyStock(stockCode = '002241', amount = 100, price = 37.01)
    # show(status)
    # show(contractNo)
    # status, contractNo = dw.sellStock(stockCode = '002241', amount = 100, price = 40.01)
    # show(status)
    # show(contractNo)
    # status, contractNo = dw.buyStock(stockCode = '002241', amount = 100)
    # show(status)
    # show(contractNo)
    # status, contractNo = dw.sellStock(stockCode = '002241', amount = 100)
    # show(status)
    # show(contractNo)

    # status, contractNo = dw.buySciTech(stockCode = '688050', amount = 200, price = 225.01)
    # show(status)
    # show(contractNo)
    # status, contractNo = dw.sellSciTech(stockCode = '688050', amount = 200, price = 220.01)
    # show(status)
    # show(contractNo)
    # status, contractNo = dw.buySciTech(stockCode = '688050', amount = 200)
    # show(status)
    # show(contractNo)
    # status, contractNo = dw.sellSciTech(stockCode = '688050', amount = 200)
    # show(status)
    # show(contractNo)

    # status, contractNo = dw.buyGem(stockCode = '300474', amount = 200, price = 72.54)
    # show(status)
    # show(contractNo)
    # status, contractNo = dw.sellGem(stockCode = '300474', amount = 200, price = 78.41)
    # show(status)
    # show(contractNo)
    # status, contractNo = dw.buyGem(stockCode = '300474', amount = 200)
    # show(status)
    # show(contractNo)
    # status, contractNo = dw.sellGem(stockCode = '300474', amount = 200)
    # show(status)
    # show(contractNo)

    # todayIPO = dw.getTodayIPO()
    # show(todayIPO)

    # status = dw.oneKeyIPO()
    # print(status)

    # status = dw.revokeEntrust(revokeType = "allBuyAndSell", assetType = "stock", contractNo = None)
    # show(status)
    # status = dw.revokeEntrust(revokeType = "allBuy", assetType = "stock", contractNo = None)
    # show(status)
    # status = dw.revokeEntrust(revokeType = "allSell", assetType = "stock", contractNo = None)
    # show(status)

    # # note: brew install cliclick
    # status = dw.revokeContractNoEntrust(assetType = "stock",  contractNo = "N8536587")
    # show(status)

    # status = dw.revokeAllEntrust()
    # show(status)
    # status = dw.revokeAllBuyEntrust()
    # show(status)
    # status = dw.revokeAllSellEntrust()
    # show(status)

    # holdingShares = dw.getHoldingShares(assetType = 'stock')
    # show(holdingShares)

    # allholdingShares = dw.getAllHoldingShares()
    # show(allholdingShares)

    # entrust = dw.getEntrust(assetType = 'stock', dateRange = 'today', isRevocable = True)
    # show(entrust)

    # entrust = dw.getEntrust(assetType = 'stock', dateRange = 'today', isRevocable = False)
    # show(entrust)

    # entrust = dw.getEntrust(assetType = 'stock', dateRange = 'thisWeek', isRevocable = False)
    # show(entrust)
    # print(len(entrust.get('data')))

    # entrust = dw.getEntrust(assetType = 'stock', dateRange = 'thisYear', isRevocable = False)
    # show(entrust)

    # res = dw.getTodayAllRevocableEntrust()
    # show(res)

    # closedDeals = dw.getClosedDeals(assetType = 'stock', dateRange = 'thisSeason')
    # show(closedDeals)

    # closedDeals = dw.getClosedDeals(assetType = 'stock', dateRange = 'today')
    # show(closedDeals)

    # capitalDetails = dw.getCapitalDetails(assetType = 'stock', dateRange = 'thisSeason')
    # show(capitalDetails)

    # capitalDetails = dw.getCapitalDetails(assetType = 'stock', dateRange = 'today')
    # show(capitalDetails)

    # res = dw.getIPO(queryType = "entrust", dateRange = "today")
    # show(res)

    # # this line will be fail
    # res = dw.getIPO(queryType = "entrust", dateRange = "thisWeek")
    # show(res)

    # res = dw.getIPO(queryType = "allotmentNo", dateRange = "thisMonth")
    # show(res)

    # res = dw.getIPO(queryType = "winningLots", dateRange = "thisSeason")
    # show(res)

    # status = dw.liquidating()
    # show(status)

    # StockCodeAmountPriceList = [['512290', '1000', '2.169'], ['512290', '1000', '2.171'], ['688050', '200', '225.01']]
    # statusList = dw.entrustPortfolio(StockCodeAmountPriceList)
    # show(statusList)

    # status = dw.revokeAllEntrust()
    # show(status)

    # service.logoutClient()


    # --- EvolvingSim
    # -----------------------------------------
    # service = Service()

    # status = service.loginClient()
    # print(status)
    # time.sleep(3)

    # dws = EvolvingSim()

    # simulationAccountInfo = dws.getAccountInfo()
    # show(simulationAccountInfo)

    # status, contractNo = dws.issuingEntrust(stockCode = '002241', amount = 100, price = 37.01, tradingAction = 'buy')
    # show(status)
    # show(contractNo)
    # status, contractNo = dws.issuingEntrust(stockCode = '600196', amount = 100, price = 60.01, tradingAction = 'buy')
    # show(status)
    # show(contractNo)
    # status, contractNo = dws.issuingEntrust(stockCode = '600196', amount = 100, tradingAction = 'buy')
    # show(status)
    # show(contractNo)
    # status, contractNo = dws.issuingEntrust(stockCode = '600196', amount = 100, price = 61.81, tradingAction = 'sell')
    # show(status)
    # show(contractNo)
    # status, contractNo = dws.issuingEntrust(stockCode = '002241', amount = 200, price = 40.01, tradingAction = 'sell')
    # show(status)
    # show(contractNo)
    # status, contractNo = dws.issuingEntrust(stockCode = '002241', amount = 200, tradingAction = 'sell')
    # show(status)
    # show(contractNo)

    # res = dws.revokeEntrust(revokeType = "allBuyAndSell", contractNo = None)
    # show(res)
    # res = dws.revokeEntrust(revokeType = "allBuy", contractNo = None)
    # show(res)
    # res = dws.revokeEntrust(revokeType = "allSell", contractNo = None)
    # show(res)
    # res = dws.revokeEntrust(revokeType = "contractNo", contractNo = "1670247753")
    # show(res)

    # simulationHoldingShares = dws.getHoldingShares()
    # show(simulationHoldingShares)

    # simulationEntrustment = dws.getEntrust(dateRange = 'today', isRevocable = False)
    # show(simulationEntrustment)

    # simulationEntrustment = dws.getEntrust(dateRange = 'today', isRevocable = True)
    # show(simulationEntrustment)

    # simulationClosedDeals = dws.getClosedDeals(dateRange = 'today')
    # show(simulationClosedDeals)

    # simulationClosedDeals = dws.getClosedDeals(dateRange = 'thisMonth')
    # show(simulationClosedDeals)

    # simulationCapitalDetails = dws.getCapitalDetails(dateRange = 'today')
    # show(simulationCapitalDetails)

    # simulationCapitalDetails = dws.getCapitalDetails(dateRange = 'thisMonth')
    # show(simulationCapitalDetails)

    # status = dws.liquidating()
    # show(status)

    # StockCodeAmountPriceList = [['512290', '1000', '2.169'], ['512290', '1000', None]]
    # res = dws.entrustPortfolio(StockCodeAmountPriceList)
    # show(res)

    # status = service.logoutClient()
    # print(status)
