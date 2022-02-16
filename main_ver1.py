from PyQt5 import QtWidgets, uic, QtCore, QtGui
import sys
import os
import threading
import cv2 as cv
parent_dir = "D:/HUST_GUI/Parking Lots/"
#parent_dir = "HUST_GUI/Parking Lots/"

default_ref_image = "D:/HUST_GUI/Reference image/default_ref_image.png"
#default_ref_image = "HUST_GUI/Reference image/default_ref_image.png"

class landing_page(QtWidgets.QMainWindow):
    def __init__(self):
        super(landing_page, self).__init__()
        uic.loadUi("open window ver 2.ui", self)

        #button function
        self.define_new_button.clicked.connect(self.define_new)
        self.process_auto_button.clicked.connect(self.process_auto)
        self.adjust_button.clicked.connect(self.adjust_lot)
        self.exit_button.clicked.connect(self.exit)

        self.show()

    def define_new(self):
        #move to define new parking lot window
        widget.setCurrentWidget(window_define)
        #pass
    def process_auto(self):
        #move to process parking lot auto window
        widget.setCurrentWidget(window_auto)
        #pass
    def adjust_lot(self):
        #move to adjust parking lot window
        widget.setCurrentWidget(window_adjust)
        #pass
    def exit(self):
        #switch to monitor window
        pass

class define_new_lot(QtWidgets.QMainWindow):
    def __init__(self):
        super(define_new_lot, self).__init__()
        uic.loadUi('define new name ver 2.ui', self)

        # button function
        self.back_button.clicked.connect(self.back_function)
        self.next_button.clicked.connect(self.next_function)

        # enter parking lot name line edit
        self.name_parking_lot.returnPressed.connect(self.name_lot)

        self.show()

    def back_function(self):
        # move back to landing page
        widget.setCurrentWidget(window_landing)

    def next_function(self):
        # send name to the reference
        directory = self.name_parking_lot.text()
        ref_file = open("temporary/reference_image.txt", "w")
        ref_file.write(directory)
        ref_file.close()
        # move to select reference image window
        widget.setCurrentWidget(window_select)

    def name_lot(self):
        # getting text from the line edit when enter is pressed
        # create directory with text input
        directory = self.name_parking_lot.text()
        #parent_dir = "D:/HUST_GUI/Parking Lots/"
        sub_folders = [name for name in os.listdir(parent_dir) if os.path.isdir(os.path.join(parent_dir, name))]

        if (directory in sub_folders):
            self.noti_label.setText(directory + " already exists, please choose another name")
        else:
            path = os.path.join(parent_dir, directory)
            os.mkdir(path)
            self.noti_label.setText(directory + " : valid name")
            # write into file

            auto_file = open("temporary/auto_parking_lot.txt", "w")
            auto_file.write(directory)
            auto_file.close()

            adjust_file = open("temporary/adjust_parking_lot.txt", "w")
            adjust_file.write(directory)
            adjust_file.close()

