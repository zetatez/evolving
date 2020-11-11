# Welcome to `evolving` !
This is a repo for the [`evolving`](https://github.com/zetatez/evolving) trading engine under the Mac OSX system.

<img src="http://latex.codecogs.com/gif.latex?S_T=S_0\int_Te^{r(t)}du"/>

## Author
[`evolving`](https://github.com/zetatez/evolving) © [Lorenzo](https://github.com/zetatez), Released under the [GPL 3.0](./LICENSE) License.

## Get in touch!

In order to get in touch with the author, join [Gitter](https://badges.gitter.im/zetatez-evolving/evolving.svg)

[![Gitter](https://badges.gitter.im/zetatez-evolving/evolving.svg)](https://gitter.im/zetatez-evolving/evolving?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge)

## How to contribute
To contribute in this repo, please open a [pull request](https://help.github.com/articles/using-pull-requests/#fork--pull) from your fork of this repo.

## Repo structure
    ```bash
    tree evolving
        evolving
        ├── LICENSE
        ├── README.md
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

## Installation guide
1. Requirements
    - python >= 3.8.5

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
    git clone git@github.com:zetatez/evolving.git ~/evolving; cd ~/evolving; python setup.py install; rm -rf ~/evolving
    ```

4. Configuration
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

## For more information
- Hint:
    - Technically, there is no restriction on securities companies, but I didn't develop it all. If you don't find the broker you want, please contact me at [email](zetatez@icloud.com).


- [wiki](https://github.com/zetatez/evolving/wiki)

From a technical point of view, there are no restrictions on securities companies





