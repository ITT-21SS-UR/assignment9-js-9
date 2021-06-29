from PyQt5 import QtCore, QtGui, QtWidgets
from enum import Enum
from QDrawWidget import *
import gesture_recognizer_transform as transform
import sys

class GestureMode(Enum):
    Training = 1
    Recognition = 2

class GestureModel(QtCore.QObject):

    mode_changed = QtCore.pyqtSignal()
    data_changed = QtCore.pyqtSignal()
    data_saved = QtCore.pyqtSignal()
    gesture_recognized = QtCore.pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)

        self.__mode = GestureMode.Training
        self.__data = {}
        self.__pending_data = []

    def get_mode(self):
        return self.__mode

    def set_mode(self, mode):
        self.__mode = mode
        self.mode_changed.emit()

    def has_data(self, gesture_name):
        return len(self.__data[gesture_name]) > 0
    
    def is_data_available(self):
        return len(self.__pending_data) > 0

    def set_data(self, data):
        if len(data) > 0:
            self.__pending_data = transform.normalize(data)
        else:
            self.__pending_data = []

        self.data_changed.emit()

    def recognize(self):
        if self.__mode != GestureMode.Recognition:
            return

        if not self.__pending_data:
            self.gesture_recognized.emit(None)
            return

        best_match = (sys.maxsize, None)
        for gesture, data_set in self.__data.items():
            for data in data_set:
                sim = transform.calculate_similarity(self.__pending_data, data)
                if sim < best_match[0]:
                    best_match = (sim, gesture)

        if best_match[0] > 1500:
            self.gesture_recognized.emit("** no match **")
        else:
            self.gesture_recognized.emit(best_match[1])

    def clear(self):
        self.__pending_data = []
        self.data_changed.emit()

    def save_data(self, gesture_name):
        self.__data[gesture_name].append(self.__pending_data)
        self.clear()
        self.data_changed.emit()
        self.data_saved.emit()

    def add_gesture(self, name):
        self.clear_gesture(name)

    def clear_gesture(self, name):
        self.__data[name] = []
        self.data_changed.emit()

    def delete_gesture(self, name):
        self.__data.pop(name)
        self.data_changed.emit()

