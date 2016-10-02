# -*- coding: utf-8 -*-
from PyQt5.QtCore import QObject

i18nStrings = None


class Strings(QObject):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.strPomodoro = self.tr('Pomodoro')
        self.strWork = self.tr('Work')
        self.strBreak = self.tr('Break')
        self.strLongBreak = self.tr('Long Break')
        self.strDecreasePomodoro = self.tr('Decrease a Pomodoro')
        self.strExit = self.tr('Exit')
        self.strShowWindow = self.tr('Show Window')
        self.strHideWindow = self.tr('Hide Window')
        self.strReset = self.tr('Reset')


def GetStrings():
    global i18nStrings
    if i18nStrings is None:
        i18nStrings = Strings()
    return i18nStrings