class run_auto(QtWidgets.QMainWindow):
    def __init__(self):
        super(run_auto, self).__init__()
        uic.loadUi('auto select ver 2.ui', self)
        #button function
        self.define_button.clicked.connect(self.define)
        self.run_auto_button.clicked.connect(self.run_auto)
        self.back_button.clicked.connect(self.back_function)
        self.run_auto_button.clicked.connect(self.run_auto)

        #list widget
        #add item from new define parking lot
        #parent_dir = "D:/HUST_GUI/Parking Lots/"
        sub_folders = [name for name in os.listdir(parent_dir) if os.path.isdir(os.path.join(parent_dir, name))]
        for item in sub_folders:
           self.list_parking_lotWidget.addItem(item)

        #refresh function
        self.refresh_function()
        self.delete_function()

        self.show()

    def define(self):
        #move to define new parking lot window
        widget.setCurrentWidget(window_define)
    def run_auto(self):
        #move to result window
        #name=self.list_parking_lotWidget.currentItem().text()
        #if not name:
        #    notification = "nothing selected, please choose a parking lot."
        #else:
        #    notification = name + " selected."
        #self.noti_label.setText(notification)
        widget.setCurrentWidget(window_result)

    def back_function(self):
        #move back to landing page
        widget.setCurrentWidget(window_landing)
    def refresh_function(self):
        threading.Timer(1.0, self.refresh_function).start()
        add_file = open("temporary/auto_parking_lot.txt", "r+")
        new_lot = add_file.read()

        if os.stat("temporary/auto_parking_lot.txt").st_size == 0:
            pass
        else:
            self.list_parking_lotWidget.addItem(new_lot)
            add_file.truncate(0)
            add_file.close()

    def delete_function(self):
        threading.Timer(1.0, self.delete_function).start()
        delete_file = open("temporary/delete_lot.txt", "r+")
        delete_lot = delete_file.read()
        if os.stat("temporary/delete_lot.txt").st_size == 0:
            pass
        else:
            items = self.list_parking_lotWidget.findItems(delete_lot, QtCore.Qt.MatchExactly)
            if len(items) > 0:
                for item in items:
                    self.list_parking_lotWidget.takeItem(self.list_parking_lotWidget.row(item))
            delete_file.truncate(0)
            delete_file.close()

        #print("timer running")

class adjust_lot(QtWidgets.QMainWindow):
    def __init__(self):
        super(adjust_lot, self).__init__()
        uic.loadUi('adjust select ver 2.ui', self)

        #button function
        self.adjust_button.clicked.connect(self.adjust_lot)
        self.back_button.clicked.connect(self.back_function)
        self.delete_button.clicked.connect(self.delete_lot)
        #list widget
        # add item from new define parking lot
        #parent_dir = "D:/HUST_GUI/Parking Lots/"
        sub_folders = [name for name in os.listdir(parent_dir) if os.path.isdir(os.path.join(parent_dir, name))]
        for item in sub_folders:
            self.list_parking_lotWidget.addItem(item)

        self.refresh_function()
        self.show()
    def adjust_lot(self):
        # take the name of selected item
        # write into text file for select reference window to read

        chosen = self.list_parking_lotWidget.currentItem().text()
        #if not chosen:
        #    notification = "nothing selected, please choose a parking lot."
        #else:
        #    notification = chosen + " selected."
        #self.noti_label.setText(notification)

        ref_file = open("temporary/reference_image.txt", "w")
        ref_file.write(chosen)
        ref_file.close()

        #move to select reference image window
        widget.setCurrentWidget(window_select)
    def back_function(self):
        #move back to landing page
        widget.setCurrentWidget(window_landing)
    def delete_lot(self):
        name=self.list_parking_lotWidget.currentItem().text()
        #print(name)
        #delete a parking lot
        list_items= self.list_parking_lotWidget.selectedItems()
        if not list_items: return
        for item in list_items:
            self.list_parking_lotWidget.takeItem(self.list_parking_lotWidget.row(item))

        # remove directory
        #parent_dir = "D:/HUST_GUI/Parking Lots/"
        path = os.path.join(parent_dir, name)
        os.rmdir(path)

        delete_file = open("temporary/delete_lot.txt", "w")
        delete_file.write(name)

    def refresh_function(self):
        threading.Timer(1.0, self.refresh_function).start()
        f = open("temporary/adjust_parking_lot.txt", "r+")
        new_lot = f.read()
        if os.stat("temporary/adjust_parking_lot.txt").st_size == 0:
            pass
        else:
            self.list_parking_lotWidget.addItem(new_lot)
            f.truncate(0)
            f.close()
        #print("timer running")

