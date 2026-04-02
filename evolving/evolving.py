# -*- coding: utf-8 -*-

from __future__ import annotations
import os
import json
import time
import subprocess
from typing import Optional
from pprint import pprint as show

from . import ascmds
from . import helper


class Lock:
    def __init__(self):
        self._lockFilePath = os.path.join('/tmp/', 'lock.json')
        self._ensure_lock_file()
        self.unlock()

    def _ensure_lock_file(self):
        directory = os.path.dirname(self._lockFilePath)
        if directory and not os.path.exists(directory):
            os.makedirs(directory, exist_ok=True)
        if not os.path.exists(self._lockFilePath):
            self._write_state(0)

    def _write_state(self, value: int) -> bool:
        try:
            payload = json.dumps({"lock": value}, ensure_ascii=False, sort_keys=True, indent=4)
            tmp_path = self._lockFilePath + '.tmp'
            with open(tmp_path, 'w', encoding='utf8') as fh:
                fh.write(payload)
            os.replace(tmp_path, self._lockFilePath)
            return True
        except Exception:
            return False

    def _read_state(self) -> int:
        try:
            with open(self._lockFilePath, 'r', encoding='utf8') as fp:
                state = json.load(fp)
            if isinstance(state, dict):
                return 1 if state.get("lock") else 0
        except FileNotFoundError:
            self._ensure_lock_file()
        except Exception:
            pass
        return 0

    def lock(self) -> bool:
        return self._write_state(1)

    def unlock(self) -> bool:
        return self._write_state(0)

    def requestLock(self) -> bool:
        islock = self._read_state()
        tolerance = 15
        elapsedTime = 0
        delta = 0.05
        while islock and elapsedTime < tolerance:
            time.sleep(delta)
            elapsedTime += delta
            islock = self._read_state()
        if islock:
            return False
        self.lock()
        return True


def run_command(cmd: str, timeout: int = 30) -> str:
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True,
            timeout=timeout
        )
        return result.stdout.strip()
    except subprocess.TimeoutExpired:
        return "failed"
    except Exception:
        return "failed"


class Service:
    def __init__(self):
        self._config = helper.Config()
        self._logging = helper.Logging(logType='service')
        self._lock = Lock()

    def isClientLoggedIn(self) -> bool:
        cmd = ascmds.asisClientLoggedIn
        res = run_command(cmd)
        return res == "true"

    def loginClient(self) -> bool:
        res = 'failed'
        if self.isClientLoggedIn():
            res = "successed"
        else:
            cmd = ascmds.asloginClient + ' ' + self._config.userid + ' ' + self._config.password
            res = run_command(cmd)

        if res == "successed":
            self._logging.info("login client: " + res)
            self._lock.unlock()
            return True
        else:
            self._logging.error("login client: " + res)
            return False

    def logoutClient(self) -> bool:
        cmd = ascmds.aslogoutClient
        res = run_command(cmd)

        if res == "successed":
            self._logging.info("logout client: " + res)
            self._lock.lock()
            return True
        else:
            self._logging.error("logout client: " + res)
            return False

    def reLoginClient(self) -> bool:
        self.logoutClient()
        time.sleep(1)
        return self.loginClient()


class Base:
    def __init__(self):
        self._config = helper.Config()

    def isBrokerLoggedIn(self) -> bool:
        return False

    def loginBroker(self) -> bool:
        return False

    def logoutBroker(self) -> bool:
        return False

    def getAccountInfo(self) -> dict:
        return {}

    def transfer(self) -> bool:
        return False

    def issuingEntrust(self) -> tuple:
        return (False, None)

    def buy(self) -> tuple:
        return (False, None)

    def sell(self) -> tuple:
        return (False, None)

    def oneKeyIPO(self) -> bool:
        return False


def _send_mail(
    action: str = '',
    assetsName: str = '',
    assetsCode: str = '',
    price: str = '',
    amount: str = '',
    status: str = '',
    comments: str = ''
) -> None:
    try:
        tlog = helper.Tlog(
            action=action,
            assetsName=assetsName,
            assetsCode=assetsCode,
            price=price,
            amount=amount,
            status=status,
            comments=comments
        )
        helper.Mail(tlog)
    except Exception:
        pass


