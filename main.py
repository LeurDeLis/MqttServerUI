# -*- coding: utf-8 -*-
# @Time    : 2025/7/24 23:57
# @Author  : LeurDeLis
# @File    : main.py
# @Software: PyCharm


import sys
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
from PyQt5 import QtCore, QtWidgets, QtGui
import icon_rc
from MqttServer import Ui_MainWindow

class MyMqtt(QtWidgets.QMainWindow):
    def __init__(self):
        super(MyMqtt, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MyMqtt()
    window.show()
    sys.exit(app.exec_())
