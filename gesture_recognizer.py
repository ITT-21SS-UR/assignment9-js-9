#!/usr/bin/env python3
# coding: utf-8
# -*- coding: utf-8 -*-

import sys
import gesture_recognizer_ui as main_ui

from PyQt5 import QtWidgets

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(True)

    win = main_ui.MainWindow()
    win.show()

    sys.exit(app.exec_())
