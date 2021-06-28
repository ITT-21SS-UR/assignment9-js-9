#!/usr/bin/env python3
# coding: utf-8
# -*- coding: utf-8 -*-

from QDrawWidget import QDrawWidget
from PyQt5 import QtWidgets, QtCore, QtGui
import matplotlib.pyplot as plt
import sys

import gesture_recognizer_model as model
import gesture_recognizer_ui as main_ui



if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(True)

    points = [(454, 382), (456, 384), (459, 385), (463, 388), (473, 394), (480, 397), (489, 401),
              (493, 401), (504, 404), (530, 406), (553, 408), (561, 408), (588, 408), (603, 408),
              (621, 403), (654, 390), (707, 361), (740, 342), (803, 299), (822, 283), (872, 243),
              (901, 219), (927, 198), (1022, 104), (1024, 101), (1026, 100), (1027, 98), (1028, 97),
              (1030, 95), (1031, 94), (1032, 93)]
    

    win = main_ui.MainWindow()
    win.show()

    sys.exit(app.exec_())
