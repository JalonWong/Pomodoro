# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(504, 376)
        self.gridLayout = QtWidgets.QGridLayout(Form)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.labelTime = QtWidgets.QLabel(Form)
        self.labelTime.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelTime.sizePolicy().hasHeightForWidth())
        self.labelTime.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(30)
        font.setBold(True)
        font.setWeight(75)
        self.labelTime.setFont(font)
        self.labelTime.setTextFormat(QtCore.Qt.AutoText)
        self.labelTime.setAlignment(QtCore.Qt.AlignCenter)
        self.labelTime.setObjectName("labelTime")
        self.verticalLayout.addWidget(self.labelTime)
        self.buttonMain = QtWidgets.QPushButton(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.buttonMain.sizePolicy().hasHeightForWidth())
        self.buttonMain.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(30)
        font.setBold(False)
        font.setWeight(50)
        self.buttonMain.setFont(font)
        self.buttonMain.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.buttonMain.setFlat(False)
        self.buttonMain.setObjectName("buttonMain")
        self.verticalLayout.addWidget(self.buttonMain)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Pomodoro"))
        self.labelTime.setText(_translate("Form", "25:00"))
        self.buttonMain.setText(_translate("Form", "Start"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())

