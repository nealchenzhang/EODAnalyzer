# -*- coding: utf-8 -*
from PyQt4 import QtGui, uic
import sys

qtCreatorFile = "assetdetailW.ui"
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

class AssetDetail(QtGui.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)

        png = QtGui.QPixmap('/home/linuxll/EODAnalyzer/test.jpg')   # 载入资金曲线图
        self.assetmap.setPixmap(png)

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    window = AssetDetail()
    window.show()
    sys.exit(app.exec_())