class select_reference(QtWidgets.QMainWindow):
    def __init__(self):
        super(select_reference, self).__init__()
        uic.loadUi('image select ver 2.ui', self)

        #button function
        self.browse_button.clicked.connect(self.browse)
        self.capture_button.clicked.connect(self.capture_cam)
        self.back_button.clicked.connect(self.back_function)
        self.next_button.clicked.connect(self.next_function)
        self.reset_button.clicked.connect(self.reset_function)

        self.show()
    def browse(self):
        #browse database for reference photo
        #read file first
        chosen_lot = open("temporary/reference_image.txt", "r+")
        chosen_lot_name = chosen_lot.read()
        #parent_dir = "D:/HUST_GUI/Parking Lots/"

        #empty the file
        #if os.stat("temporary/reference_image.txt").st_size == 0:
        #    pass
        #else:
        #    chosen_lot.truncate(0)
        #    chosen_lot.close()

        #check if the chosen parking lot is in directory
        sub_folders = [name for name in os.listdir(parent_dir) if os.path.isdir(os.path.join(parent_dir, name))]
        if chosen_lot_name not in sub_folders:
            #notification = "cannot find directory"
            self.noti_label.setText("Cannot find directory, please choose another parking lot.")
        else:
            #creata a dialog to choose file
            path = os.path.join(parent_dir, chosen_lot_name)
            if len(os.listdir(path)) == 0:
                notification = "No images found in the directory: " + chosen_lot_name +"."
                self.noti_label.setText(notification)
            else:
                choose_image_dia = QtWidgets.QFileDialog(self)
                chosen_ref_image = choose_image_dia.getOpenFileName(self,"select reference image",path,"Images (*.jpg)")

                #set image in gui into the choosen image
                #print(chosen_ref_image[0])
                self.pixmap = QtGui.QPixmap(chosen_ref_image[0])
                self.ref_image.setPixmap(self.pixmap)

                self.image_name.setText(chosen_ref_image[0])

                self.noti_label.setText(" ")
                #write into text file for calibrate window to read
                cali_file = open("temporary/calibrate_image.txt", "w")
                cali_file.write(chosen_ref_image[0])
                cali_file.close()

    def capture_cam(self):
        #get data from preinstalled cam
        pass
    def reset_function(self):
        self.pixmap = QtGui.QPixmap(default_ref_image)
        self.ref_image.setPixmap(self.pixmap)

    def back_function(self):
        #move back to adjust window
        widget.setCurrentWidget(window_adjust)
    def next_function(self):
        #empty the file
        chosen_lot = open("temporary/reference_image.txt", "r+")
        if os.stat("temporary/reference_image.txt").st_size == 0:
            pass
        else:
            chosen_lot.truncate(0)
            chosen_lot.close()

        #move back to calibrate window
        widget.setCurrentWidget(window_calibrate)

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
        uic.loadUi('reference ver 2.ui', self)

        #button function
        self.landmark_button.clicked.connect(self.save_landmark)
        self.slot_button.clicked.connect(self.save_slot)
        self.undo_button.clicked.connect(self.undo_function)
        self.redo_button.clicked.connect(self.redo_function)
        self.reset_button.clicked.connect(self.reset_function)
        self.back_button.clicked.connect(self.back_function)
        self.next_button.clicked.connect(self.next_function)

        self.lb = MyLabel(self.calibrate_image)
        self.lb.setGeometry(QtCore.QRect(0, 0, self.calibrate_image.width(), self.calibrate_image.height()))

        #set image according to reference image
        self.set_cali_image()
        #select image function

        self.show()
    def save_landmark(self):
        #save data as landmark
        self.begin = (self.lb.x0, self.lb.y0)
        self.end = (self.lb.x1, self.lb.y1)
        slot = (self.begin, self.end)
        if not all(self.begin) or not all(self.end):
            # print("pass")
            pass
        else:
            slot_str = "lm:"+str(slot)[1:len(str(slot)) - 1]
            self.list_dataWidget.addItem(slot_str)
            # print(slot_str)
    def save_slot(self):
        #save data as parking slot
        self.begin = (self.lb.x0, self.lb.y0)
        self.end = (self.lb.x1, self.lb.y1)
        slot = (self.begin, self.end)
        if not all(self.begin) or not all(self.end):
            # print("pass")
            pass
        else:
            slot_str = "s:" + str(slot)[1:len(str(slot)) - 1]
            self.list_dataWidget.addItem(slot_str)
            # print(slot_str)
    def undo_function(self):
        #undo selection
        pass
    def redo_function(self):
        #redo selection
        pass
    def reset_function(self):
        #reset selection
        pass
    def back_function(self):
        #move back to select reference window
        widget.setCurrentWidget(window_select)
        #pass
    def next_function(self):
        #move back to result window
        widget.setCurrentWidget(window_result)
        #pass
    def set_cali_image(self):
        threading.Timer(1.0, self.set_cali_image).start()
        cali_file = open("temporary/calibrate_image.txt", "r+")
        cali_image = cali_file.read()

        result_image = cali_image
        if result_image:
            result_file = open("temporary/result_original.txt", "w")
            result_file.write(result_image)
            result_file.close()
            #print(result_image)
        else:
            pass
            #print("nothing")

        if os.stat("temporary/calibrate_image.txt").st_size == 0:
            pass
        else:
            #self.lb = MyLabel(self.calibrate_image)
            img = cv.imread(cali_image)
            img = cv.resize(img, (self.calibrate_image.width(), self.calibrate_image.height()))
            height, width, bytesPerComponent = img.shape
            bytesPerLine = 3 * width
            cv.cvtColor(img, cv.COLOR_BGR2RGB, img)
            QImg = QtGui.QImage(img.data, width, height, bytesPerLine, QtGui.QImage.Format_RGB888)
            pixmap = QtGui.QPixmap.fromImage(QImg)

            self.lb.setPixmap(pixmap)
            self.lb.setCursor(QtCore.Qt.CrossCursor)

            #self.pixmap = QtGui.QPixmap(cali_image)
            #self.calibrate_image.setPixmap(self.pixmap)
            cali_file.truncate(0)
            cali_file.close()

