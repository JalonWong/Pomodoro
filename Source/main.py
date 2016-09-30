# coding=utf-8
import sys
import platform
import time
import ctypes
from PyQt5 import QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QCursor
from PyQt5.QtCore import QTranslator, QFileInfo, QTimer
from MyConfig import *
from MainWindow import MainWindow

if platform.system() == 'Windows':
    myAppId = 'jalon.pomodoro'  # Arbitrary string
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myAppId)

configData = None
AppIcon = None
EXE_Flag = False


class Main(MainWindow):
    Run = 0
    ReadyToWork = 1
    ReadyToShortBreak = 2
    ReadyToLoneBreak = 3

    def __init__(self):
        super().__init__(AppIcon, EXE_Flag)
        self.nextTime = 0
        self.status = self.ReadyToWork
        self.lastStatue = self.ReadyToWork
        self.timer = MyTimer(self)
        self.timer.update.connect(self.viewTime)
        self.timer.fullTimeout.connect(self.timeout)

        self.buttonMain.customContextMenuRequested.connect(self.menuRequested)
        self.buttonMain.clicked.connect(self.mainClicked)

    def close(self):
        self.timer.stop()
        super().close()
        print('exit')

    def menuRequested(self):
        if self.status != self.Run:
            self.buttonMenu.exec(QCursor.pos())

    def mainClicked(self):
        if self.status != self.Run:
            if self.status == self.ReadyToWork:
                self.hide()
            self.setStatus(self.Run)
        else:
            self.setStatus(self.lastStatue)

    def timeout(self):
        print('timeout')
        self.showWindow()
        if self.lastStatue != self.ReadyToWork:
            self.setStatus(self.ReadyToWork)
        else:
            self.tomatoCount += 1
            self.setCompleteTomato(self.tomatoCount)
            if self.tomatoCount % configData.longBreakPomodoroNumber == 0:
                self.setStatus(self.ReadyToLoneBreak)
            else:
                self.setStatus(self.ReadyToShortBreak)

    # 状态管理
    def setStatus(self, state):
        self.lastStatue = self.status
        self.status = state
        if state == self.Run:
            self.buttonMain.setText(self.tr('Reset'))
            self.timer.runTimer(self.nextTime)
        else:
            self.timer.stop()

            if state == self.ReadyToWork:
                self.workView(self.tr('Work'))
                self.nextTime = configData.workTime
            elif state == self.ReadyToShortBreak:
                self.breakView(self.tr('Break'))
                self.nextTime = configData.shortTime
            elif state == self.ReadyToLoneBreak:
                self.breakView(self.tr('Long Break'))
                self.nextTime = configData.longTime

            self.viewTime(self.nextTime)

    def setWorkStatus(self):
        self.setStatus(self.ReadyToWork)

    def setBreakStatus(self):
        self.setStatus(self.ReadyToShortBreak)

    def setLoneBreakStatus(self):
        self.setStatus(self.ReadyToLoneBreak)


class MyTimer(QTimer):
    fullTimeout = QtCore.pyqtSignal()
    update = QtCore.pyqtSignal(int)

    def __init__(self, parent):
        super().__init__(parent)
        self.setInterval(100)
        self.timeout.connect(self.onTick)
        self.fullTime = 0
        self.startTime = 0
        self.lastTime = 0

    def onTick(self):
        current_time = time.perf_counter()
        view_time = self.fullTime - (current_time - self.startTime)
        if view_time <= 0:
            self.stop()
            self.fullTimeout.emit()
        elif int(view_time) != self.lastTime:
            self.lastTime = int(view_time)
            self.update.emit(self.lastTime)

    def runTimer(self, full_time):
        self.fullTime = full_time
        self.startTime = time.perf_counter()
        self.lastTime = 0
        super().start()


def main():
    global configData
    global EXE_Flag
    global AppIcon

    app = QApplication(sys.argv)

    filename = sys.argv[0]
    if filename.split('.')[1] == 'exe':
        iconF = QFileIconProvider()
        AppIcon = iconF.icon(QFileInfo(filename))
        EXE_Flag = True
    else:
        AppIcon = QIcon('Resource/tomato.ico')

    configData = ConfigData()

    # Language
    print('Language: ' + configData.lang)
    trans = QTranslator()
    trans.load('i18n/'+configData.lang+'.qm')
    if not app.installTranslator(trans):
        print('Failed to load translator file!')

    mainWindow = Main()
    mainWindow.setWorkStatus()
    mainWindow.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass
