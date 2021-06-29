from pyqtgraph.Qt import QtGui, QtCore, QtWidgets

class QDrawWidget(QtWidgets.QWidget):
    
    drawing_finished = QtCore.pyqtSignal()

    def __init__(self, width=800, height=800):
        super().__init__()
        self.setMinimumSize(width, height)
        self.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.drawing = False
        self.grid = True
        self.points = []
        self.setMouseTracking(True) # only get events when button is pressed
        self.initUI()

    def initUI(self):      
        self.setWindowTitle('Drawable')
        self.show()
        
    def clear(self):
        self.drawing = False
        self.points = []
        self.update()
        self.drawing_finished.emit()

    def mousePressEvent(self, ev):
        if ev.button() == QtCore.Qt.LeftButton:
            self.drawing = True
            self.points = []
            self.update()
            
    def mouseReleaseEvent(self, ev):
        if ev.button() == QtCore.Qt.LeftButton:
            self.drawing = False
            self.update() 
            self.drawing_finished.emit()

    def mouseMoveEvent(self, ev):
        if self.drawing:
            self.points.append((ev.x(), ev.y()))
            self.update() 
    
    def poly(self, pts):
        return QtGui.QPolygonF(map(lambda p: QtCore.QPointF(*p), pts))

    def paintEvent(self, ev):
        qp = QtGui.QPainter()
        qp.begin(self)
        qp.setBrush(QtGui.QColor(0, 0, 0))
        qp.drawRect(ev.rect())
        qp.setBrush(QtGui.QColor(20, 255, 190))
        qp.setPen(QtGui.QColor(0, 155, 0))
        qp.drawPolyline(self.poly(self.points))
        
        for point in self.points:
            qp.drawEllipse(point[0]-1, point[1] - 1, 2, 2)
        if self.grid:
            qp.setPen(QtGui.QColor(255, 100, 100, 20))  # semi-transparent
            
            for x in range(0, self.width(), 20):
                qp.drawLine(x, 0, x, self.height())
                
            for y in range(0, self.height(), 20):
                qp.drawLine(0, y, self.width(), y)
                
        qp.end()