class GestureWidget(QtGui.QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.__model = GestureModel()
        self.__setup_ui()

    def get_gesture_name(self, index=None):
        if index is None:
            return self.__gestures_list.currentText()

        return self.__gestures_list.itemText(index)

    def get_model(self):
        return self.__model

    def set_model(self, model):
        self.__model = model

    def __setup_ui(self):
        layout = QtWidgets.QVBoxLayout()

        mode_group = QtWidgets.QGroupBox("Mode")
        training_mode_button = QtWidgets.QRadioButton("Training", mode_group)
        training_mode_button.setChecked(True)
        recognition_mode_button = QtWidgets.QRadioButton("Recognition", mode_group)
        mode_group_layout = QtWidgets.QVBoxLayout()
        mode_group_layout.addWidget(training_mode_button)
        mode_group_layout.addWidget(recognition_mode_button)
        mode_group.setLayout(mode_group_layout)

        gestures_group = QtWidgets.QGroupBox("Gestures")
        gesture_name_edit = QtWidgets.QLineEdit()
        gesture_name_label = QtWidgets.QLabel("New gesture name")
        gesture_name_label.setBuddy(gesture_name_edit)
        gesture_add_button = QtWidgets.QToolButton()
        gesture_add_button.setText("+")
        gesture_name_layout = QtWidgets.QHBoxLayout()
        gesture_name_layout.addWidget(gesture_name_edit)
        gesture_name_layout.addWidget(gesture_add_button)
        gestures_list = QtWidgets.QComboBox()
        save_button = QtWidgets.QPushButton("Save")
        save_button.setEnabled(False)
        reset_button = QtWidgets.QPushButton("Reset")
        reset_button.setEnabled(False)
        delete_button = QtWidgets.QPushButton("Delete")
        delete_button.setEnabled(False)
        button_layout = QtWidgets.QHBoxLayout()
        button_layout.addWidget(reset_button)
        button_layout.addWidget(delete_button)
        gestures_group_layout = QtWidgets.QVBoxLayout()
        gestures_group_layout.addWidget(gesture_name_label)
        gestures_group_layout.addLayout(gesture_name_layout)
        gestures_group_layout.addWidget(gestures_list)
        gestures_group_layout.addWidget(save_button)
        gestures_group_layout.addLayout(button_layout)
        gestures_group.setLayout(gestures_group_layout)

        recognition_group = QtWidgets.QGroupBox("Recognized Gesture")
        recognized_gesture_label = QtWidgets.QLabel()
        recognized_gesture_label.setAlignment(QtCore.Qt.AlignCenter)
        recognition_group_layout = QtWidgets.QVBoxLayout()
        recognition_group_layout.addWidget(recognized_gesture_label)
        recognition_group.setLayout(recognition_group_layout)

        layout.addWidget(recognition_group)
        layout.addStretch()
        layout.addWidget(mode_group)
        layout.addWidget(gestures_group)

        self.setLayout(layout)
        self.__gestures_group = gestures_group
        self.__gestures_list = gestures_list
        self.__gesture_name_edit = gesture_name_edit
        self.__train_button = save_button
        self.__reset_button = reset_button
        self.__delete_button = delete_button
        self.__recognized_gesture_label = recognized_gesture_label

        training_mode_button.clicked.connect(self.__on_mode_button_clicked)
        recognition_mode_button.clicked.connect(self.__on_mode_button_clicked)
        gesture_add_button.clicked.connect(self.__on_add_gesture)
        delete_button.clicked.connect(self.__on_delete_gesture)
        save_button.clicked.connect(lambda: self.__model.save_data(self.get_gesture_name()))
        reset_button.clicked.connect(lambda: self.__model.clear_gesture(self.get_gesture_name()))

        self.__model.mode_changed.connect(self.__on_mode_changed)
        self.__model.data_changed.connect(self.__on_model_data_changed)
        self.__model.gesture_recognized.connect(self.__set_recognized_gesture)
        self.__set_recognized_gesture()

    def __on_mode_button_clicked(self):
        if self.sender().text() == "Training":
            self.__model.set_mode(GestureMode.Training)

        if self.sender().text() == "Recognition":
            self.__model.set_mode(GestureMode.Recognition)

    def __on_mode_changed(self):
        if self.__model.get_mode() == GestureMode.Training:
            self.__gestures_group.setEnabled(True)

        if self.__model.get_mode() == GestureMode.Recognition:
            self.__gestures_group.setEnabled(False)

        self.__set_recognized_gesture()

    def __on_add_gesture(self):
        name = self.__gesture_name_edit.text()
        if not name:
            return

        if self.__gestures_list.findText(name, QtCore.Qt.MatchFixedString) >= 0:
            return

        self.__gesture_name_edit.setText("")
        self.__gestures_list.addItem(name)
        self.__gestures_list.setCurrentIndex(self.__gestures_list.count() - 1)
        self.__model.add_gesture(name)

    def __on_delete_gesture(self):
        name = self.get_gesture_name()
        self.__gestures_list.removeItem(self.__gestures_list.currentIndex())
        self.__model.delete_gesture(name)

    def __on_model_data_changed(self):
        self.__update_training_buttons()
        self.__model.recognize()

    def __update_training_buttons(self):
        if self.__model.get_mode() != GestureMode.Training:
            return

        self.__delete_button.setEnabled(self.__gestures_list.count() > 0)

        can_enable_reset_btn = self.__gestures_list.count() > 0 \
                                    and self.__model.has_data(self.get_gesture_name())
        self.__reset_button.setEnabled(can_enable_reset_btn)

        can_enable_training_btn = self.__gestures_list.count() > 0 \
                                    and self.__model.is_data_available()
        self.__train_button.setEnabled(can_enable_training_btn)

    def __set_recognized_gesture(self, gesture=None):
        text = "** n/a **" if not gesture else gesture
        self.__recognized_gesture_label.setText("<b>" + text + "</b>")

class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Gesture Recognizer")

        layout = QtWidgets.QHBoxLayout()

        gesture = GestureWidget()
        layout.addWidget(gesture)

        draw_widget = QDrawWidget()
        layout.addWidget(draw_widget, 1)

        draw_widget.drawing_finished.connect(lambda: gesture.get_model().set_data(draw_widget.points))
        gesture.get_model().data_saved.connect(draw_widget.clear)
        gesture.get_model().mode_changed.connect(draw_widget.clear)

        cw = QtGui.QWidget()
        cw.setLayout(layout)
        self.setCentralWidget(cw)
