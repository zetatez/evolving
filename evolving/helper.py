# -*- coding: utf-8 -*-

from __future__ import annotations
import re
import os
import time
from datetime import datetime
from dataclasses import dataclass, field
from typing import Optional
import yaml
import logging
from logging import FileHandler
import smtplib
from email.header import Header
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

BASE_DIR = os.path.expanduser('~')
CONFIG_PATH = os.path.join(BASE_DIR, '.config', 'evolving', 'config.yaml')

_smtp_connection: Optional[smtplib.SMTP] = None


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


def _load_yaml_section(section_name: str) -> dict:
    root = _load_yaml_root()
    section = root.get(section_name, {}) if isinstance(root, dict) else {}
    if section is None:
        section = {}
    if not isinstance(section, dict):
        raise ValueError("Section '{}' must be a mapping".format(section_name))
    return section


@dataclass
class Config:
    userid: str = ""
    password: str = ""
    broker_code: str = ""
    broker_account: str = ""
    broker_password: str = ""
    bank_name: str = ""
    bank_account: str = ""
    bank_password: str = ""
    comment: str = ""
    _config: dict = field(default_factory=dict, repr=False)

    def __post_init__(self):
        config = _load_yaml_section('trading')
        self._config = dict(config)
        self.userid = config.get("userid") or ""
        self.password = config.get("password") or ""
        self.broker_code = config.get("broker_code") or ""
        self.broker_account = config.get("broker_account") or ""
        self.broker_password = config.get("broker_password") or ""
        self.bank_name = config.get("bank_name") or ""
        self.bank_account = config.get("bank_account") or ""
        self.bank_password = config.get("bank_password") or ""
        self.comment = config.get("comment") or ""

    @property
    def config(self) -> dict:
        return self._config


@dataclass
class MConfig:
    mail_host: str = ""
    mail_sender: str = ""
    mail_license: str = ""
    mail_receivers: list[str] = field(default_factory=list)
    _config: dict = field(default_factory=dict, repr=False)

    def __post_init__(self):
        config = _load_yaml_section('mail')
        self._config = dict(config)
        self.mail_host = config.get("mail_host") or ""
        self.mail_sender = config.get("mail_sender") or ""
        self.mail_license = config.get("mail_license") or ""
        self.mail_receivers = self._parse_receivers(config.get("mail_receivers"))

    @staticmethod
    def _parse_receivers(receivers) -> list[str]:
        if receivers is None:
            return []
        if isinstance(receivers, str):
            return [rcp.strip() for rcp in receivers.split(';') if rcp.strip()]
        if isinstance(receivers, (list, tuple)):
            return [str(rcp).strip() for rcp in receivers if str(rcp).strip()]
        raise ValueError("mail_receivers must be a string or list")

    @property
    def config(self) -> dict:
        return self._config


class Msg:
    def __init__(self):
        self.subject: str = "subject"
        self.body: str = "body goes here"


class Mail:
    def __init__(self, msg: Msg):
        assert isinstance(msg, Msg)
        self._mconfig = MConfig()
        self.mail_host = self._mconfig.mail_host
        self.mail_sender = self._mconfig.mail_sender
        self.mail_license = self._mconfig.mail_license
        self.mail_receivers = self._mconfig.mail_receivers
        self._validate_config()
        self._connect_and_send(msg)

    def _validate_config(self):
        missing = []
        for field_name, field_value in (("mail_host", self.mail_host), ("mail_sender", self.mail_sender), ("mail_license", self.mail_license)):
            if not field_value:
                missing.append(field_name)
        if not self.mail_receivers:
            missing.append("mail_receivers")
        if missing:
            raise ValueError("Mail configuration missing required fields: " + ', '.join(missing))

    def _connect_and_send(self, msg: Msg):
        global _smtp_connection
        try:
            if _smtp_connection is None:
                _smtp_connection = smtplib.SMTP()
                _smtp_connection.connect(self.mail_host, 25)
                _smtp_connection.ehlo()
                _smtp_connection.login(self.mail_sender, self.mail_license)

            self._compose(msg)
            _smtp_connection.sendmail(self.mail_sender, self.mail_receivers, self.mail.as_string())
        except Exception:
            raise

    def _compose(self, msg: Msg):
        self.mail = MIMEMultipart()
        self.mail["From"] = f"zero<{self.mail_sender}>"
        self.mail["To"] = ''.join([y.split("@")[0] + "<" + y + ">;" for y in self.mail_receivers])
        self.mail["Subject"] = str(Header(msg.subject, 'utf-8'))
        self.mail.attach(MIMEText(msg.body, "plain", "utf-8"))


class Tlog(Msg):
    def __init__(
        self,
        action: str = '',
        assetsName: str = '',
        assetsCode: str = '',
        price: str = '',
        amount: str = '',
        status: str = '',
        comments: str = ''
    ):
        self._timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self._action = action
        self._assetsName = assetsName
        self._assetsCode = assetsCode
        self._price = price
        self._amount = amount
        self._status = status
        self._comments = comments
        self.subject = self._subject()
        self.body = self.__str__()
        self.str = self.__str__()

    def __str__(self) -> str:
        strvar = f"{self._action} {self._assetsName} {self._assetsCode} {self._price} {self._amount} {self._status} {self._comments}"
        strvar = re.sub(' +', ' ', strvar)
        return strvar

    def _subject(self) -> str:
        strvar = f"! {time.strftime('%H:%M:%S %d-%m', time.localtime())} {self._action} {self._status}"
        strvar = re.sub(' +', ' ', strvar)
        return strvar


class Logging(logging.Logger):
    def __init__(self, logType: str = 'service'):
        super(Logging, self).__init__("evolving")
        self._logType = logType
        self.setLevel('DEBUG')
        self._setFileHandler()

    def _setFileHandler(self):
        path = os.path.join(BASE_DIR, 'logs/evolving/', self._logType)
        if not os.path.exists(path):
            os.makedirs(path)
        logFilePath = os.path.join(path, datetime.now().date().strftime('%Y-%m-%d.log'))
        fh = FileHandler(logFilePath)
        fh.setFormatter(logging.Formatter('%(asctime)s %(levelname)s %(message)s'))
        self.addHandler(fh)


def close_smtp_connection():
    global _smtp_connection
    if _smtp_connection is not None:
        try:
            _smtp_connection.quit()
        except Exception:
            pass
        _smtp_connection = None


if __name__ == "__main__":
    config = Config()
    print(config.config)
    print(config.userid)

    mconfig = MConfig()
    print(mconfig.config)
    print(mconfig.mail_sender)

    msg = Msg()
    mail = Mail(msg)

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

    tlog = Tlog(action='entrust buy', assetsName='stock', assetsCode='000000', price='45.93', amount='1000', status='successed', comments='')
    mail = Mail(tlog)
    print(tlog)

    close_smtp_connection()
