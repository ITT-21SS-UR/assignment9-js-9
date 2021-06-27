from QDrawWidget import QDrawWidget
from PyQt5 import QtWidgets, QtCore, QtGui
import matplotlib.pyplot as plt
import sys

import gesture_recognizer_model as model



if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    draw_widget = QDrawWidget()

    points = [(454, 382), (456, 384), (459, 385), (463, 388), (473, 394), (480, 397), (489, 401),
              (493, 401), (504, 404), (530, 406), (553, 408), (561, 408), (588, 408), (603, 408),
              (621, 403), (654, 390), (707, 361), (740, 342), (803, 299), (822, 283), (872, 243),
              (901, 219), (927, 198), (1022, 104), (1024, 101), (1026, 100), (1027, 98), (1028, 97),
              (1030, 95), (1031, 94), (1032, 93)]
    
    # set the draw widgets custom filter variable to the function
    # of the same way which applies our transformation stack
    draw_widget.custom_filter = model.custom_filter
    #custom_filter(points)
    #transpose_points(points)
    # plt.plot(model.transpose_points(draw_widget.points)[0], model.transpose_points(draw_widget.points)[1])
    # plt.plot(transpose_points(draw_widget.points))
    
    # s1 = model.normalize([(-1,0), (0,-1), (1,0), (0,1)])
    # sim = model.calculate_similarity(s1, model.normalize(draw_widget.points))
    # print("print:", sim)    
