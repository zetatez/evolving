# Welcome to the evolving !
This is a repo for the [`evolving`](https://github.com/zetatez/evolving) trading engine under the MacOS system.

<img src="http://latex.codecogs.com/gif.latex?S_T=S_0\int_Te^{r(t)}du"/>

## Author
[`evolving`](https://github.com/zetatez/evolving) ©[Lorenzo](https://github.com/zetatez), Released under the [GPL-3.0](./LICENSE) License.

## Get in touch!

In order to get in touch with the author, join [Gitter](https://badges.gitter.im/zetatez-evolving/evolving.svg) or [wechat group](https://raw.githubusercontent.com/zetatez/evolving/main/wechatgroup.jpg).

- Wechat Group

    <img src="https://raw.githubusercontent.com/zetatez/evolving/main/wechatgroup.jpg" alt="wechat group" width="120" align="top" />

- E-mail: zetatez@icloud.com

## How to contribute
To contribute in this repo, please open a [pull request](https://help.github.com/articles/using-pull-requests/#fork--pull) from your fork of this repo.

## Repo structure
```bash
tree evolving
    evolving
    ├── LICENSE
    ├── README.md
    ├── evo
    ├── evolving
    │   ├── ascmds.py
    │   ├── evolving.py
    │   └── helper.py
    │   └── top_level.txt
    ├── requirements.txt
    ├── setup.py
    ├── tests
    │   ├── __init__.py
    │   ├── evolving.py
    │   └── helper.py
    └── wechatgroup.jpg

tree ~/.config/evolving
    ~/.config/evolving
    └── config.xml
```

## Installation guide
1. Requirements
    - python >= 3.8.5
    - 同花顺 == Version 2.3.0 or 2.3.1

2. Dependencies
    ```bash
    brew install cliclick
    cliclick -V             # cliclick 4.0.1, 2018-04-10
    which cliclick          # /usr/local/bin/cliclick

    pip install `curl -fsSL https://raw.githubusercontent.com/zetatez/evolving/main/requirements.txt`
    ```

3. Installation
   - Building `evolving` from pip
       ```bash
       pip install evolving
       ```

   - Building `evolving` from source
       ```bash
       git clone git@github.com:zetatez/evolving.git ~/evolving; cd ~/evolving; python setup.py install
       ```

4. Configuration
    ```bash
    mkdir -p ~/.ipython/profile_default/startup/
    mkdir -p ~/.config/evolving

    # Note: 
    # 1. You need to log in broker and bank account manually at least once.
    # 2. If you want to use the email notification module, you need to register a 163 email account.
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

 5. Authorization
    - Mac -> Systerm Preference -> Security & Privacy -> Privacy -> unluck -> Accessibility
        - [x] Terminal
        - [x] osascript
    - Mac -> Systerm Preference -> Security & Privacy -> Privacy -> unluck -> Full Disk Access
        - [x] Terminal
        - [x] osascript

6. Starting from the command line !
    ```bash
    ~/evolving/evo -s

    ******************************************
    *** Evo !                              ***
    *** Trading through the command line ! ***
    ******************************************
    os, sys, time, datetime, np, pd, plt, show, Service, Evolving, EvolvingSim, Msg, Mail, Logging, Tlog were imported
    
    s = Service()
    e = Evolving()
    es = EvolvingSim()
    e.keepInformed = True

    In [1]: s.loginClient()
    Out[1]: True

    In [2]: e.loginBroker()
    Out[2]: True

    In [3]: 
    ...
	```
A brief **tutorial** can be found at [***wik***i](https://github.com/zetatez/evolving/wiki).

## For more information

- Hints:
    - You need to log in broker and bank account manually at least once.
    - If you want to use the email notification module, you need to register a 163 email account.
    - Technically, there is no restriction on brokers, but I didn't develop it all. If you don't find the broker you want, please contact me at zetatez@icloud.com.
        Or you can make a little change to the `asloginBroker` of the script [*ascmd.py*](https://github.com/zetatez/evolving/blob/main/evolving/ascmds.py) file and `python setup.py install` again.
        
        Up to now, The supported brokers are
        - <broker_code>ZXZQ</broker_code>       -- 中信证券
        - <broker_code>PAZQ</broker_code>       -- 平安证券
        - <broker_code>ZSZQ</broker_code>       -- 浙商证券					    
        - <broker_code>GTJA</broker_code>       -- 国泰君安
        - <broker_code>GJZQ</broker_code>       -- 国金证券
        - <broker_code>XYZQ</broker_code>       -- 兴业证券
        - <broker_code>ZJZQ</broker_code>       -- 中金证券
        - <broker_code>ZTZQ</broker_code>       -- 中泰证券

        Note: For different brokers, the display might be different. That is to say, the code might need to be slightly adjusted according to the different brokers.

- [PyPi](https://pypi.org/project/evolving/).

