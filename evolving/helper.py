# -*- coding: utf-8 -*-

import re, os, sys, time, json
from datetime import datetime
import yaml
import logging
from logging import FileHandler
import requests
from pprint import pprint as show
import email
import smtplib
from email.header import Header
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart

BASE_DIR = os.path.expanduser('~')
CONFIG_PATH = os.path.join(BASE_DIR, '.config', 'evolving', 'config.yaml')


def _load_yaml_root():
    if not os.path.exists(CONFIG_PATH):
        raise FileNotFoundError("Missing configuration file: {}".format(CONFIG_PATH))
    with open(CONFIG_PATH, 'r', encoding='utf8') as fp:
        data = yaml.safe_load(fp) or {}
    if not isinstance(data, dict):
        raise ValueError("Configuration file must define a mapping at the top level")
    if 'evolving' in data and isinstance(data['evolving'], dict):
        return data['evolving']
    return data


def _load_yaml_section(section_name):
    root = _load_yaml_root()
    section = root.get(section_name, {}) if isinstance(root, dict) else {}
    if section is None:
        section = {}
    if not isinstance(section, dict):
        raise ValueError("Section '{}' must be a mapping".format(section_name))
    return section

class Config(object):
    def __init__(self):
        self.__config = self.__loadConfiguration()
        self.__userid = self.__config.get("userid", None)
        self.__password = self.__config.get("password", None)
        self.__broker_code = self.__config.get("broker_code", None)
        self.__broker_account = self.__config.get("broker_account", None)
        self.__broker_password = self.__config.get("broker_password", None)
        self.__bank_name = self.__config.get("bank_name", None)
        self.__bank_account = self.__config.get("bank_account", None)
        self.__bank_password = self.__config.get("bank_password", None)
        self.__comment = self.__config.get("comment", None)

    def __loadConfiguration(self):
        config = _load_yaml_section('trading')
        return dict(config)

    @property
    def config(self):
        return self.__config

    def __str__(self):
        return str(self.__config)

    @property
    def userid(self):
        return self.__userid

    @property
    def password(self):
        return self.__password

    @property
    def broker_code(self):
        return self.__broker_code

    @property
    def broker_account(self):
        return self.__broker_account

    @property
    def broker_password(self):
        return self.__broker_password

    @property
    def bank_name(self):
        return self.__bank_name

    @property
    def bank_account(self):
        return self.__bank_account

    @property
    def bank_password(self):
        return self.__bank_password

class MConfig(object):
    def __init__(self):
        self.__config = self.__loadConfiguration()
        self.__mail_host = self.__config.get("mail_host", None)
        self.__mail_sender = self.__config.get("mail_sender", None)
        self.__mail_license = self.__config.get("mail_license", None)
        self.__mail_receivers = self.__parse_receivers(self.__config.get("mail_receivers", None))

    def __parse_receivers(self, receivers):
        if receivers is None:
            return []
        if isinstance(receivers, str):
            return [rcp.strip() for rcp in receivers.split(';') if rcp.strip()]
        if isinstance(receivers, (list, tuple)):
            parsed = []
            for rcp in receivers:
                value = str(rcp).strip()
                if value:
                    parsed.append(value)
            return parsed
        raise ValueError("mail_receivers must be a string or list")

    def __loadConfiguration(self):
        config = _load_yaml_section('mail')
        return dict(config)

    @property
    def config(self):
        return self.__config

    def __str__(self):
        return str(self.__config)

    @property
    def mail_host(self):
        return self.__mail_host

    @property
    def mail_sender(self):
        return self.__mail_sender

    @property
    def mail_license(self):
        return self.__mail_license

    @property
    def mail_receivers(self):
        return self.__mail_receivers

class Msg(object):
    def __init__(self):
        self.subject = "subject"
        self.body = "body goes here"

