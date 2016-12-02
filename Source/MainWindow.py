# coding=utf-8
from PyQt5 import uic, QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QCursor
from ui_main import Ui_Form
import i18n.Strings as Strings
import webbrowser

qtUIFile = "main.ui"


class MainWindow(QWidget, Ui_Form):
    def __init__(self, icon, is_pyui=False, stays_on_top=True):
        super().__init__()
        self.s = Strings.Strings()

        self.tomatoCount = 0
        self.isPyUI = is_pyui
        self.icon = icon

        self.version = '1.0.1'
        self.TrayText = '{0} v{1}\n'.format(self.s.strPomodoro, self.version)

        # Object Init
        if self.isPyUI:
            self.setupUi(self)
        else:
            uic.loadUi(qtUIFile, self)

        self.setWindowIcon(self.icon)
        self.trayIcon = None
        self.closeEnable = False
        self.setWindowTitle(self.s.strPomodoro)
        self.title = self.windowTitle()

        self.showAction = QAction(self.s.strShowWindow, self)
        self.showAction.triggered.connect(self.showWindow)
        self.hideAction = QAction(self.s.strHideWindow, self)
        self.hideAction.triggered.connect(self.hide)
        self.aboutAction = QAction(self.s.strAbout + '...', self)
        self.aboutAction.triggered.connect(lambda: webbrowser.open_new_tab('https://github.com/JalonWong/Pomodoro'))

        self.buttonMenu = QMenu()
        self.buttonMenu.addAction(self.s.strWork).triggered.connect(self.setWorkStatus)
        self.buttonMenu.addAction(self.s.strBreak).triggered.connect(self.setBreakStatus)
        self.buttonMenu.addAction(self.s.strLongBreak).triggered.connect(self.setLoneBreakStatus)
        self.buttonMenu.addAction(self.s.strDecreasePomodoro).triggered.connect(self.decreaseOneTomato)
        self.buttonMenu.addAction(self.aboutAction)
        self.buttonMenu.addSeparator()
        self.buttonMenu.addAction(self.s.strExit).triggered.connect(self.close)
        self.buttonMain.customContextMenuRequested.connect(lambda: self.buttonMenu.exec(QCursor.pos()))

        self.buildTray()

        if stays_on_top:
            flags = self.windowFlags() | QtCore.Qt.WindowStaysOnTopHint
            self.setWindowFlags(flags)

    def close(self):
        self.closeEnable = True
        return super().close()

    def closeEvent(self, QCloseEvent):
        if self.closeEnable:
            self.trayIcon.hide()
            super().closeEvent(QCloseEvent)
        else:
            QCloseEvent.ignore()
            self.hide()

    def buildTray(self):
        self.trayIcon = QSystemTrayIcon(self)
        self.trayIcon.setIcon(self.icon)
        self.trayIcon.setToolTip(self.TrayText)
        self.trayIcon.activated.connect(self.onTrayActivated)
        self.trayIcon.show()

        menu = QMenu()
        menu.addAction(self.showAction)
        menu.addAction(self.hideAction)
        menu.addAction(self.aboutAction)
        menu.addSeparator()
        menu.addAction(self.s.strExit).triggered.connect(self.close)
        self.trayIcon.setContextMenu(menu)

    def setTrayToolTipText(self, text):
        self.trayIcon.setToolTip(self.TrayText + text)

    def onTrayActivated(self, reason):
        if reason == QSystemTrayIcon.DoubleClick:
            self.showOrHideWindow()
        elif reason == QSystemTrayIcon.Context:
            enable = self.isHidden()
            self.showAction.setEnabled(enable)
            self.hideAction.setEnabled(not enable)

    def showOrHideWindow(self):
        if self.isHidden():
            self.showWindow()
        else:
            self.hide()

    def showWindow(self):
        if self.buttonMain.hasFocus():
            return
        elif not self.isHidden():
            self.showMinimized()
        self.showNormal()

    def keyPressEvent(self, QKeyEvent):
        key = QKeyEvent.key()
        if key == QtCore.Qt.Key_Escape:
            self.hide()
        elif key == QtCore.Qt.Key_Enter or key == QtCore.Qt.Key_Return:
            self.buttonMain.click()
        else:
            super().keyPressEvent(QKeyEvent)

    def workView(self, s):
        self.buttonMain.setText(s)
        self.buttonMain.setStyleSheet(
            'QPushButton{background:rgb(235, 97, 97);color:lightgrey}'
            'QPushButton:focus{background:rgb(235, 97, 97);color:black}'
            'QPushButton:hover{background:rgb(237, 114, 114)}'
            'QPushButton:pressed{background:rgb(234, 85, 85)}'
        )
        # self.buttonMain.setStyleSheet('background:rgb(218, 101, 101)')

    def breakView(self, s):
        self.buttonMain.setText(s)
        self.buttonMain.setStyleSheet(
            'QPushButton{background:rgb(0, 175, 108);color:lightgrey}'
            'QPushButton:focus{background:rgb(0, 175, 108);color:black}'
            'QPushButton:hover{background:rgb(0, 191, 120)}'
            'QPushButton:pressed{background:rgb(0, 159, 100)}'
        )
        # self.buttonMain.setStyleSheet('background:rgb(131, 218, 101)')

    def setCompleteTomato(self, count):
        self.setWindowTitle(self.title + ' - ' + self.tr('Complete') + ': {0}'.format(count))

    def viewTime(self, view_time):
        self.labelTime.setText('{0:02d}:{1:02d}'.format(int(view_time / 60), int(view_time % 60)))

    def decreaseOneTomato(self):
        if self.tomatoCount > 0:
            self.tomatoCount -= 1
            self.setCompleteTomato(self.tomatoCount)

    def setWorkStatus(self):
        pass

    def setBreakStatus(self):
        pass

    def setLoneBreakStatus(self):
        pass