class result(QtWidgets.QMainWindow):
    def __init__(self):
        super(result, self).__init__()
        uic.loadUi('result ver 2.ui', self)

        #button function
        self.back_define_button.clicked.connect(self.back_define_function)
        self.compare_button.clicked.connect(self.compare_function)
        self.accept_button.clicked.connect(self.accept_function)
        #select image function

        self.set_original_image()
        self.set_calibrate_image()

        self.show()

    def back_define_function(self):
        #move back to calibrate window
        widget.setCurrentWidget(window_calibrate)
    def compare_function(self):
        #compare with reference photo
        pass
    def accept_function(self):
        #accept result
        pass
    def set_original_image(self):
        threading.Timer(1.0, self.set_original_image).start()
        result_file = open("temporary/result_original.txt", "r+")
        result_image = result_file.read()

        if os.stat("temporary/result_original.txt").st_size == 0:
            pass
        else:
            self.pixmap = QtGui.QPixmap(result_image)
            self.original_image.setPixmap(self.pixmap)
            result_file.truncate(0)
            result_file.close()

    def set_calibrate_image(self):
        pass

app = QtWidgets.QApplication(sys.argv)

widget=QtWidgets.QStackedWidget()
#main_window=landing_page()

#window_1 = landing_page()
window_landing = landing_page()
window_auto = run_auto()
window_define = define_new_lot()
window_adjust = adjust_lot()
window_select = select_reference()
window_calibrate = calibrate_screen()
window_result = result()

widget.addWidget(window_landing)
widget.addWidget(window_auto)
widget.addWidget(window_define)
widget.addWidget(window_adjust)
widget.addWidget(window_select)
widget.addWidget(window_calibrate)
widget.addWidget(window_result)

widget.setFixedHeight(720)
widget.setFixedWidth(1280)
widget.show()
app.exec_()