class Mail(object):
    def __init__(self, msg):
        assert isinstance(msg, Msg)
        self.__mconfig = MConfig()
        self.mail_host = self.__mconfig.mail_host
        self.mail_sender = self.__mconfig.mail_sender
        self.mail_license = self.__mconfig.mail_license
        self.mail_receivers = self.__mconfig.mail_receivers
        self.stp = smtplib.SMTP()
        self.stp.connect(self.mail_host, 25)
        # self.stp.set_debuglevel(1)
        self.stp.ehlo()
        self.stp.login(self.mail_sender, self.mail_license)
        self.__compose(msg)
        self.stp.sendmail(self.mail_sender, self.mail_receivers, self.mail.as_string())
        self.stp.quit()

    def __compose(self, msg):
        self.mail = MIMEMultipart()
        self.mail["From"] = "zero<" + self.mail_sender + ">"
        self.mail["To"] = ''.join([y.split("@")[0] + "<" + y + ">;" for y in self.mail_receivers])
        self.mail["Subject"] = Header(msg.subject, 'utf-8')
        self.mail.attach(MIMEText(msg.body, "plain", "utf-8"))


class Tlog(Msg):
    def __init__(self, action='', assetsName='', assetsCode='', price='', amount='', status='', comments=''):
        """ transaction msg for email
        Args:
            action:     # entrust buy, entrust sell, buy, sell, revoke, transferBroker2Bank, transferBank2Broker
            assets:     # stock, sciTech, gem
            assetsCode:
            price:
            amount:
            status:     # successed, failed,
            comments:
        """
        self.__timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.__time = self.__timestamp.split()[1]
        self.__date = time.strftime("%m-%d", time.localtime())
        self.__action = action
        self.__assetsName = assetsName
        self.__assetsCode = assetsCode
        self.__price = price
        self.__amount = amount
        self.__status = status
        self.__comments = comments
        self.subject = self.__subject()
        self.body = self.__str__()
        self.str = self.__str__()

    def __str__(self):
        strvar = str(self.__action) + " " + str(self.__assetsName) + " " + str(self.__assetsCode) + " " + str(self.__price) + " " + str(self.__amount) + " " + str(self.__status) + " " + str(self.__comments)
        strvar = re.sub(' +', ' ', strvar)
        return strvar

    def __subject(self):
        strvar = "! " + time.strftime("%H:%M:%S %d-%m", time.localtime()) + " " + str(self.__action) + " " + str(self.__status)
        strvar = re.sub(' +', ' ', strvar)
        return strvar

class Logging(logging.Logger):
    def __init__(self, logType='service'):
        super(Logging, self).__init__(self)
        self.__logType = logType
        self.setLevel('DEBUG')
        self.__setFileHandler()

    def __setFileHandler(self):
        path = os.path.join(BASE_DIR, 'logs/evolving/', self.__logType)
        if not os.path.exists(path):
            os.makedirs(path)
        logFilePath = os.path.join(path, datetime.now().date().strftime('%Y-%m-%d.log'))
        fh = FileHandler(logFilePath)
        fh.setFormatter(logging.Formatter('%(asctime)s %(levelname)s %(message)s'))
        self.addHandler(fh)

if __name__ == "__main__":
    # --- Config
    config = Config()
    print(config.config)
    print(config.userid)

    # --- MConfig
    config = MConfig()
    print(config.config)
    print(config.mail_sender)

    # --- Msg
    msg = Msg()
    mail = Mail(msg)

    # --- Logging
    lg = Logging(logType='prod_env')
    lg.info("this is a info")
    lg.debug("this is a debug")
    lg.warning("this is a warning")
    lg.error("this is a error")
    lg.critical('this is a critical')

    lg = Logging(logType='simu_env')
    lg.info("this is a info")
    lg.debug("this is a debug")
    lg.warning("this is a warning")
    lg.error("this is a error")
    lg.critical('this is a critical')

    # --- Tlog
    tlog = Tlog(action='entrust buy', assetsName='stock', assetsCode='000000', price='45.93', amount='1000', status='successed', comments='')
    mail = Mail(tlog)
    print(tlog)
