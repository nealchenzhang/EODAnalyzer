# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(460, 269)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.layoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.layoutWidget.setGeometry(QtCore.QRect(9, 9, 350, 205))
        self.layoutWidget.setObjectName("layoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.layoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setObjectName("formLayout")
        self.label_sysytemname = QtWidgets.QLabel(self.layoutWidget)
        self.label_sysytemname.setEnabled(False)
        font = QtGui.QFont()
        font.setFamily("Utopia")
        font.setPointSize(14)
        self.label_sysytemname.setFont(font)
        self.label_sysytemname.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_sysytemname.setTextFormat(QtCore.Qt.AutoText)
        self.label_sysytemname.setAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignTop)
        self.label_sysytemname.setObjectName("label_sysytemname")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_sysytemname)
        self.gridLayout.addLayout(self.formLayout, 0, 1, 1, 2)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.lineEdit = QtWidgets.QLineEdit(self.layoutWidget)
        self.lineEdit.setObjectName("lineEdit")
        self.verticalLayout_2.addWidget(self.lineEdit)
        self.comboBox_startdate = QtWidgets.QComboBox(self.layoutWidget)
        self.comboBox_startdate.setObjectName("comboBox_startdate")
        self.verticalLayout_2.addWidget(self.comboBox_startdate)
        self.comboBox_enddate = QtWidgets.QComboBox(self.layoutWidget)
        self.comboBox_enddate.setObjectName("comboBox_enddate")
        self.verticalLayout_2.addWidget(self.comboBox_enddate)
        self.gridLayout.addLayout(self.verticalLayout_2, 3, 2, 1, 1)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_investname = QtWidgets.QLabel(self.layoutWidget)
        self.label_investname.setEnabled(False)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_investname.setFont(font)
        self.label_investname.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_investname.setAlignment(QtCore.Qt.AlignCenter)
        self.label_investname.setObjectName("label_investname")
        self.verticalLayout.addWidget(self.label_investname)
        self.label_filepath = QtWidgets.QLabel(self.layoutWidget)
        self.label_filepath.setEnabled(False)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_filepath.setFont(font)
        self.label_filepath.setMouseTracking(False)
        self.label_filepath.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        self.label_filepath.setAlignment(QtCore.Qt.AlignCenter)
        self.label_filepath.setObjectName("label_filepath")
        self.verticalLayout.addWidget(self.label_filepath)
        self.label_starttime = QtWidgets.QLabel(self.layoutWidget)
        self.label_starttime.setEnabled(False)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_starttime.setFont(font)
        self.label_starttime.setAlignment(QtCore.Qt.AlignCenter)
        self.label_starttime.setObjectName("label_starttime")
        self.verticalLayout.addWidget(self.label_starttime)
        self.label_endtime = QtWidgets.QLabel(self.layoutWidget)
        self.label_endtime.setEnabled(False)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_endtime.setFont(font)
        self.label_endtime.setAlignment(QtCore.Qt.AlignCenter)
        self.label_endtime.setObjectName("label_endtime")
        self.verticalLayout.addWidget(self.label_endtime)
        self.gridLayout.addLayout(self.verticalLayout, 3, 0, 1, 2)
        self.pushButton_analysis = QtWidgets.QPushButton(self.layoutWidget)
        self.pushButton_analysis.setObjectName("pushButton_analysis")
        self.gridLayout.addWidget(self.pushButton_analysis, 4, 2, 1, 1)
        self.pushButton_assetdetail = QtWidgets.QPushButton(self.layoutWidget)
        self.pushButton_assetdetail.setObjectName("pushButton_assetdetail")
        self.gridLayout.addWidget(self.pushButton_assetdetail, 4, 0, 1, 2)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.menuBar = QtWidgets.QMenuBar(MainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 460, 26))
        self.menuBar.setObjectName("menuBar")
        MainWindow.setMenuBar(self.menuBar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label_sysytemname.setText(_translate("MainWindow", "投顾复盘系统 V1.0"))
        self.label_investname.setText(_translate("MainWindow", "投顾名："))
        self.label_filepath.setText(_translate("MainWindow", "保证金监控中心文件路径："))
        self.label_starttime.setText(_translate("MainWindow", "开始时间："))
        self.label_endtime.setText(_translate("MainWindow", "结束时间："))
        self.pushButton_analysis.setText(_translate("MainWindow", "分析"))
        self.pushButton_assetdetail.setText(_translate("MainWindow", "资金明细"))

