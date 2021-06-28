#!/usr/bin/env python3
# coding: utf-8
# -*- coding: utf-8 -*-

from QDrawWidget import QDrawWidget
from PyQt5 import QtWidgets, QtCore, QtGui
from pyqtgraph.flowchart import Flowchart, Node
from sklearn import svm
import pyqtgraph.flowchart.library as fclib
import sys

import gesture_recognizer_model as model
import gesture_recognizer_ui as main_ui
from gesture_recognizer_ui import SvmNodeCtrl


class SvmNode(Node):
    nodeName = "SVM"

    def __init__(self, name):
        terminals = {"dataIn": {"io": "in"},
                     "categoryOut": {"io": "out"}}
        super().__init__(name, terminals)

        self.__buffer = []
        self.__classifier = svm.SVC()

        self.ui = SvmNodeCtrl()
        self.ui.training_started.connect(self.__clear_buffer)
        self.ui.data_changed.connect(self.__process_training_data)
        self.ui.mode_changed.connect(self.__clear_buffer)

    def ctrlWidget(self):
        return self.ui

    def process(self, **kargs):
        if self.ui.get_mode() == SvmNodeCtrl.SvmMode.Inactive:
            return {"categoryOut": "** classifier inactive **"}

        self.__buffer = kargs["dataIn"]

        if self.ui.get_mode() == SvmNodeCtrl.SvmMode.Training:
            return {"categoryOut": "** training mode **"}

        if len(self.ui.get_categories()) < 2:
            return {"categoryOut": "** you have to train at least 2 categories **"}

        try:
            category = self.__classifier.predict([self.__buffer])
            return {"categoryOut": self.ui.get_category_name(category[0])}
        except ValueError:
            return {"categoryOut": "** need more training data **"}

    def __process_training_data(self):
        self.ui.set_data(self.__buffer)
        self.__clear_buffer()
        self.__train_data()

    def __clear_buffer(self):
        self.__buffer = []

    def __train_data(self):
        training_set = []
        classifiers = []

        categories = self.ui.get_categories()
        all_data = self.ui.get_all_data()

        for i in range(len(categories)):
            category_name = self.ui.get_category_name(i)
            data = all_data[category_name]

            for d in data:
                training_set.append(d)
                classifiers.append(i)

        try:
            self.__classifier.fit(training_set, classifiers)
        except ValueError:
            pass


fclib.registerNodeType(SvmNode, [("Classifier",)])

class TransformationNode(Node): # TODO
    nodeName = "TransformNode"

    SAMPLE_SIZE = 64

    def __init__(self, name):
        terminals = {"accelX": {"io": "in"},
                     "accelY": {"io": "in"},
                     "accelZ": {"io": "in"},
                     "dspOut": {"io": "out"}}
        super().__init__(name, terminals)

        self.clear()

    def clear(self):
        self.__avg = []

    def process(self, **kargs):
        pass


fclib.registerNodeType(TransformationNode, [("TransformNode",)])

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
