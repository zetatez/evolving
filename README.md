# Looking For Maintainers

# Welcome to the evolving

`evolving` is an automated trading engine for MacOS that interacts with the Tonghuashun (同花顺) client via AppleScript. It enables programmatic stock trading, bank-stock transfers, and portfolio management.

<center><img src="http://latex.codecogs.com/gif.latex?S_T=S_0\int_Te^{r(t)}du"/></center>

## Features

- Automated stock trading (A-shares, STAR, GEM)
- Bank-stock fund transfers
- Order management and revocation
- Portfolio queries
- One-click IPO subscription
- Email notifications

## Supported Brokers

Currently supported: ZXZQ (中信证券), PAZQ (平安证券), ZSZQ (浙商证券), GTJA (国泰君安), GJZQ (国金证券), XYZQ (兴业证券), ZJZQ (中金证券), ZTZQ (中泰证券).

The broker login logic is implemented in `ascmds.py`. Users can add support for other brokers by modifying the `asloginBroker` handler.

## Requirements

- MacOS
- cliclick >= 4.0.1
- Python >= 3.8.5
- 同花顺 Version 2.3.1

## Installation

```bash
brew install cliclick
pip install -r requirements.txt
```

## Configuration

```bash
mkdir -p ~/.config/evolving
vim ~/.config/evolving/config.yaml
```

```yaml
evolving:
  trading:
    userid: YOUR_THS_ID
    password: YOUR_THS_PASSWORD
    broker_code: PAZQ
    broker_account: YOUR_BROKER_ACCOUNT
    broker_password: YOUR_BROKER_PASSWORD
    bank_name: YOUR_BANK_NAME
    bank_account: YOUR_BANK_ACCOUNT
    bank_password: YOUR_BANK_PASSWORD
  mail:
    mail_host: smtp.163.com
    mail_sender: your_email@163.com
    mail_license: YOUR_EMAIL_LICENSE
    mail_receivers:
      - your_email@163.com
```

`mail_receivers` can also be a semicolon-separated string.

## Authorization

Mac -> System Preference -> Security & Privacy -> Privacy -> unlock -> **Accessibility** AND **Full Disk Access**
- [x] Terminal
- [x] osascript

## Usage Example

```python
from evolving import Evolving

# Initialize trading engine
trader = Evolving()

# Login to broker
trader.loginBroker()

# Buy 100 shares at 10.0 yuan
trader.buyStock(stock_code="600519", price=10.0, amount=100)

# Transfer 10000 yuan from bank to broker
trader.transfer_bank2broker(bank_amount=10000)

# Get current holdings
holdings = trader.getHoldingShares()

# Revoke all entrustments
trader.revokeAllEntrust()

# Logout
trader.logoutBroker()
```

## Project Structure

```
evolving/
├── evolving.py          # Core trading engine (Evolving class)
├── helper.py            # Utilities (Config, Mail, Logging)
├── ascmds.py            # AppleScript commands for Tonghuashun
└── __init__.py          # Package exports
```

## Notes

- You need to log in to your broker and bank account manually at least once before first use
- Email notifications require a 163 email account
- Different brokers may have slightly different UI interactions; see `ascmds.py` for customization

## Tutorial

A detailed tutorial is available at the [wiki](https://github.com/zetatez/evolving/wiki).

## License

Released under the [MIT](./LICENSE) License.

## Get in Touch

- E-mail: zetatez@icloud.com
- Wechat Group

  <img src="https://raw.githubusercontent.com/zetatez/evolving/main/wechatgroup.jpg" alt="wechat group" width="120" align="top" />
