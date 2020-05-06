import sys
import csv
import os,shutil           
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow,QFileDialog
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt,pyqtSignal
import numpy as np
#from mainWindow import *

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 540)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(538, 460, 93, 28))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(648, 460, 93, 28))
        self.pushButton_2.setObjectName("pushButton_2")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(120, 160, 72, 15))
        self.label.setText("")
        self.label.setObjectName("label")
        self.listWidget_4 = QtWidgets.QListWidget(self.centralwidget)
        self.listWidget_4.setGeometry(QtCore.QRect(600, 160, 141, 231))
        self.listWidget_4.setObjectName("listWidget_4")
        self.listWidget_2 = QtWidgets.QListWidget(self.centralwidget)
        self.listWidget_2.setGeometry(QtCore.QRect(260, 160, 141, 231))
        self.listWidget_2.setObjectName("listWidget_2")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(60, 30, 541, 51))
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(260, 110, 141, 16))
        self.label_5.setObjectName("label_5")
        self.listWidget_3 = QtWidgets.QListWidget(self.centralwidget)
        self.listWidget_3.setGeometry(QtCore.QRect(430, 160, 141, 231))
        self.listWidget_3.setObjectName("listWidget_3")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(120, 300, 72, 15))
        self.label_3.setText("")
        self.label_3.setObjectName("label_3")
        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        self.label_6.setGeometry(QtCore.QRect(430, 110, 141, 16))
        self.label_6.setObjectName("label_6")
        self.listWidget = QtWidgets.QListWidget(self.centralwidget)
        self.listWidget.setGeometry(QtCore.QRect(60, 160, 171, 231))
        self.listWidget.setObjectName("listWidget")
        self.label_7 = QtWidgets.QLabel(self.centralwidget)
        self.label_7.setGeometry(QtCore.QRect(600, 110, 201, 16))
        self.label_7.setObjectName("label_7")
        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(60, 110, 93, 28))
        self.pushButton_3.setObjectName("pushButton_3")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 851, 26))
        self.menubar.setObjectName("menubar")
        self.menuHeusler_AlloysFormation_Prediction = QtWidgets.QMenu(self.menubar)
        self.menuHeusler_AlloysFormation_Prediction.setObjectName("menuHeusler_AlloysFormation_Prediction")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.menubar.addAction(self.menuHeusler_AlloysFormation_Prediction.menuAction())
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton.setText(_translate("MainWindow", "OK"))
        self.pushButton_2.setText(_translate("MainWindow", "Cancel"))
        self.label_4.setText(_translate("MainWindow", "Please enter the cif files of the compounds to be predicted."))
        self.label_5.setText(_translate("MainWindow", "Formation energy :"))
        self.label_6.setText(_translate("MainWindow", "Stability :"))
        self.label_7.setText(_translate("MainWindow", "Likely to exist :"))
        self.pushButton_3.setText(_translate("MainWindow", "Choose"))
        self.menuHeusler_AlloysFormation_Prediction.setTitle(_translate("MainWindow", "Heusler AlloysFormation Prediction"))


class MyWindow(QMainWindow, Ui_MainWindow):
    signal_filename = pyqtSignal(str)
    def __init__(self, parent=None):
        super(MyWindow, self).__init__(parent)
        self.setupUi(self)
        self.initUI()
    def initUI(self):
        self.pushButton_3.clicked.connect(self.openFile)
        self.pushButton.clicked.connect(self.outFile)   
        self.signal_filename.connect(self.showFileName)
        #self.signal_filename.connect(self.showData)
    def openFile(self):
        global fileName
        fileName, filetype = QFileDialog.getOpenFileName(self,
                                                         "选取文件",
                                                         "C:/Users/96913/cgcnn-master/data/heus/",
                                                         "CIF Files (*.cif)")  # 设置文件扩展名过滤,注意用双分号间隔       
        self.signal_filename.emit(fileName)  # 信号发送，括号里面是内容
    def outFile(self):
        l=np.zeros((10, 2), dtype=int)
        x=0
        y=0
        os.system('python predict.py pre-trained/formation-energy.pth.tar data/test')
        with open('C:/Users/96913/cgcnn-master/test_results.csv','r')as f:
          a=csv.reader(f)
          for i, row in enumerate(a):
             if(len(row) < 1):
                continue
             data=row[2]
             self.listWidget_2.addItem(data)
             if(float(data)<1):
                 l[x][0]=1
                 x+=1
             else:
                 l[x][0]=0
                 x+=1
        os.system('python predict.py pre-trained/stability.pth.tar data/test')
        with open('C:/Users/96913/cgcnn-master/test_results.csv','r')as f:
          a=csv.reader(f)
          for i, row in enumerate(a):
             if(len(row) < 1):
                continue
             data=row[2]
             self.listWidget_3.addItem(data)
             if(float(data)>0):
                 l[y][1]=1
                 y+=1
             else:
                 l[y][0]=0
                 y+=1
        a=0
        while a < self.listWidget_3.count():
         if(l[a][0]==1):
            if(l[a][1]==1):
               self.listWidget_4.addItem("Yes")
               a+=1
            else:
               self.listWidget_4.addItem("No")
               a+=1
         else:
            self.listWidget_4.addItem("No")
            a+=1
        #csvFile.close("C:/Users/96913/cgcnn-master/data/test/id_prop.csv")
        os.remove("C:/Users/96913/cgcnn-master/data/test/id_prop.csv")
        
    def showFileName(self, str):
        shutil.copyfile(str, "C:/Users/96913/cgcnn-master/data/test/"+str[-9:])
        csvFile = open("C:/Users/96913/cgcnn-master/data/test/id_prop.csv",'a',newline='')
        writer = csv.writer(csvFile)
        a=[str[-9:-4],"0"]
        writer.writerow(a)
        csvFile.close()
        self.listWidget.addItem(str)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWin = MyWindow()
    myWin.show()
    sys.exit(app.exec_())
