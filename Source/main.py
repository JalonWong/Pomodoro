# coding=utf-8
import sys
import platform
import time
import ctypes
from PyQt5 import QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QTranslator, QFileInfo, QTimer
from MyConfig import *
from MainWindow import MainWindow

if platform.system() == 'Windows':
    myAppId = 'jalon.pomodoro'  # Arbitrary string
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myAppId)

Config = None
AppIcon = None
EXE_Flag = False


class MainCtrl(MainWindow):
    Run = 0
    ReadyToWork = 1
    ReadyToShortBreak = 2
    ReadyToLoneBreak = 3

    def __init__(self):
        super().__init__(AppIcon, EXE_Flag)
        self.nextTime = 0
        self.nextTipText = ''
        self.status = self.ReadyToWork
        self.lastStatue = self.ReadyToWork
        self.timer = MyTimer(self)
        self.timer.update.connect(self.viewTime)
        self.timer.fullTimeout.connect(self.timeout)

        self.buttonMain.clicked.connect(self.mainClicked)

    def close(self):
        self.timer.stop()
        super().close()
        print('exit')

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
            if self.tomatoCount % Config.longBreakPomodoroNumber == 0:
                self.setStatus(self.ReadyToLoneBreak)
            else:
                self.setStatus(self.ReadyToShortBreak)

    # 状态管理
    def setStatus(self, state):
        self.lastStatue = self.status
        self.status = state
        if state == self.Run:
            self.buttonMain.setText(self.s.strReset)
            self.timer.runTimer(self.nextTime)
            self.setTrayToolTipText(self.nextTipText)
        else:
            self.timer.stop()
            self.setTrayToolTipText(self.s.strStop)

            if state == self.ReadyToWork:
                self.workView(self.s.strWork)
                self.nextTipText = self.s.strWork
                self.nextTime = Config.workTime
            elif state == self.ReadyToShortBreak:
                self.breakView(self.s.strBreak)
                self.nextTipText = self.s.strBreak
                self.nextTime = Config.shortTime
            elif state == self.ReadyToLoneBreak:
                self.breakView(self.s.strLongBreak)
                self.nextTipText = self.s.strLongBreak
                self.nextTime = Config.longTime

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
        self.setInterval(1000)
        self.timeout.connect(self.onTick)
        self.fullTime = 0

    def onTick(self):
        self.fullTime -= 1
        if self.fullTime <= 0:
            self.stop()
            self.fullTimeout.emit()
        else:
            self.update.emit(self.fullTime)

    def runTimer(self, full_time):
        self.fullTime = full_time
        super().start()


def main():
    global Config
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

    Config = ConfigData()

    # Language
    print('Language: ' + Config.lang)
    trans = QTranslator()
    trans.load('i18n/' + Config.lang + '.qm')
    if not app.installTranslator(trans):
        print('Failed to load translator file!')

    m = MainCtrl()
    m.setWorkStatus()
    m.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass
