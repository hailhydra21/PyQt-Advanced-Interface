#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/5/10 11:26
# @Author  : YiWen
# @File    : app_config.py
# @software: PyCharm

from src.moduels.share import *

import configparser
import atexit
import os


class AppConfig:
    def __init__(self):
        super(AppConfig, self).__init__()

        atexit.register(self._delete)
        self.config = configparser.ConfigParser()

        self._init()

    def _init(self):
        self._config_file = GlobalStatic.PROJECT_DIR + '/config.ini'
        if os.path.exists(self._config_file):
            self.config_read()
        else:
            self.config.add_section("Test")
            self.config_write()

    # 代理析构
    def _delete(self):
        self.config_write()

    def config_read(self):
        self.config.read(self._config_file)
        GlobalStatic.TEST_LOGIN_ACCOUNT = self.config.get("Test", "TEST_LOGIN_ACCOUNT")
        GlobalStatic.TEST_LOGIN_PASSWORD = self.config.get("Test", "TEST_LOGIN_PASSWORD")
        GlobalStatic.TEST_REGISTER_ACCOUNT = self.config.get("Test", "TEST_REGISTER_ACCOUNT")
        GlobalStatic.TEST_REGISTER_PASSWORD = self.config.get("Test", "TEST_REGISTER_PASSWORD")

    def config_write(self):
        self.config.set("Test", "TEST_LOGIN_ACCOUNT", GlobalStatic.TEST_LOGIN_ACCOUNT)
        self.config.set("Test", "TEST_LOGIN_PASSWORD", GlobalStatic.TEST_LOGIN_PASSWORD)
        self.config.set("Test", "TEST_REGISTER_ACCOUNT", GlobalStatic.TEST_REGISTER_ACCOUNT)
        self.config.set("Test", "TEST_REGISTER_PASSWORD", GlobalStatic.TEST_REGISTER_PASSWORD)
        self.config.write(open(self._config_file, 'w'))


if __name__ == '__main__':
    pass