class Evolving(Base):
    def __init__(self):
        super(Evolving, self).__init__()
        self._logging = helper.Logging(logType='env_prod')
        self._keepInformed = False
        self._lock = Lock()

    @property
    def keepInformed(self) -> bool:
        return self._keepInformed

    @keepInformed.setter
    def keepInformed(self, val: bool = True):
        self._keepInformed = val

    def _mailMe(
        self,
        action: str = '',
        assetsName: str = '',
        assetsCode: str = '',
        price: str = '',
        amount: str = '',
        status: str = '',
        comments: str = ''
    ) -> None:
        if self._keepInformed:
            _send_mail(action, assetsName, assetsCode, price, amount, status, comments)

    def isBrokerLoggedIn(self) -> bool:
        status = False
        if not self._lock.requestLock():
            return status

        cmd = ascmds.asisBrokerLoggedIn + ' ' + self._config.broker_code + ' ' + self._config.broker_account + ' ' + self._config.broker_password
        res = run_command(cmd)
        status = True if res == "true" else False
        self._lock.unlock()
        return status

    def loginBroker(self) -> bool:
        status = False
        if not self._lock.requestLock():
            return status

        cmd = ascmds.asloginBroker + ' ' + self._config.broker_code + ' ' + self._config.broker_account + ' ' + self._config.broker_password
        res = run_command(cmd)
        if res == "successed":
            self._logging.info("login broker: " + res)
            status = True
        else:
            self._logging.error("login broker: " + res)
        self._lock.unlock()
        return status

    def logoutBroker(self) -> bool:
        status = False
        if not self._lock.requestLock():
            return status

        cmd = ascmds.aslogoutBroker
        res = run_command(cmd)
        if res == "successed":
            self._logging.info("logout broker: " + res)
            status = True
        else:
            self._logging.error("login broker: " + res)
        self._lock.unlock()
        return status

    def getAccountInfo(self) -> dict:
        accountInfo = {}
        if not self._lock.requestLock():
            return accountInfo

        try:
            cmd = ascmds.asgetAccountInfo
            res = run_command(cmd)
            ls = [x.strip() for x in res.split(',')]
            flag = ls.pop(0)
            accountInfo.update({'status': flag == "successed"})

            doc = {}
            if accountInfo.get("status"):
                while len(ls) > 1:
                    doc.update({ls.pop(0): ls.pop(0)})
                accountInfo.update({'data': doc})
                accountInfo.update({'info': None})
                self._logging.info("get account info successed")
            else:
                accountInfo.update({'data': doc})
                accountInfo.update({'info': ' '.join(ls)})
                self._logging.error("get account info failed: " + str(accountInfo.get('info')))
        except Exception as e:
            self._logging.error("get account info failed: " + str(e))
        self._lock.unlock()
        return accountInfo

    def transfer(self, transferType: str = "bank2broker", amount: int = 100000) -> bool:
        status = False
        if not self._lock.requestLock():
            return status

        try:
            cmd = ascmds.astransfer + ' ' + transferType + ' ' + str(amount) + ' ' + self._config.broker_password + ' ' + self._config.broker_password
            res = run_command(cmd)
            ls = [x.strip() for x in res.split(',')]

            flag = ls.pop(0)
            if flag == "successed":
                status = True
                self._logging.info("transfer successed: " + transferType + ' ' + str(amount))
                self._mailMe(action="transfer", assetsName=transferType, assetsCode='', price='', amount=str(amount), status="successed")
            else:
                info = ' '.join(ls)
                self._logging.error("transfer failed: " + transferType + ' ' + str(amount) + '. Err: ' + info)
                self._mailMe(action="transfer", assetsName=transferType, assetsCode='', price='', amount=str(amount), status="failed")
        except Exception as e:
            self._logging.error("transfer failed: " + transferType + ' ' + str(amount) + '. Err: ' + str(e))
            self._mailMe(action="transfer", assetsName=transferType, assetsCode='', price='', amount=str(amount), status="failed")
        self._lock.unlock()
        return status

    def transfer_bank2broker(self, amount: int = 100000) -> bool:
        return self.transfer(transferType="bank2broker", amount=amount)

    def transfer_broker2bank(self, amount: int = 100000) -> bool:
        return self.transfer(transferType="broker2bank", amount=amount)

    def getTransferRecords(self, dateRange: str = "thisWeek") -> dict:
        transferRecords = {}
        if not self._lock.requestLock():
            return transferRecords

        try:
            cmd = ascmds.asgetTransferRecords + ' ' + dateRange
            res = run_command(cmd)
            ls = [x.strip() for x in res.split(',')]

            flag = ls.pop(0)
            transferRecords.update({'status': flag == "successed"})

            if transferRecords.get('status'):
                length = 7
                transferRecords.update({'comment': [ls.pop(0) for x in range(length) if ls]})
                transferRecords.update({'data': []})
                while ls:
                    transferRecords['data'].append([ls.pop(0) for x in range(length) if ls])
                self._logging.info("get transfer records successed")
            else:
                transferRecords.update({'comment': ''})
                transferRecords.update({'data': []})
                transferRecords.update({'info': ' '.join(ls)})
                self._logging.error("get transfer records failed: " + str(transferRecords.get('info')))
        except Exception as e:
            self._logging.error("get transfer records failed: " + str(e))
        self._lock.unlock()
        return transferRecords

    def getAssetType(self, stockCode: str) -> str:
        if stockCode.startswith('688'):
            return 'sciTech'
        elif stockCode.startswith('300'):
            return 'gem'
        else:
            return 'stock'

    def getBids(self, stockCode: str = "600030", assetType: Optional[str] = None) -> dict:
        bids = {}
        if not self._lock.requestLock():
            return bids

        if assetType is None:
            assetType = self.getAssetType(stockCode)

        try:
            cmd = ascmds.asgetBids + ' ' + assetType + ' ' + stockCode
            res = run_command(cmd)
            ls = [x.strip() for x in res.split(',')]
            flag = ls.pop(0)
            bids.update({'status': flag == "successed"})

            doc = {}
            if bids.get('status'):
                length = 5
                bidsPrice = [ls.pop(0) for x in range(10)]
                ct = 1
                while ct <= length:
                    x = length - ct + 1
                    k = (ls.pop(0) + '_' + str(x)).replace('卖', 'sell')
                    v = {'price': bidsPrice.pop(0), 'vol': ls.pop(0)}
                    doc.update({k: v})
                    ct = ct + 1

                ct = 1
                while ct <= length:
                    x = ct
                    k = (ls.pop(0) + '_' + str(x)).replace('买', 'buy')
                    v = {'price': bidsPrice.pop(0), 'vol': ls.pop(0)}
                    doc.update({k: v})
                    ct = ct + 1
                bids.update({'data': doc})
                bids.update({'info': ''})
                self._logging.info("get bids successed")
            else:
                bids.update({'data': doc})
                bids.update({'info': ' '.join(ls)})
                self._logging.error("get bids failed: " + str(bids.get('info')))
        except Exception as e:
            self._logging.error("get bids failed: " + str(e))
        self._lock.unlock()
        return bids

    def issuingEntrust(
        self,
        stockCode: str,
        amount: int,
        price: Optional[str] = None,
        tradingAction: str = 'buy',
        assetType: Optional[str] = None
    ) -> tuple:
        status = False
        contractNo = None
        if not self._lock.requestLock():
            return status, contractNo

        if assetType is None:
            assetType = self.getAssetType(stockCode)

        try:
            if price is not None:
                price = "{:.2f}".format(float(price)) if not len(str(price).split(".")[1]) > 2 else price

            if assetType == "sciTech":
                assert not (int(amount) < 200)
            else:
                assert not (int(amount) < 100)

            cmd = ascmds.asissuingEntrust + ' ' + tradingAction + ' ' + assetType + ' ' + str(stockCode) + ' ' + str(price) + ' ' + str(amount)
            res = run_command(cmd)
            ls = [x.strip() for x in res.split(',')]

            flag = ls.pop(0)
            if flag == "successed":
                status = True
                contractNo = ls.pop(0)
                self._logging.info("issuing entrust successed: " + tradingAction + ' ' + assetType + ' ' + str(stockCode) + ' ' + str(price) + ' ' + str(amount))
                self._mailMe(action=tradingAction, assetsName=assetType, assetsCode=stockCode, price=str(price), amount=str(amount), status="successed")
            else:
                info = ' '.join(ls)
                self._logging.error("issuing entrust failed: " + tradingAction + ' ' + assetType + ' ' + str(stockCode) + ' ' + str(price) + ' ' + str(amount) + '. Err: ' + info)
                self._mailMe(action=tradingAction, assetsName=assetType, assetsCode=stockCode, price=str(price), amount=str(amount), status="failed")
        except Exception as e:
            self._logging.error("issuing entrust failed: " + tradingAction + ' ' + assetType + ' ' + str(stockCode) + ' ' + str(price) + ' ' + str(amount) + '. Err: ' + str(e))
            self._mailMe(action=tradingAction, assetsName=assetType, assetsCode=stockCode, price=str(price), amount=str(amount), status="failed")
        self._lock.unlock()
        return status, contractNo

    def buy(self, stockCode: str, amount: int, price: Optional[str] = None) -> tuple:
        return self.issuingEntrust(stockCode=stockCode, amount=amount, price=price, tradingAction='buy')

    def sell(self, stockCode: str, amount: int, price: Optional[str] = None) -> tuple:
        return self.issuingEntrust(stockCode=stockCode, amount=amount, price=price, tradingAction='sell')

    def buyStock(self, stockCode: str, amount: int, price: Optional[str] = None) -> tuple:
        return self.issuingEntrust(stockCode, amount, price=price, tradingAction='buy', assetType='stock')

    def sellStock(self, stockCode: str, amount: int, price: Optional[str] = None) -> tuple:
        return self.issuingEntrust(stockCode, amount, price=price, tradingAction='sell', assetType='stock')

    def buySciTech(self, stockCode: str, amount: int, price: Optional[str] = None) -> tuple:
        return self.issuingEntrust(stockCode, amount, price=price, tradingAction='buy', assetType='sciTech')

    def sellSciTech(self, stockCode: str, amount: int, price: Optional[str] = None) -> tuple:
        return self.issuingEntrust(stockCode, amount, price=price, tradingAction='sell', assetType='sciTech')

    def buyGem(self, stockCode: str, amount: int, price: Optional[str] = None) -> tuple:
        return self.issuingEntrust(stockCode, amount, price=price, tradingAction='buy', assetType='gem')

    def sellGem(self, stockCode: str, amount: int, price: Optional[str] = None) -> tuple:
        return self.issuingEntrust(stockCode, amount, price=price, tradingAction='sell', assetType='gem')

    def getTodayIPO(self) -> dict:
        todayIPO = {}
        if not self._lock.requestLock():
            return todayIPO

        try:
            cmd = ascmds.asgetTodayIPO
            res = run_command(cmd)
            ls = [x.strip() for x in res.split(',')]

            flag = ls.pop(0)
            todayIPO.update({'status': flag == "successed"})

            if todayIPO.get("status"):
                length = 4
                todayIPO.update({'comment': [ls.pop(0) for x in range(length) if ls]})
                todayIPO.update({'data': []})
                while ls:
                    todayIPO['data'].append([ls.pop(0) for x in range(length) if ls])
                todayIPO.update({'info': ''})
                self._logging.info("get today IPO successed")
            else:
                todayIPO.update({'comment': ''})
                todayIPO.update({'data': []})
                todayIPO.update({'info': ' '.join(ls)})
                self._logging.error("get today IPO failed: " + str(todayIPO.get('info')))
        except Exception as e:
            self._logging.error("get today IPO failed: " + str(e))
        self._lock.unlock()
        return todayIPO

    def oneKeyIPO(self) -> bool:
        status = False
        if not self._lock.requestLock():
            return status

        try:
            cmd = ascmds.asoneKeyIPO
            res = run_command(cmd)
            ls = [x.strip() for x in res.split(',')]

            flag = ls.pop(0)
            if flag == "successed":
                status = True
                self._logging.info("auto IPO successed")
                self._mailMe(action="auto IPO", assetsName='', assetsCode='', price='', amount='', status="successed")
            else:
                info = ' '.join(ls)
                self._logging.error("auto IPO failed: " + info)
                self._mailMe(action="auto IPO", assetsName='', assetsCode='', price='', amount='', status="failed")
        except Exception as e:
            self._logging.error("IPO failed: " + str(e))
            self._mailMe(action="IPO", assetsName='', assetsCode='', price='', amount='', status="failed")
        self._lock.unlock()
        return status

    def revokeEntrust(
        self,
        revokeType: str = "allBuyAndSell",
        assetType: str = "stock",
        contractNo: Optional[str] = None
    ) -> bool:
        status = False
        if not self._lock.requestLock():
            return status

        try:
            cmd = ascmds.asrevokeEntrust + " " + revokeType + " " + assetType + " " + str(contractNo)
            res = run_command(cmd)
            ls = [x.strip() for x in res.split(',')]

            flag = ls.pop(0)
            info = ls.pop(0)
            if flag == "successed":
                status = True
                self._logging.info("revoke entrust successed: " + revokeType + " " + assetType + " " + str(contractNo) + ". Info: " + info)
                self._mailMe(action="revoke entrust " + revokeType, assetsName=assetType, assetsCode=str(contractNo), price='', amount='', status="successed")
            else:
                self._logging.error("revoke entrust failed: " + revokeType + " " + assetType + " " + str(contractNo) + ". Err: " + info)
                self._mailMe(action="revoke entrust " + revokeType, assetsName=assetType, assetsCode=str(contractNo), price='', amount='', status="failed")
        except Exception as e:
            self._logging.error("revoke entrust failed: " + revokeType + " " + assetType + " " + str(contractNo) + ". Err: " + str(e))
            self._mailMe(action="revoke entrust " + revokeType, assetsName=assetType, assetsCode=str(contractNo), price='', amount='', status="failed")
        self._lock.unlock()
        return status

    def revokeAllBuyEntrust(self) -> bool:
        status = False
        if not self._lock.requestLock():
            return status

        try:
            cmd = ascmds.asrevokeAllBuyEntrust
            res = run_command(cmd)
            ls = [x.strip() for x in res.split(',')]

            flag = ls.pop(0)
            if flag == "successed":
                status = True
                self._logging.info("revoke all sell entrust successed")
                self._mailMe(action="revoke all sell entrust", status='successed')
            else:
                self._logging.error("revoke all sell entrust failed")
                self._mailMe(action="revoke all sell entrust", status="failed")
        except Exception as e:
            self._logging.error("revoke all sell entrust failed Err: " + str(e))
            self._mailMe(action="revoke all sell entrust", status="failed")
        self._lock.unlock()
        return status

    def revokeAllSellEntrust(self) -> bool:
        status = False
        if not self._lock.requestLock():
            return status

        try:
            cmd = ascmds.asrevokeAllSellEntrust
            res = run_command(cmd)
            ls = [x.strip() for x in res.split(',')]

            flag = ls.pop(0)
            if flag == "successed":
                status = True
                self._logging.info("revoke all buy entrust successed")
                self._mailMe(action="revoke all buy entrust", status='successed')
            else:
                self._logging.error("revoke all buy entrust failed")
                self._mailMe(action="revoke all buy entrust", status="failed")
        except Exception as e:
            self._logging.error("revoke all buy entrust failed Err: " + str(e))
            self._mailMe(action="revoke all buy entrust", status="failed")
        self._lock.unlock()
        return status

    def revokeAllEntrust(self) -> bool:
        status = False
        if not self._lock.requestLock():
            return status

        try:
            cmd = ascmds.asrevokeAllEntrust
            res = run_command(cmd)
            ls = [x.strip() for x in res.split(',')]

            flag = ls.pop(0)
            if flag == "successed":
                status = True
                self._logging.info("revoke all entrust successed")
                self._mailMe(action="revoke all entrust", status='successed')
            else:
                self._logging.error("revoke all entrust failed")
                self._mailMe(action="revoke all entrust", status="failed")
        except Exception as e:
            self._logging.error("revoke all entrust failed Err: " + str(e))
            self._mailMe(action="revoke all entrust", status="failed")
        self._lock.unlock()
        return status

    def revokeContractNoEntrust(self, assetType: str = "stock", contractNo: str = "N8743678") -> bool:
        return self.revokeEntrust(revokeType="contractNo", assetType=assetType, contractNo=contractNo)

    def getHoldingShares(self, assetType: str = 'stock') -> dict:
        holdingShares = {}
        if not self._lock.requestLock():
            return holdingShares

        try:
            cmd = ascmds.asgetHoldingShares + ' ' + assetType
            res = run_command(cmd)
            ls = [x.strip() for x in res.split(',')]

            flag = ls.pop(0)
            holdingShares.update({'status': flag == "successed"})

            if holdingShares.get("status"):
                length = 15 if assetType in ['stock'] else 13
                holdingShares.update({'comment': [ls.pop(0) for x in range(length) if ls]})
                holdingShares.update({'data': []})
                while ls:
                    holdingShares['data'].append([ls.pop(0) for x in range(length) if ls])
                holdingShares.update({'info': ''})
                self._logging.info("get holding shares successed")
            else:
                holdingShares.update({'comment': ''})
                holdingShares.update({'data': []})
                holdingShares.update({'info': ' '.join(ls)})
                self._logging.error("get holding shares failed: " + str(holdingShares.get('info')))
        except Exception as e:
            self._logging.error("get holding shares failed: " + str(e))
        self._lock.unlock()
        return holdingShares

    def getAllHoldingShares(self) -> dict:
        res1 = self.getHoldingShares(assetType='stock')
        res2 = self.getHoldingShares(assetType='sciTech')
        res3 = self.getHoldingShares(assetType='gem')
        return {"stock": res1, "sciTech": res2, "gem": res3}

    def getEntrust(self, assetType: str = 'stock', dateRange: str = 'today', isRevocable: bool = True) -> dict:
        entrust = {}
        if not self._lock.requestLock():
            return entrust

        try:
            cmd = ascmds.asgetEntrust + ' ' + assetType + ' ' + dateRange + ' ' + str(isRevocable).lower()
            res = run_command(cmd)
            ls = [x.strip() for x in res.split(',')]

            flag = ls.pop(0)
            entrust.update({'status': flag == "successed"})

            if entrust.get('status'):
                length = 13 if assetType in ['sciTech', 'gem'] else 11
                entrust.update({'comment': [ls.pop(0) for x in range(length) if ls]})
                entrust.update({'data': []})
                while ls:
                    entrust['data'].append([ls.pop(0) for x in range(length) if ls])
                entrust.update({'info': ''})
                self._logging.info("get entrust successed")
            else:
                entrust.update({'comment': ''})
                entrust.update({'data': []})
                entrust.update({'info': ' '.join(ls)})
                self._logging.error("get entrust failed: " + str(entrust.get('info')))
        except Exception as e:
            self._logging.error("get entrust failed: " + str(e))
        self._lock.unlock()
        return entrust

    def getTodayAllRevocableEntrust(self) -> dict:
        res1 = self.getEntrust(assetType='stock', dateRange='today', isRevocable=True)
        res2 = self.getEntrust(assetType='sciTech', dateRange='today', isRevocable=True)
        res3 = self.getEntrust(assetType='gem', dateRange='today', isRevocable=True)
        return {"stock": res1, "sciTech": res2, "gem": res3}

    def getClosedDeals(self, assetType: str = 'stock', dateRange: str = 'today') -> dict:
        closedDeals = {}
        if not self._lock.requestLock():
            return closedDeals

        try:
            cmd = ascmds.asgetClosedDeals + ' ' + assetType + ' ' + dateRange
            res = run_command(cmd)
            ls = [x.strip() for x in res.split(',')]

            flag = ls.pop(0)
            closedDeals.update({'status': flag == "successed"})

            if closedDeals.get("status"):
                length = 10
                closedDeals.update({'comment': [ls.pop(0) for x in range(length) if ls]})
                closedDeals.update({'data': []})
                while ls:
                    closedDeals['data'].append([ls.pop(0) for x in range(length) if ls])
                closedDeals.update({'info': None})
                self._logging.info("get closed deals successed")
            else:
                closedDeals.update({'comment': ''})
                closedDeals.update({'data': []})
                closedDeals.update({'info': ' '.join(ls)})
                self._logging.error("get closed deals failed: " + str(closedDeals.get('info')))
        except Exception as e:
            self._logging.error("get closed deals failed: " + str(e))
        self._lock.unlock()
        return closedDeals

    def getCapitalDetails(self, assetType: str = 'stock', dateRange: str = 'thisSeason') -> dict:
        capitalDetails = {}
        if not self._lock.requestLock():
            return capitalDetails

        try:
            cmd = ascmds.asgetCapitalDetails + ' ' + assetType + ' ' + dateRange
            res = run_command(cmd)
            ls = [x.strip() for x in res.split(',')]

            flag = ls.pop(0)
            capitalDetails.update({'status': flag == "successed"})

            if capitalDetails.get("status"):
                length = 11
                capitalDetails.update({'comment': [ls.pop(0) for x in range(length) if ls]})
                capitalDetails.update({'data': []})
                while ls:
                    capitalDetails['data'].append([ls.pop(0) for x in range(length) if ls])
                capitalDetails.update({'info': ''})
                self._logging.info("get capital details successed")
            else:
                capitalDetails.update({'comment': ''})
                capitalDetails.update({'data': []})
                capitalDetails.update({'info': ' '.join(ls)})
                self._logging.error("get capital details failed: " + str(capitalDetails.get('info')))
        except Exception as e:
            self._logging.error("get capital details failed: " + str(e))
        self._lock.unlock()
        return capitalDetails

    def getIPO(self, queryType: str = "entrust", dateRange: str = "today") -> dict:
        result = {}
        if not self._lock.requestLock():
            return result

        try:
            cmd = ascmds.asgetIPO + ' ' + queryType + ' ' + dateRange
            res = run_command(cmd)
            ls = [x.strip() for x in res.split(',')]

            flag = ls.pop(0)
            result.update({'status': flag == "successed"})

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
                    self._logging.error("get IPO failed: " + queryType + " " + dateRange + ". Err: " + str(result.get('info')))
                    self._lock.unlock()
                    return result

                result.update({'comment': [ls.pop(0) for x in range(length) if ls]})
                result.update({'data': []})
                while ls:
                    result['data'].append([ls.pop(0) for x in range(length) if ls])
                result.update({'info': ''})
                self._logging.info("get IPO successed: " + queryType + " " + dateRange)
            else:
                result.update({'comment': ''})
                result.update({'data': []})
                result.update({'info': ' '.join(ls)})
                self._logging.error("get IPO failed: " + queryType + " " + dateRange + ". Err: " + str(result.get('info')))
        except Exception as e:
            self._logging.error("get IPO failed: " + queryType + " " + dateRange + ". Err: " + str(e))
        self._lock.unlock()
        return result

    def getIPOentrust(self, dateRange: str = "today") -> dict:
        return self.getIPO(queryType="entrust", dateRange="today")

    def getIPOallotmentNo(self, dateRange: str = "today") -> dict:
        return self.getIPO(queryType="allotmentNo", dateRange="today")

    def getIPOwinningLots(self, dateRange: str = "today") -> dict:
        return self.getIPO(queryType="winningLots", dateRange="today")

    def liquidating(self) -> bool:
        try:
            for _ in range(3):
                self.revokeAllEntrust()
                allHoldingShares = self.getAllHoldingShares()
                show(allHoldingShares)
                stock_data = allHoldingShares.get("stock") or {}
                scitech_data = allHoldingShares.get("sciTech") or {}
                gem_data = allHoldingShares.get("gem") or {}
                if stock_data.get("status") and scitech_data.get("status") and gem_data.get("status"):
                    l = []
                    for assetType in ["stock", "sciTech", "gem"]:
                        dt = (allHoldingShares.get(assetType) or {}).get("data")
                        if dt and dt[0] and dt[0][0]:
                            l.extend([[assetType, x[0], x[7]] for x in dt if x[7] and int(x[7])])
                    if l and l[0]:
                        for assetType, stockCode, availableQuantity in l:
                            if assetType == "stock":
                                self.sellStock(stockCode, availableQuantity)
                            if assetType == "sciTech":
                                self.sellSciTech(stockCode, availableQuantity)
                            if assetType == "gem":
                                self.sellGem(stockCode, availableQuantity)
                        time.sleep(3.5)
                    else:
                        self._logging.info("liquidating successed")
                        return True
        except Exception as e:
            self._logging.error("liquidating failed: " + str(e))
        return False

    def entrustPortfolio(self, StockCodeAmountPriceList: list) -> list:
        statusList = []
        for stockCode, amount, price in StockCodeAmountPriceList:
            try:
                status, contractNo = self.issuingEntrust(stockCode=stockCode, amount=amount, price=price, tradingAction="buy")
                statusList.append({'stockCode': stockCode, 'status': status, 'contractNo': contractNo})
                self._logging.info("entrust buy successed")
            except Exception as e:
                self._logging.error("entrust buy failed: " + str(e))
                statusList.append({'stockCode': stockCode, 'status': 'failed', 'contractNo': None})
        return statusList


class EvolvingSim:
    pass
