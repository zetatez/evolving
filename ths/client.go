package ths

import (
	"errors"
	"strconv"
	"strings"
	"sync"
)

var ErrResourceBusy = errors.New("resource is busy")

type thsClient struct {
	mu sync.Mutex
}

var (
	instance *thsClient
	once     sync.Once
)

func GetThsClient() *thsClient {
	once.Do(func() {
		instance = &thsClient{}
	})
	return instance
}

func (t *thsClient) getLock() error {
	if !t.mu.TryLock() {
		return ErrResourceBusy
	}
	return nil
}

func (t *thsClient) unLock() {
	t.mu.Unlock()
}

func (t *thsClient) isLocked() bool {
	if t.mu.TryLock() {
		t.mu.Unlock()
		return false
	}
	return true
}

func (t *thsClient) GetAssetType(stockCode string) string {
	if strings.HasPrefix(stockCode, "688") {
		return "sciTech"
	}
	if strings.HasPrefix(stockCode, "300") {
		return "gem"
	}
	return "stock"
}

func (t *thsClient) IsClientLoggedIn() (bool, error) {
	if err := t.getLock(); err != nil {
		return false, err
	}
	defer t.unLock()
	res, err := Run(AsIsClientLoggedIn)
	if err != nil {
		return false, err
	}
	return strings.TrimSpace(res) == "true", nil
}

func (t *thsClient) LoginClient(userID, password string) (bool, error) {
	if err := t.getLock(); err != nil {
		return false, err
	}
	defer t.unLock()
	if t.isClientLoggedInNoLock() {
		return true, nil
	}
	script := AsLoginClient + " " + userID + " " + password
	res, err := Run(script)
	if err != nil {
		return false, err
	}
	return strings.TrimSpace(res) == "successed", nil
}

func (t *thsClient) LogoutClient() (bool, error) {
	if err := t.getLock(); err != nil {
		return false, err
	}
	defer t.unLock()
	res, err := Run(AsLogoutClient)
	if err != nil {
		return false, err
	}
	return strings.TrimSpace(res) == "successed", nil
}

func (t *thsClient) ReLoginClient(userID, password string) (bool, error) {
	if err := t.getLock(); err != nil {
		return false, err
	}
	defer t.unLock()
	if _, err := Run(AsLogoutClient); err != nil {
		return false, err
	}
	script := AsLoginClient + " " + userID + " " + password
	res, err := Run(script)
	if err != nil {
		return false, err
	}
	return strings.TrimSpace(res) == "successed", nil
}

func (t *thsClient) isClientLoggedInNoLock() bool {
	res, err := Run(AsIsClientLoggedIn)
	if err != nil {
		return false
	}
	return strings.TrimSpace(res) == "true"
}

func (t *thsClient) IsBrokerLoggedIn() (bool, error) {
	if err := t.getLock(); err != nil {
		return false, err
	}
	defer t.unLock()
	res, err := Run(AsIsBrokerLoggedIn)
	if err != nil {
		return false, err
	}
	return strings.TrimSpace(res) == "true", nil
}

func (t *thsClient) LoginBroker(brokerName, brokerAccount, brokerPassword string) (bool, error) {
	if err := t.getLock(); err != nil {
		return false, err
	}
	defer t.unLock()
	script := AsLoginBroker + " " + brokerName + " " + brokerAccount + " " + brokerPassword
	res, err := Run(script)
	if err != nil {
		return false, err
	}
	return strings.TrimSpace(res) == "successed", nil
}

func (t *thsClient) LogoutBroker() (bool, error) {
	if err := t.getLock(); err != nil {
		return false, err
	}
	defer t.unLock()
	res, err := Run(AsLogoutBroker)
	if err != nil {
		return false, err
	}
	return strings.TrimSpace(res) == "successed", nil
}

func (t *thsClient) Transfer(transferType string, amount int, bankPassword, brokerPassword string) (bool, error) {
	if err := t.getLock(); err != nil {
		return false, err
	}
	defer t.unLock()
	var script string
	if transferType == "broker2bank" {
		script = AsTransferBroker2Bank + " " + transferType + " " + strconv.Itoa(amount) + " " + bankPassword + " " + brokerPassword
	} else {
		script = AsTransferBank2Broker + " " + transferType + " " + strconv.Itoa(amount) + " " + bankPassword + " " + brokerPassword
	}
	_, err := Run(script)
	if err != nil {
		return false, err
	}
	return true, nil
}

func (t *thsClient) TransferBank2Broker(amount int, bankPassword, brokerPassword string) (bool, error) {
	return t.Transfer("bank2broker", amount, bankPassword, brokerPassword)
}

func (t *thsClient) TransferBroker2Bank(amount int, bankPassword, brokerPassword string) (bool, error) {
	return t.Transfer("broker2bank", amount, bankPassword, brokerPassword)
}

