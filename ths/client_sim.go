package ths

import (
	"strconv"
	"strings"
	"sync"
)

type thsSimClient struct {
	mu sync.Mutex
}

var (
	simInstance *thsSimClient
	simOnce     sync.Once
)

func GetThsSimClient() *thsSimClient {
	simOnce.Do(func() {
		simInstance = &thsSimClient{}
	})
	return simInstance
}

func (t *thsSimClient) getLock() error {
	if !t.mu.TryLock() {
		return ErrResourceBusy
	}
	return nil
}

func (t *thsSimClient) unLock() {
	t.mu.Unlock()
}

func (t *thsSimClient) isLocked() bool {
	if t.mu.TryLock() {
		t.mu.Unlock()
		return false
	}
	return true
}

func (t *thsSimClient) IsClientLoggedIn() (bool, error) {
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

func (t *thsSimClient) LoginClient(userID, password string) (bool, error) {
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

func (t *thsSimClient) LogoutClient() (bool, error) {
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

func (t *thsSimClient) isClientLoggedInNoLock() bool {
	res, err := Run(AsIsClientLoggedIn)
	if err != nil {
		return false
	}
	return strings.TrimSpace(res) == "true"
}

func (t *thsSimClient) GetAccountInfo() (string, error) {
	if err := t.getLock(); err != nil {
		return "", err
	}
	defer t.unLock()
	return Run(AsGetAccountInfoSim)
}

func (t *thsSimClient) IssuingEntrust(tradingAction, assetType, stockCode, price string, amount int) (string, error) {
	if err := t.getLock(); err != nil {
		return "", err
	}
	defer t.unLock()
	return Run(AsIssuingEntrustSim + " " + tradingAction + " " + assetType + " " + stockCode + " " + price + " " + strconv.Itoa(amount))
}

func (t *thsSimClient) GetHoldingShares(assetType string) (string, error) {
	if err := t.getLock(); err != nil {
		return "", err
	}
	defer t.unLock()
	return Run(AsGetHoldingSharesSim + " " + assetType)
}

func (t *thsSimClient) GetEntrust(assetType, dateRange string, isRevocable bool) (string, error) {
	if err := t.getLock(); err != nil {
		return "", err
	}
	defer t.unLock()
	return Run(AsGetEntrustSim + " " + assetType + " " + dateRange + " " + strconv.FormatBool(isRevocable))
}

func (t *thsSimClient) RevokeEntrust(revokeType, assetType, contractNo string) (string, error) {
	if err := t.getLock(); err != nil {
		return "", err
	}
	defer t.unLock()
	return Run(AsRevokeEntrustSim + " " + revokeType + " " + assetType + " " + contractNo)
}

func (t *thsSimClient) GetClosedDeals(assetType, dateRange string) (string, error) {
	if err := t.getLock(); err != nil {
		return "", err
	}
	defer t.unLock()
	return Run(AsGetClosedDealsSim + " " + assetType + " " + dateRange)
}

func (t *thsSimClient) GetCapitalDetails(assetType, dateRange string) (string, error) {
	if err := t.getLock(); err != nil {
		return "", err
	}
	defer t.unLock()
	return Run(AsGetCapitalDetailsSim + " " + assetType + " " + dateRange)
}
