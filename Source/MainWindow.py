# coding=utf-8
from PyQt5 import uic, QtCore
from PyQt5.QtWidgets import *
from ui_main import *

qtUIFile = "main.ui"


class MainWindow(QWidget, Ui_Form):
    def __init__(self, icon, is_pyui=False):
        super().__init__()
        self.status = ''
        self.lastStatue = ''

        self.tomatoCount = 0
        self.isPyUI = is_pyui
        self.icon = icon

        # Object Init
        if self.isPyUI:
            self.setupUi(self)
        else:
            uic.loadUi(qtUIFile, self)

        self.setWindowIcon(self.icon)
        self.trayIcon = None
        self.closeEnable = False
        self.setWindowTitle(self.tr('Pomodoro'))
        self.title = self.windowTitle()

        self.buttonMenu = QMenu()
        self.buttonMenu.addAction(self.tr('Work')).triggered.connect(self.setWorkStatus)
        self.buttonMenu.addAction(self.tr('Break')).triggered.connect(self.setBreakStatus)
        self.buttonMenu.addAction(self.tr('Long Break')).triggered.connect(self.setLoneBreakStatus)
        self.buttonMenu.addAction(self.tr('Decrease a Pomodoro')).triggered.connect(self.decreaseOneTomato)
        self.buttonMenu.addSeparator()
        self.buttonMenu.addAction(self.tr('Exit')).triggered.connect(self.close)

        self.showAction = QAction(self.tr('Show Window'), self)
        self.showAction.triggered.connect(self.showWindow)
        self.hideAction = QAction(self.tr('Hide Window'), self)
        self.hideAction.triggered.connect(self.hide)
        self.buildTray()

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
        self.trayIcon.setToolTip('Pomodoro')
        self.trayIcon.activated.connect(self.onTrayActivated)
        self.trayIcon.show()

        menu = QMenu()
        menu.addAction(self.showAction)
        menu.addAction(self.hideAction)
        menu.addSeparator()
        menu.addAction(self.tr('Exit')).triggered.connect(self.close)
        self.trayIcon.setContextMenu(menu)

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
        # mainWindow.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.show()
        self.setWindowState(QtCore.Qt.WindowActive)
        self.activateWindow()
        self.buttonMain.setFocus()

    def keyPressEvent(self, QKeyEvent):
        if QKeyEvent.key() == QtCore.Qt.Key_Escape:
            self.hide()
        else:
            super().keyPressEvent(QKeyEvent)

    def workView(self, s):
        self.buttonMain.setText(s)
        self.buttonMain.setStyleSheet('background:rgb(235, 97, 97)')
        # self.buttonMain.setStyleSheet('background:rgb(218, 101, 101)')

    def breakView(self, s):
        self.buttonMain.setText(s)
        self.buttonMain.setStyleSheet('background:rgb(0, 175, 108)')
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