func (t *thsClient) GetBids(stockCode, assetType string) (string, error) {
	if err := t.getLock(); err != nil {
		return "", err
	}
	defer t.unLock()
	if assetType == "" {
		assetType = t.GetAssetType(stockCode)
	}
	var script string
	switch assetType {
	case "sciTech":
		script = AsGetBidsSciTech
	case "gem":
		script = AsGetBidsGem
	default:
		script = AsGetBidsStock
	}
	return Run(script + " " + assetType + " " + stockCode)
}

func (t *thsClient) Buy(stockCode string, amount int, price, assetType string) (string, error) {
	if err := t.getLock(); err != nil {
		return "", err
	}
	defer t.unLock()
	if assetType == "" {
		assetType = t.GetAssetType(stockCode)
	}
	var script string
	switch assetType {
	case "sciTech":
		script = AsIssuingEntrustBuySciTech
	case "gem":
		script = AsIssuingEntrustBuyGem
	default:
		script = AsIssuingEntrustBuyStock
	}
	return Run(script + " buy " + assetType + " " + stockCode + " " + price + " " + strconv.Itoa(amount))
}

func (t *thsClient) Sell(stockCode string, amount int, price, assetType string) (string, error) {
	if err := t.getLock(); err != nil {
		return "", err
	}
	defer t.unLock()
	if assetType == "" {
		assetType = t.GetAssetType(stockCode)
	}
	var script string
	switch assetType {
	case "sciTech":
		script = AsIssuingEntrustSellSciTech
	case "gem":
		script = AsIssuingEntrustSellGem
	default:
		script = AsIssuingEntrustSellStock
	}
	return Run(script + " sell " + assetType + " " + stockCode + " " + price + " " + strconv.Itoa(amount))
}

func (t *thsClient) GetHoldingShares(assetType string) (string, error) {
	if err := t.getLock(); err != nil {
		return "", err
	}
	defer t.unLock()
	var script string
	switch assetType {
	case "sciTech":
		script = AsGetHoldingSharesSciTech
	case "gem":
		script = AsGetHoldingSharesGem
	default:
		script = AsGetHoldingSharesStock
	}
	return Run(script + " " + assetType)
}

func (t *thsClient) GetEntrust(assetType string, isRevocable bool) (string, error) {
	if err := t.getLock(); err != nil {
		return "", err
	}
	defer t.unLock()
	return Run(AsGetEntrustToday + " " + assetType + " today " + strconv.FormatBool(isRevocable))
}

func (t *thsClient) GetClosedDeals(assetType string) (string, error) {
	if err := t.getLock(); err != nil {
		return "", err
	}
	defer t.unLock()
	return Run(AsGetClosedDealsToday + " " + assetType + " today")
}

func (t *thsClient) RevokeEntrust(assetType string) (string, error) {
	if err := t.getLock(); err != nil {
		return "", err
	}
	defer t.unLock()
	var script string
	switch assetType {
	case "sciTech":
		script = AsRevokeEntrustAllBuyAndSellSciTech
	case "gem":
		script = AsRevokeEntrustAllBuyAndSellGem
	default:
		script = AsRevokeEntrustAllBuyAndSellStock
	}
	return Run(script + " allBuyAndSell " + assetType + " \"\"")
}

func (t *thsClient) RevokeAllEntrust() (string, error) {
	if err := t.getLock(); err != nil {
		return "", err
	}
	defer t.unLock()
	return Run(AsRevokeAllEntrust)
}

func (t *thsClient) OneKeyIPO() (string, error) {
	if err := t.getLock(); err != nil {
		return "", err
	}
	defer t.unLock()
	return Run(AsOneKeyIPO)
}

func (t *thsClient) GetTodayIPO() (string, error) {
	if err := t.getLock(); err != nil {
		return "", err
	}
	defer t.unLock()
	return Run(AsGetTodayIPO)
}

func (t *thsClient) GetAccountInfo() (string, error) {
	if err := t.getLock(); err != nil {
		return "", err
	}
	defer t.unLock()
	return Run(AsGetAccountInfo)
}

func (t *thsClient) GetTransferRecords(dateRange string) (string, error) {
	if err := t.getLock(); err != nil {
		return "", err
	}
	defer t.unLock()
	return Run(AsGetTransferRecords + " " + dateRange)
}

func (t *thsClient) RevokeAllBuyEntrust() (string, error) {
	if err := t.getLock(); err != nil {
		return "", err
	}
	defer t.unLock()
	return Run(AsRevokeAllBuyEntrust)
}

func (t *thsClient) RevokeAllSellEntrust() (string, error) {
	if err := t.getLock(); err != nil {
		return "", err
	}
	defer t.unLock()
	return Run(AsRevokeAllSellEntrust)
}

func (t *thsClient) GetCapitalDetails(assetType, dateRange string) (string, error) {
	if err := t.getLock(); err != nil {
		return "", err
	}
	defer t.unLock()
	return Run(AsGetCapitalDetails + " " + assetType + " " + dateRange)
}

func (t *thsClient) GetIPO(queryType, dateRange string) (string, error) {
	if err := t.getLock(); err != nil {
		return "", err
	}
	defer t.unLock()
	return Run(AsGetIPO + " " + queryType + " " + dateRange)
}
