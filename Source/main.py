# coding=utf-8
import sys
import platform
import threading
import time
from PyQt5 import uic, QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QCursor, QIcon
from PyQt5.QtCore import QLocale, QTranslator
import ctypes

if platform.system() == 'Windows':
    myAppId = 'jalon.tomato'  # arbitrary string
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myAppId)

mainWindow = None

qtUIFile = "main.ui"


class MainWindow(QWidget):
    closed = QtCore.pyqtSignal()

    def __init__(self):
        super(self.__class__, self).__init__()
        # Data Init
        self.workTime = 25 * 60
        self.shortTime = 5 * 60
        self.longTime = 15 * 60
        # self.workTime = 3
        # self.shortTime = 3
        # self.longTime = 3
        self.longBreakTomatoNumber = 4

        self.status = ''
        self.lastStatue = ''
        self.timer = None
        self.tomatoCount = 0
        self.nextTime = 0

        # Object Init
        uic.loadUi(qtUIFile, self)
        self.trayIcon = None
        self.closeEnable = False
        self.title = self.windowTitle()

        self.buttonMenu = QMenu()
        self.buttonMenu.addAction(self.tr('Work')).triggered.connect(self.setWorkStatus)
        self.buttonMenu.addAction(self.tr('Break')).triggered.connect(self.setBreakStatus)
        self.buttonMenu.addAction(self.tr('Long Break')).triggered.connect(self.setLoneBreakStatus)
        self.buttonMenu.addAction(self.tr('Decrease a Pomodoro')).triggered.connect(self.decreaseOneTomato)
        self.buttonMenu.addSeparator()
        self.buttonMenu.addAction(self.tr('Exit')).triggered.connect(self.close)

        self.buttonMain.customContextMenuRequested.connect(self.menuRequested)
        self.buttonMain.clicked.connect(self.mainClicked)

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
            if self.timer:
                self.timer.stop()
                self.timer.join()
            print('exit')
        else:
            QCloseEvent.ignore()
            self.hide()

    def buildTray(self):
        self.trayIcon = QSystemTrayIcon(self)
        self.trayIcon.setIcon(QIcon('resource/tomato.ico'))
        self.trayIcon.setToolTip('Tomato')
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

    def menuRequested(self):
        if self.status != 'Run':
            self.buttonMenu.exec(QCursor.pos())

    def mainClicked(self):
        if self.status != 'Run':
            if self.status == 'ReadyToWork':
                self.hide()
            self.setStatus('Run')
        else:
            self.setStatus(self.lastStatue)

    def timeout(self):
        print('timeout')
        self.timer = None
        if self.lastStatue != 'ReadyToWork':
            self.setStatus('ReadyToWork')
        else:
            self.tomatoCount += 1
            self.setCompleteTomato(self.tomatoCount)
            if self.tomatoCount % self.longBreakTomatoNumber == 0:
                self.setStatus('ReadyToLoneBreak')
            else:
                self.setStatus('ReadyToShortBreak')

        self.showWindow()

    def decreaseOneTomato(self):
        if self.tomatoCount > 0:
            self.tomatoCount -= 1
            self.setCompleteTomato(self.tomatoCount)

    # 状态管理
    def setStatus(self, state):
        self.lastStatue = self.status
        self.status = state
        if state == 'Run':
            self.buttonMain.setText(self.tr('Reset'))
            self.timer = ThreadTimer(full_time=self.nextTime, timeoutCallBack=self.timeout)
            self.timer.start()
            return
        elif state == 'ReadyToWork':
            self.workView(self.tr('Work'))
            if self.timer:
                self.timer.stop()
                self.timer.join()
                self.timer = None

            self.nextTime = self.workTime
        elif state == 'ReadyToShortBreak':
            self.breakView(self.tr('Break'))
            if self.timer:
                self.timer.stop()
                self.timer.join()
                self.timer = None

            self.nextTime = self.shortTime
        elif state == 'ReadyToLoneBreak':
            self.breakView(self.tr('Long Break'))
            if self.timer:
                self.timer.stop()
                self.timer.join()
                self.timer = None

            self.nextTime = self.longTime

        self.viewTime(self.nextTime)

    def setWorkStatus(self):
        self.setStatus('ReadyToWork')

    def setBreakStatus(self):
        self.setStatus('ReadyToShortBreak')

    def setLoneBreakStatus(self):
        self.setStatus('ReadyToLoneBreak')


class ThreadTimer(threading.Thread):
    def __init__(self, group=None, target=None, name=None, args=(), kwargs=None, *, daemon=None, full_time,
                 timeoutCallBack):
        super().__init__(group, target, name, args, kwargs, daemon=daemon)
        self.isRun = True
        self.fullTime = full_time
        self.timeoutCallBack = timeoutCallBack

    def run(self):
        start_time = time.perf_counter()
        last_time = 0
        self.isRun = True
        while self.isRun:
            time.sleep(0.2)
            current_time = time.perf_counter()
            view_time = self.fullTime - (current_time - start_time)
            if view_time <= 0:
                self.timeoutCallBack()
                break
            if view_time != last_time:
                mainWindow.viewTime(view_time)
                last_time = view_time

    def stop(self):
        self.isRun = False


def main():
    global mainWindow

    app = QApplication(sys.argv)

    # 加载中文
    # lang = QLocale.system().name()
    # print('Language: '+lang)
    # trans = QTranslator()
    # trans.load('i18n/'+lang+'.qm')
    # if not app.installTranslator(trans):
    #     print('Failed to load translator file!')

    mainWindow = MainWindow()
    mainWindow.setStatus('ReadyToWork')
    mainWindow.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass
