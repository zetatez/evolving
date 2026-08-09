

```markdown
# evolving

MacOS automated trading engine for Tonghuashun (同花顺) via AppleScript.

## Features

- Stock trading (A-share, STAR, GEM)
- Bank-broker fund transfers
- Order management
- Holdings and entrustment queries
- IPO subscription
- Simulation trading

## Structure

```
ths/
├── ascmds.go        # osascript executor
├── client.go        # thsClient (production) singleton
├── client_sim.go    # thsSimClient (simulation) singleton
├── consts.go        # production AppleScript constants (34)
└── consts_sim.go    # simulation AppleScript constants (7)
```

## Requirements

- MacOS
- cliclick >= 4.0.1 (`brew install cliclick`)
- Tonghuashun client

## Usage

```go
import "evolving/ths"

client := ths.GetThsClient()
simClient := ths.GetThsSimClient()
```

### thsClient (production)

```go
// Client login/logout
client.LoginClient(userID, password string) (bool, error)
client.LogoutClient() (bool, error)
client.IsClientLoggedIn() (bool, error)
client.ReLoginClient(userID, password string) (bool, error)

// Broker login/logout
client.LoginBroker(brokerName, account, password string) (bool, error)
client.LogoutBroker() (bool, error)
client.IsBrokerLoggedIn() (bool, error)

// Trading
client.Buy(stockCode string, amount int, price, assetType string) (string, error)
client.Sell(stockCode string, amount int, price, assetType string) (string, error)
client.Transfer(transferType string, amount int, bankPassword, brokerPassword string) (bool, error)
client.TransferBank2Broker(amount int, bankPassword, brokerPassword string) (bool, error)
client.TransferBroker2Bank(amount int, bankPassword, brokerPassword string) (bool, error)

// Revoke
client.RevokeAllEntrust() (string, error)
client.RevokeAllBuyEntrust() (string, error)
client.RevokeAllSellEntrust() (string, error)
client.RevokeEntrust(assetType string) (string, error)

// Queries
client.GetAccountInfo() (string, error)
client.GetHoldingShares(assetType string) (string, error)  // stock/sciTech/gem
client.GetEntrust(assetType string, isRevocable bool) (string, error)
client.GetClosedDeals(assetType string) (string, error)
client.GetBids(stockCode, assetType string) (string, error)
client.GetTransferRecords(dateRange string) (string, error)
client.GetCapitalDetails(assetType, dateRange string) (string, error)

// IPO
client.OneKeyIPO() (string, error)
client.GetTodayIPO() (string, error)
client.GetIPO(queryType, dateRange string) (string, error)

// Asset type detection
client.GetAssetType(stockCode string) string  // stock/sciTech/gem
```

### thsSimClient (simulation)

```go
simClient.LoginClient(userID, password string) (bool, error)
simClient.LogoutClient() (bool, error)
simClient.IsClientLoggedIn() (bool, error)
simClient.GetAccountInfo() (string, error)
simClient.GetHoldingShares(assetType string) (string, error)
simClient.GetEntrust(assetType, dateRange string, isRevocable bool) (string, error)
simClient.GetClosedDeals(assetType, dateRange string) (string, error)
simClient.GetCapitalDetails(assetType, dateRange string) (string, error)
simClient.IssuingEntrust(tradingAction, assetType, stockCode, price string, amount int) (string, error)
simClient.RevokeEntrust(revokeType, assetType, contractNo string) (string, error)
```

## Permissions

Mac -> System Settings -> Privacy & Security -> Accessibility / Full Disk Access
- [x] Terminal
- [x] osascript

## License

MIT
```
