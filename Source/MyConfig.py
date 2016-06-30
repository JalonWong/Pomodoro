# coding=utf-8
import configparser
from PyQt5.QtCore import QLocale


class ConfigData(object):
    def __init__(self):
        super().__init__()

        self.config = configparser.ConfigParser()
        filename = 'config.ini'
        self.config.read(filename)

        self.lang = QLocale.system().name()
        self.lang = self.getValue('DEFAULT', 'Language', self.lang)

        self.workTime = int(float(self.getValue('DEFAULT', 'WorkTime', '25')) * 60)
        self.shortTime = int(float(self.getValue('DEFAULT', 'BreakTime', '5')) * 60)
        self.longTime = int(float(self.getValue('DEFAULT', 'LongBreakTime', '15')) * 60)
        self.longBreakPomodoroNumber = int(self.getValue('DEFAULT', 'PomodoroForLongBreak', '4'))

        file = open(filename, 'w')
        self.config.write(file)
        file.close()

        for key in self.config['DEFAULT']:
            print(key)

    def getValue(self, section, key, default_value):
        s = self.config[section]
        if key in s:
            return s[key]
        else:
            s[key] = default_value
            return default_value
