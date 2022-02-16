from PyQt5 import QtWidgets, uic, QtCore, QtGui
from PyQt5.QtWidgets import QLineEdit
import sys
import os
import threading
import cv2 as cv
import imutils

cali_image = "HUST_GUI/Reference image/default_image.png"

class MyLabel(QtWidgets.QLabel):
    x0 = 0
    y0 = 0
    x1 = 0
    y1 = 0
    flag = False
 #Mouse click event
    def mousePressEvent(self,event):
        self.flag = True
        self.x0 = event.x()
        self.y0 = event.y()
 #Mouse release event
    def mouseReleaseEvent(self,event):
        self.flag = False
 #Mouse movement events
    def mouseMoveEvent(self,event):
        if self.flag:
            self.x1 = event.x()
            self.y1 = event.y()
            self.update()
 #Draw events
    def paintEvent(self, event):
        super().paintEvent(event)
        rect = QtCore.QRect(self.x0, self.y0, abs(self.x1-self.x0), abs(self.y1-self.y0))
        painter = QtGui.QPainter(self)
        painter.setPen(QtGui.QPen(QtCore.Qt.red,2,QtCore.Qt.SolidLine))
        painter.drawRect(rect)

class calibrate_screen(QtWidgets.QMainWindow):
    def __init__(self):
        super(calibrate_screen, self).__init__()
        uic.loadUi('Ver 1/calibration screen ver 1.ui', self)

        #button function
        self.landmark_button.clicked.connect(self.save_landmark)
        self.slot_button.clicked.connect(self.save_slot)
        self.undo_button.clicked.connect(self.undo_function)
        self.redo_button.clicked.connect(self.redo_function)
        self.reset_button.clicked.connect(self.reset_function)

        self.lb = MyLabel(self.calibrate_image)  # redefined label
        #self.lb.setGeometry(QtCore.QRect(30, 30, 511, 541))
        # img = cv.imread("HUST_GUI/Data/lmTst_0.jpg")
        # height, width, bytesPerComponent = img.shape
        # bytesPerLine = 3 * width
        # cv.cvtColor(img, cv.COLOR_BGR2RGB, img)
        # QImg = QtGui.QImage(img.data, width, height, bytesPerLine, QtGui.QImage.Format_RGB888)
        # pixmap = QtGui.QPixmap.fromImage(QImg)
        #
        # self.lb.setPixmap(pixmap)
        # self.lb.setCursor(QtCore.Qt.CrossCursor)

        self.show()

    def save_landmark(self):
        #save data as landmark
        pass
    def save_slot(self):
        self.begin = (self.lb.x0, self.lb.y0)
        self.end = (self.lb.x1, self.lb.y1)
        # self.update()
        slot = (self.begin, self.end)
        # print(slot)
        if not all(self.begin) or not all(self.end):
            print("pass")
            # pass
        else:
            slot_str = str(slot)[1:len(str(slot))-1]
            self.list_dataWidget.addItem(slot_str)
            print(slot_str)
        #save data as parking slot
        #pass
    def undo_function(self):
        #undo selection
        pass
    def redo_function(self):
        #redo selection
        pass
    def reset_function(self):
        #reset selection
        pass

app = QtWidgets.QApplication(sys.argv)

widget=QtWidgets.QStackedWidget()
#main_window=landing_page()

window_1 = calibrate_screen()
#window_draw = draw_screen()


widget.addWidget(window_1)
#widget.addWidget(window_draw)

widget.setFixedHeight(800)
widget.setFixedWidth(1000)
widget.show()
app.exec_()
