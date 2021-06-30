#!/usr/bin/env python3
# coding: utf-8
# -*- coding: utf-8 -*-

import sys
import gesture_recognizer_ui as main_ui

from PyQt5 import QtWidgets


'''
START:
- Type python3 gesture_recognizer.py in the console.

APPLICATION:
- To train gestures select "Training", then enter a name for a gesture and press the plus button.
- Afterwards, draw a suitable gesture in the window on the right hand side and click on the "Save" button.
- To recognise gestures, switch to recognition mode and draw a gesture in the window on the right hand side.
- The recognised gesture is displayed in the upper left corner.
- If the gesture is not similar to a previously trained gesture, "no match" is displayed.

- Numbers can be distinguished well if you draw a one as a vertical line, otherwise it is difficult to
  distinguish it from a seven.
- Letters are hard to keep distinct and need some training to be drawn in a single stroke.

Author Sarah
Reviewer: Jonas
'''

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(True)

    win = main_ui.MainWindow()
    win.show()

    sys.exit(app.exec_())
