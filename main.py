#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/7/27 14:41
# @Author  : YiWen
# @File    : main.py
# @software: PyCharm

import sys
import ctypes
from src.moduels.login import Login
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QIcon

if __name__ == '__main__':
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("myappid")
    app = QApplication(sys.argv)

    win = Login()
    win.setWindowIcon(QIcon("logo.png"))
    win.show()

    sys.exit(app.exec_())
