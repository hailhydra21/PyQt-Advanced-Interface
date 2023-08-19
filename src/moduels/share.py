#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/7/27 15:09
# @Author  : YiWen
# @File    : share.py
# @software: PyCharm

from enum import Enum

import os


def get_project_rootpath():
    # 获取项目根目录
    path = os.path.realpath(os.curdir)
    last = None
    while True:
        # PyCharm项目中，'.idea'是必然存在的，且名称唯一
        if '.idea' in os.listdir(path):
            return path
        last = path
        # 去掉文件名
        path = os.path.dirname(path)
        if last == path:
            # 没有.idea说明运行的是exe，返回exe所在目录
            return os.getcwd()


class ActionFlag(Enum):
    initial = 0
    win_close = 1
    win_switch = 2


class GlobalStatic:
    QSS_FILE_DIR = ':/QSS/'
    IMAGES_FILE_DIR = ':/Images/'
    PROJECT_DIR = None

    TEST_LOGIN_ACCOUNT = 'qwer'
    TEST_LOGIN_PASSWORD = '123'
    TEST_REGISTER_ACCOUNT = 'asd'
    TEST_REGISTER_PASSWORD = '111'


GlobalStatic.PROJECT_DIR = get_project_rootpath()

if __name__ == '__main__':
    pass
