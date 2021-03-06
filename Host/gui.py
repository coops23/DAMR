import sys, vlc, commands
from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(QtGui.QWidget):
    def __init__(self):
        QtGui.QWidget.__init__(self)
        self.setupUi(self)
        self.command = commands.Command(self.frame)
        
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(1130, 614)
        MainWindow.setAutoFillBackground(False)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.gridLayout_4 = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout_4.setObjectName(_fromUtf8("gridLayout_4"))
        self.groupBox_7 = QtGui.QGroupBox(self.centralwidget)
        self.groupBox_7.setObjectName(_fromUtf8("groupBox_7"))
        self.gridLayout_2 = QtGui.QGridLayout(self.groupBox_7)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.frame = QtGui.QFrame(self.groupBox_7)
        self.frame.setMinimumSize(QtCore.QSize(320, 240))
        self.frame.setMaximumSize(QtCore.QSize(320, 240))
        self.frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtGui.QFrame.Raised)
        self.frame.setObjectName(_fromUtf8("frame"))
        self.gridLayout_2.addWidget(self.frame, 0, 0, 1, 1)
        self.videoButton = QtGui.QPushButton(self.groupBox_7)
        self.videoButton.setObjectName(_fromUtf8("videoButton"))
        self.gridLayout_2.addWidget(self.videoButton, 1, 0, 1, 1)
        self.gridLayout_4.addWidget(self.groupBox_7, 0, 0, 1, 1)
        self.groupBox_2 = QtGui.QGroupBox(self.centralwidget)
        self.groupBox_2.setObjectName(_fromUtf8("groupBox_2"))
        self.gridLayout_3 = QtGui.QGridLayout(self.groupBox_2)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.textBrowser = QtGui.QTextBrowser(self.groupBox_2)
        self.textBrowser.setMinimumSize(QtCore.QSize(300, 400))
        self.textBrowser.setMaximumSize(QtCore.QSize(300, 530))
        self.textBrowser.setObjectName(_fromUtf8("textBrowser"))
        self.gridLayout_3.addWidget(self.textBrowser, 0, 0, 1, 1)
        self.gridLayout_4.addWidget(self.groupBox_2, 0, 1, 2, 1)
        self.groupBox = QtGui.QGroupBox(self.centralwidget)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.gridLayout_7 = QtGui.QGridLayout(self.groupBox)
        self.gridLayout_7.setObjectName(_fromUtf8("gridLayout_7"))
        self.mapGraphicsView = QtGui.QGraphicsView(self.groupBox)
        self.mapGraphicsView.setMinimumSize(QtCore.QSize(400, 400))
        self.mapGraphicsView.setMaximumSize(QtCore.QSize(400, 400))
        self.mapGraphicsView.setObjectName(_fromUtf8("mapGraphicsView"))
        self.gridLayout_7.addWidget(self.mapGraphicsView, 0, 0, 1, 1)
        self.testButton = QtGui.QPushButton(self.groupBox)
        self.testButton.setObjectName(_fromUtf8("testButton"))
        self.gridLayout_7.addWidget(self.testButton, 1, 0, 1, 1)
        self.gridLayout_4.addWidget(self.groupBox, 0, 2, 2, 1)
        self.groupBox_3 = QtGui.QGroupBox(self.centralwidget)
        self.groupBox_3.setObjectName(_fromUtf8("groupBox_3"))
        self.gridLayout = QtGui.QGridLayout(self.groupBox_3)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.groupBox_4 = QtGui.QGroupBox(self.groupBox_3)
        self.groupBox_4.setObjectName(_fromUtf8("groupBox_4"))
        self.gridLayout_5 = QtGui.QGridLayout(self.groupBox_4)
        self.gridLayout_5.setObjectName(_fromUtf8("gridLayout_5"))
        self.pushButton = QtGui.QPushButton(self.groupBox_4)
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.gridLayout_5.addWidget(self.pushButton, 0, 0, 1, 1)
        self.spinBox_2 = QtGui.QSpinBox(self.groupBox_4)
        self.spinBox_2.setMaximum(180)
        self.spinBox_2.setObjectName(_fromUtf8("spinBox_2"))
        self.gridLayout_5.addWidget(self.spinBox_2, 0, 1, 1, 1)
        self.gridLayout.addWidget(self.groupBox_4, 0, 0, 1, 1)
        self.groupBox_5 = QtGui.QGroupBox(self.groupBox_3)
        self.groupBox_5.setObjectName(_fromUtf8("groupBox_5"))
        self.gridLayout_8 = QtGui.QGridLayout(self.groupBox_5)
        self.gridLayout_8.setObjectName(_fromUtf8("gridLayout_8"))
        self.distanceButton = QtGui.QPushButton(self.groupBox_5)
        self.distanceButton.setObjectName(_fromUtf8("distanceButton"))
        self.gridLayout_8.addWidget(self.distanceButton, 0, 1, 1, 1)
        self.scanButton = QtGui.QPushButton(self.groupBox_5)
        self.scanButton.setObjectName(_fromUtf8("scanButton"))
        self.gridLayout_8.addWidget(self.scanButton, 1, 1, 1, 1)
        self.gridLayout.addWidget(self.groupBox_5, 0, 1, 1, 1)
        self.groupBox_6 = QtGui.QGroupBox(self.groupBox_3)
        self.groupBox_6.setObjectName(_fromUtf8("groupBox_6"))
        self.gridLayout_9 = QtGui.QGridLayout(self.groupBox_6)
        self.gridLayout_9.setObjectName(_fromUtf8("gridLayout_9"))
        self.forwardButton = QtGui.QPushButton(self.groupBox_6)
        self.forwardButton.setObjectName(_fromUtf8("forwardButton"))
        self.gridLayout_9.addWidget(self.forwardButton, 0, 0, 1, 1)
        self.leftButton = QtGui.QPushButton(self.groupBox_6)
        self.leftButton.setObjectName(_fromUtf8("leftButton"))
        self.gridLayout_9.addWidget(self.leftButton, 0, 1, 1, 1)
        self.movementSpinBox = QtGui.QSpinBox(self.groupBox_6)
        self.movementSpinBox.setMaximum(100)
        self.movementSpinBox.setObjectName(_fromUtf8("movementSpinBox"))
        self.gridLayout_9.addWidget(self.movementSpinBox, 0, 2, 2, 1)
        self.backButton = QtGui.QPushButton(self.groupBox_6)
        self.backButton.setObjectName(_fromUtf8("backButton"))
        self.gridLayout_9.addWidget(self.backButton, 1, 0, 1, 1)
        self.rightButton = QtGui.QPushButton(self.groupBox_6)
        self.rightButton.setObjectName(_fromUtf8("rightButton"))
        self.gridLayout_9.addWidget(self.rightButton, 1, 1, 1, 1)
        self.gridLayout.addWidget(self.groupBox_6, 1, 0, 1, 2)
        self.gridLayout_4.addWidget(self.groupBox_3, 1, 0, 1, 1)
        #MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1130, 25))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        #MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        #MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "Robot", None))
        self.groupBox_7.setTitle(_translate("MainWindow", "Video Stream", None))
        self.videoButton.setText(_translate("MainWindow", "Stream Video", None))
        self.groupBox_2.setTitle(_translate("MainWindow", "Output", None))
        self.groupBox.setTitle(_translate("MainWindow", "Map", None))
        self.testButton.setText(_translate("MainWindow", "Run Test", None))
        self.groupBox_3.setTitle(_translate("MainWindow", "Commands", None))
        self.groupBox_4.setTitle(_translate("MainWindow", "Servo", None))
        self.pushButton.setText(_translate("MainWindow", "Set", None))
        self.groupBox_5.setTitle(_translate("MainWindow", "Ultrasonic Sensor", None))
        self.distanceButton.setText(_translate("MainWindow", "Get Distance", None))
        self.scanButton.setText(_translate("MainWindow", "Scan", None))
        self.groupBox_6.setTitle(_translate("MainWindow", "Movement", None))
        self.forwardButton.setText(_translate("MainWindow", "Forward", None))
        self.leftButton.setText(_translate("MainWindow", "Left", None))
        self.backButton.setText(_translate("MainWindow", "Back", None))
        self.rightButton.setText(_translate("MainWindow", "Right", None))
       
        self.forwardButton.clicked.connect(self.Forward)
        self.backButton.clicked.connect(self.Backward)
        self.leftButton.clicked.connect(self.Left)
        self.rightButton.clicked.connect(self.Right)
        self.distanceButton.clicked.connect(self.Distance)
        self.pushButton.clicked.connect(self.Servo)
        self.videoButton.clicked.connect(self.StreamVideo)
        self.testButton.clicked.connect(self.RunTest)
        self.scanButton.clicked.connect(self.Scan)

    def Print(self, text):
        self.textBrowser.append(text)
        
    def Connect(self):
        self.Print(self.command.Connect())

    def Forward(self):
        self.Print(self.command.Forward(self.movementSpinBox.value()))

    def Backward(self):
        self.Print(self.command.Backward(self.movementSpinBox.value()))

    def Left(self):        
        self.Print(self.command.Left(self.movementSpinBox.value()))

    def Right(self):
        self.Print(self.command.Right(self.movementSpinBox.value()))

    def Distance(self):
        (print_str, distance) = self.command.Distance()
        self.Print(print_str)

    def Scan(self):
        print_str = self.command.Scan()
        self.Print(print_str)
    
    def Servo(self):
        self.Print(self.command.Servo(self.spinBox_2.value()))

    def StreamVideo(self):
        self.videoButton.setText(self.command.StreamVideo())
     
    def RunTest(self):
        generateMap = GenerateMap(self.command)
        GenerateMap.Run(self.command)

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    gui = Ui_MainWindow()
    gui.show()
    sys.exit(app.exec_())
