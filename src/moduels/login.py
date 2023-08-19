# -*- coding:utf-8 -*-
"""
作者：YiWen
日期：2021年04月12日
"""

from src.moduels.share import *
from src.ui.login_form import Ui_Login
from src.moduels.app_config import AppConfig

from PyQt5.QtWidgets import QWidget, QLineEdit, QGraphicsOpacityEffect, QAction, QApplication, QMessageBox
from PyQt5.QtCore import QEasingCurve, Qt, QRegExp, QPropertyAnimation, QEasingCurve, QSequentialAnimationGroup, QFile
from PyQt5.QtGui import QPixmap, QRegExpValidator, QMouseEvent, QKeyEvent, QPainter, QColor, QIcon

import sys
import src.resources.Images_rc
import src.resources.QSS_rc


class Login(QWidget):
    def __init__(self):
        super(Login, self).__init__()

        self._register_account_input_state = False
        self._drag_position = None
        self.valueAnimation = 1
        self.background_image = QPixmap(GlobalStatic.IMAGES_FILE_DIR + 'login_background.png')

        self._app_config = AppConfig()

        self._init()

    def _init(self):
        self.ui = Ui_Login()
        self.ui.setupUi(self)
        self.setWindowTitle("PyQt-Advanced-Interface")

        # 无边框
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Dialog)
        self.setAttribute(Qt.WA_TranslucentBackground)

        # 信号与槽自动连接
        # QMetaObject.connectSlotsByName(self)

        # 设置窗体样式
        style_file = QFile(GlobalStatic.QSS_FILE_DIR + "login_form.qss")
        style_file.open(QFile.ReadOnly)
        style_sheet = style_file.readAll()
        self.setStyleSheet(str(style_sheet, "UTF-8"))

        # 设置箭头提示
        self.ui.toolButtonArrow1.setToolTip('<font style="font: bold;color:#838894;font-family: Bauhaus">switch</font>')
        self.ui.toolButtonArrow2.setToolTip('<font style="font: bold;color:#838894;font-family: Bauhaus">submit</font>')
        self.ui.toolButtonArrow3.setToolTip('<font style="font: bold;color:#838894;font-family: Bauhaus">switch</font>')

        # 设置输入框属性
        self.ui.labelCentralInfo.setText('LOG INTO <font style="font: bold;color:#838894">SYSTEM</font>')
        self.ui.labelCentralInfo.setWordWrap(True)
        self.ui.lineEditAccount.setPlaceholderText('Account...')
        self.ui.lineEditPassword.setPlaceholderText('Password...')
        self.ui.lineEditPassword.setEchoMode(QLineEdit.Password)

        self.ui.labelCentralInfo2.setText('<font style="font: bold;color:#838894">REGISTER</font> YOUR ACCOUNT')
        self.ui.labelCentralInfo2.setWordWrap(True)
        self.ui.lineEditRegisterAccount.setPlaceholderText('Account')
        self.ui.lineEditRegisterPassword.setPlaceholderText('Password...')
        self.ui.lineEditRegisterPasswordConfirm.setPlaceholderText('Password Again...')
        self.ui.lineEditRegisterPassword.setEchoMode(QLineEdit.Password)
        self.ui.lineEditRegisterPasswordConfirm.setEchoMode(QLineEdit.Password)

        # 禁止输入汉字
        re_account = QRegExp(r'^[a-zA-z0-9]+$')
        validator_account = QRegExpValidator(self)
        validator_account.setRegExp(re_account)

        re_password = QRegExp(r'^[A-Za-z0-9`~!@#$%^&*()_-+=<>,.\\\/]+$')
        validator_password = QRegExpValidator(self)
        validator_password.setRegExp(re_password)

        # 设置验证器
        self.ui.lineEditAccount.setValidator(validator_account)
        self.ui.lineEditRegisterAccount.setValidator(validator_account)
        self.ui.lineEditPassword.setValidator(validator_password)
        self.ui.lineEditRegisterPassword.setValidator(validator_password)
        self.ui.lineEditRegisterPasswordConfirm.setValidator(validator_password)

        # 启用亚洲语言的输入法。创建自定义文本编辑小部件时必须设置
        self.ui.lineEditAccount.setAttribute(Qt.WA_InputMethodEnabled, False)
        self.ui.lineEditRegisterAccount.setAttribute(Qt.WA_InputMethodEnabled, False)
        self.ui.lineEditPassword.setAttribute(Qt.WA_InputMethodEnabled, False)
        self.ui.lineEditRegisterPassword.setAttribute(Qt.WA_InputMethodEnabled, False)
        self.ui.lineEditRegisterPasswordConfirm.setAttribute(Qt.WA_InputMethodEnabled, False)

        # 登录，注册小部件的淡入，淡出动画
        self.opacityEffectLogin = QGraphicsOpacityEffect(self.ui.widgetLogin)
        self.opacityEffectLogin.setOpacity(1)
        self.ui.widgetLogin.setGraphicsEffect(self.opacityEffectLogin)

        self.opacityEffectRegister = QGraphicsOpacityEffect(self.ui.widgetRegister)
        self.opacityEffectRegister.setOpacity(0)
        self.ui.widgetRegister.setGraphicsEffect(self.opacityEffectRegister)

        self.animationLoginFade = QPropertyAnimation(self.opacityEffectLogin, b"opacity", self)
        self.animationLoginFade.setEasingCurve(QEasingCurve.Linear)
        self.animationLoginFade.setDuration(500)

        self.animationRegisterFade = QPropertyAnimation(self.opacityEffectRegister, b"opacity", self)
        self.animationRegisterFade.setEasingCurve(QEasingCurve.Linear)
        self.animationRegisterFade.setDuration(500)

        # 主窗口淡入，淡出动画
        self.animationFadeOut = QPropertyAnimation(self, b"windowOpacity")
        self.animationGroup = QSequentialAnimationGroup()

        self._create_connect()

        self.ui.widgetRegister.move(50, 320)

        # 提升，置于顶层
        self.ui.widgetLogin.raise_()
        # self.ui.widgetRegister.hide()

    # 连接信号与槽
    def _create_connect(self):
        self.ui.toolButtonExit.clicked.connect(self._clicked_exit)

        self.ui.toolButtonArrow1.clicked.connect(self._switch)
        self.ui.toolButtonArrow2.clicked.connect(self._submit)
        self.ui.toolButtonArrow3.clicked.connect(self._switch)

        self.ui.lineEditAccount.textChanged.connect(self._data_check)
        self.ui.lineEditRegisterAccount.textChanged.connect(self._data_check)
        self.ui.lineEditRegisterPasswordConfirm.textChanged.connect(self._data_check)
        self.ui.lineEditRegisterPassword.textChanged.connect(self._data_check)

        self.actionLineEditAccount = QAction(self)
        self.actionLineEditRegisterAccount = QAction(self)
        self.ui.lineEditAccount.addAction(self.actionLineEditAccount, QLineEdit.TrailingPosition)
        self.ui.lineEditRegisterAccount.addAction(self.actionLineEditRegisterAccount, QLineEdit.TrailingPosition)

        self.animationFadeOut.finished.connect(self._handle_action_flag)

    def _handle_action_flag(self):
        if self._action_flag == ActionFlag.win_close:
            self.close()
        elif self._action_flag == ActionFlag.win_switch:
            # self.signalSwitchTOMainWin.emit()
            # self._mainwin.show()
            # self.hide()
            pass

    def _clicked_exit(self):
        self._action_flag = ActionFlag.win_close
        self._fade_out(1000)

    def _back_login(self):
        self._fade_in()
        self._action_flag = ActionFlag.initial
        self.show()

        # self._mainwin.hide()

    def _switch(self):

        if self.valueAnimation:
            self.animationGroup.addAnimation(self.animationLoginFade)
            self.animationGroup.addAnimation(self.animationRegisterFade)
            self.ui.widgetRegister.raise_()

            self.ui.toolButtonArrow1.setStyleSheet("QToolButton#toolButtonArrow1{border-image:"
                                                   "url(:/Images/Arrow1return.png);}"
                                                   "QToolButton#toolButtonArrow1:hover{"
                                                   "border-image:url(:/Images/Arrow1return.png)2 2 2 2;}"
                                                   "QToolButton#toolButtonArrow1::pressed{"
                                                   "border-image:url(:/Images/Arrow1return.png)1 4 2 1;}")

            self.ui.toolButtonArrow3.setStyleSheet("QToolButton#toolButtonArrow3{border-image:"
                                                   "url(:/Images/Arrow3return.png);}"
                                                   "QToolButton#toolButtonArrow3:hover{"
                                                   "border-image:url(:/Images/Arrow3return.png)2 2 2 2;}"
                                                   "QToolButton#toolButtonArrow3::pressed{"
                                                   "border-image:url(:/Images/Arrow3return.png)1 4 2 1;}")

        else:
            self.animationGroup.addAnimation(self.animationRegisterFade)
            self.animationGroup.addAnimation(self.animationLoginFade)
            self.ui.widgetLogin.raise_()

            self.ui.toolButtonArrow1.setStyleSheet("QToolButton#toolButtonArrow1{border-image:"
                                                   "url(:/Images/Arrow1.png);}"
                                                   "QToolButton#toolButtonArrow1:hover{"
                                                   "border-image:url(:/Images/Arrow1.png)2 2 2 2;}"
                                                   "QToolButton#toolButtonArrow1::pressed{"
                                                   "border-image:url(:/Images/Arrow1.png)1 4 2 1;}")

            self.ui.toolButtonArrow3.setStyleSheet("QToolButton#toolButtonArrow3{border-image:"
                                                   "url(:/Images/Arrow3.png);}"
                                                   "QToolButton#toolButtonArrow3:hover{"
                                                   "border-image:url(:/Images/Arrow3.png)2 2 2 2;}"
                                                   "QToolButton#toolButtonArrow3::pressed{"
                                                   "border-image:url(:/Images/Arrow3.png)1 4 2 1;}")

        self.animationLoginFade.setStartValue(self.valueAnimation)
        self.animationLoginFade.setEndValue(int(not self.valueAnimation))
        # self.animationLoginFade.start(QAbstractAnimation.KeepWhenStopped)

        self.animationRegisterFade.setStartValue(int(not self.valueAnimation))
        self.animationRegisterFade.setEndValue(self.valueAnimation)

        self.animationGroup.start()
        self.valueAnimation = int(not self.valueAnimation)

    def _fade_out(self, millisecond):
        self.animationFadeOut.setDuration(millisecond)
        self.animationFadeOut.setStartValue(1)
        self.animationFadeOut.setEndValue(0)
        self.animationFadeOut.start()

    def _fade_in(self):
        self.animationFadeOut.setDuration(1000)
        self.animationFadeOut.setStartValue(0)
        self.animationFadeOut.setEndValue(1)
        self.animationFadeOut.start()

    def _data_check(self, text):
        if self.sender().objectName() == self.ui.lineEditRegisterPassword.objectName():
            if text != self.ui.lineEditRegisterPasswordConfirm.text():
                stylesheet = "color: salmon;"
                self.ui.lineEditRegisterPasswordConfirm.setStyleSheet(stylesheet)
            else:
                stylesheet = "color: #404244;"
                self.ui.lineEditRegisterPasswordConfirm.setStyleSheet(stylesheet)

        elif self.sender().objectName() == self.ui.lineEditRegisterPasswordConfirm.objectName():
            if text != self.ui.lineEditRegisterPassword.text():
                stylesheet = "color: salmon;"
                self.ui.lineEditRegisterPasswordConfirm.setStyleSheet(stylesheet)
            else:
                stylesheet = "color: #404244;"
                self.ui.lineEditRegisterPasswordConfirm.setStyleSheet(stylesheet)
        else:
            if self.sender().objectName() == self.ui.lineEditAccount.objectName():
                result = GlobalStatic.TEST_LOGIN_ACCOUNT
                if len(text) == 0:
                    self.actionLineEditAccount.setIcon(QIcon(GlobalStatic.IMAGES_FILE_DIR + 'exclamatory.png'))
                elif len(result) == 0:
                    self.actionLineEditAccount.setIcon(QIcon(GlobalStatic.IMAGES_FILE_DIR + 'exclamatory.png'))
                else:
                    self.actionLineEditAccount.setIcon(QIcon(GlobalStatic.IMAGES_FILE_DIR + 'hook.png'))
            elif self.sender().objectName() == self.ui.lineEditRegisterAccount.objectName():
                result = GlobalStatic.TEST_REGISTER_ACCOUNT
                if len(text) == 0 or len(text) < 3:
                    self.actionLineEditRegisterAccount.setIcon(QIcon(GlobalStatic.IMAGES_FILE_DIR + 'exclamatory.png'))
                    self._register_account_input_state = False
                elif text != result:
                    self.actionLineEditRegisterAccount.setIcon(QIcon(GlobalStatic.IMAGES_FILE_DIR + 'hook.png'))
                    self._register_account_input_state = True
                else:
                    self.actionLineEditRegisterAccount.setIcon(QIcon(GlobalStatic.IMAGES_FILE_DIR + 'exclamatory.png'))
                    self._register_account_input_state = False

    def _submit(self):
        self._action_flag = ActionFlag.win_switch
        if self.valueAnimation:
            account = self.ui.lineEditAccount.text()
            password = self.ui.lineEditPassword.text()
            if len(account) == 0:
                self._widget_shake(self.ui.lineEditAccount)
            elif len(password) == 0:
                self._widget_shake(self.ui.lineEditPassword)
            else:
                result = GlobalStatic.TEST_LOGIN_PASSWORD
                if len(result) == 0:
                    return
                if password == result and account == GlobalStatic.TEST_LOGIN_ACCOUNT:
                    QMessageBox.information(self, '消息提示', '登录成功', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                    # self._fade_out(700)
                    # self.ui.lineEditPassword.clear()
                    pass
                else:
                    QMessageBox.warning(self, '消息提示', '密码错误', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        else:
            account = self.ui.lineEditRegisterAccount.text()
            password = self.ui.lineEditRegisterPassword.text()
            password_confirm = self.ui.lineEditRegisterPasswordConfirm.text()
            if len(account) == 0 and len(account) < 3 or not self._register_account_input_state:
                self._widget_shake(self.ui.lineEditRegisterAccount)
            elif len(password) == 0:
                self._widget_shake(self.ui.lineEditRegisterPassword)
            elif len(password_confirm) == 0 or password != password_confirm:
                self._widget_shake(self.ui.lineEditRegisterPasswordConfirm)
            else:
                GlobalStatic.TEST_REGISTER_ACCOUNT = account
                GlobalStatic.TEST_REGISTER_PASSWORD = password
                self._app_config.config_write()
                QMessageBox.information(self, '消息提示', '注册成功', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                # self._fade_out(700)
                #
                # self.ui.lineEditRegisterPasswordConfirm.clear()
                # self.ui.lineEditRegisterPassword.clear()
                pass

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.fillRect(self.rect(), QColor(0, 0, 255, 0))
        painter.drawPixmap(self.rect(), self.background_image)

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            self._drag_position = event.globalPos() - self.frameGeometry().topLeft()

    def mouseMoveEvent(self, event):
        if self.ui.toolButtonArrow1.underMouse() \
                or self.ui.toolButtonArrow2.underMouse() \
                or self.ui.toolButtonArrow3.underMouse():
            return
        if event.buttons() == Qt.LeftButton:
            self.move(event.globalPos() - self._drag_position)

    def keyPressEvent(self, event: QKeyEvent):
        if event.key() == Qt.Key_Escape:
            self._clicked_exit()
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self._submit()

    # 小部件抖动
    def _widget_shake(self, widget):
        self.animation = QPropertyAnimation(widget, b'pos')
        self.animation.setEasingCurve(QEasingCurve.OutElastic)

        origin_pos = widget.pos()
        pos = widget.pos()
        pos.setX(pos.x() + 25)

        self.animation.setStartValue(pos)
        self.animation.setEndValue(origin_pos)

        self.animation.setDuration(500)
        self.animation.start()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = Login()

    win.show()
    sys.exit(app.exec_())
