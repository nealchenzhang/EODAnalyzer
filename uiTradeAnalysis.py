# -*- coding: utf-8 -*
from PyQt4 import QtGui, uic
import sys
# import TradingAnalysis

# qtCreatorFile = "analysisW.ui"
qtCreatorFile = "untitled1.ui"
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

class TradeAnalysis(QtGui.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)

        contract_list = ['AL', 'CU', 'ZN']
        self.lineEdit_contract.setText(str(contract_list))               # 写入交易品种  缺少对接
        # for i in contract_list:
        #     # for j in range(len(contract_list)):
        #     # labelname = get_class('PyQt4.QtGui.QLabel')
        #     # labelname=getattr(labelname,i)
        #     labelname=contract_list[i]
        #     # print labelname
        #     # i=labelname
        #     png= QtGui.QPixmap('/home/linuxll/png/{}.png'.format(i))                      # 载入交易图
        #     labelname.setPixmap(png)
        # 载入资金曲线图
        self.A.setPixmap(QtGui.QPixmap('/home/linuxll/EODAnalyzer/png/A.png'))
        self.AL.setPixmap(QtGui.QPixmap('/home/linuxll/EODAnalyzer/png/AL.png'))
        self.AG.setPixmap(QtGui.QPixmap('/home/linuxll/EODAnalyzer/png/AG.png'))
        self.AU.setPixmap(QtGui.QPixmap('/home/linuxll/EODAnalyzer/png/AU.png'))
        self.CU.setPixmap(QtGui.QPixmap('/home/linuxll/EODAnalyzer/png/CU.png'))
        self.B.setPixmap(QtGui.QPixmap('/home/linuxll/EODAnalyzer/png/B.png'))
        self.BU.setPixmap(QtGui.QPixmap('/home/linuxll/EODAnalyzer/png/BU.png'))
        self.C.setPixmap(QtGui.QPixmap('/home/linuxll/EODAnalyzer/png/C.png'))
        self.CU.setPixmap(QtGui.QPixmap('/home/linuxll/EODAnalyzer/png/CU.png'))
        self.FG.setPixmap(QtGui.QPixmap('/home/linuxll/EODAnalyzer/png/FG.png'))
        self.FU.setPixmap(QtGui.QPixmap('/home/linuxll/EODAnalyzer/png/FU.png'))
        self.HC.setPixmap(QtGui.QPixmap('/home/linuxll/EODAnalyzer/png/HC.png'))
        self.IC.setPixmap(QtGui.QPixmap('/home/linuxll/EODAnalyzer/png/IC.png'))
        self.IF.setPixmap(QtGui.QPixmap('/home/linuxll/EODAnalyzer/png/IF.png'))
        self.J.setPixmap(QtGui.QPixmap('/home/linuxll/EODAnalyzer/png/J.png'))
        self.L.setPixmap(QtGui.QPixmap('/home/linuxll/EODAnalyzer/png/L.png'))
        self.M.setPixmap(QtGui.QPixmap('/home/linuxll/EODAnalyzer/png/M.png'))
        self.NI.setPixmap(QtGui.QPixmap('/home/linuxll/EODAnalyzer/png/NI.png'))
        self.P.setPixmap(QtGui.QPixmap('/home/linuxll/EODAnalyzer/png/P.png'))
        self.PB.setPixmap(QtGui.QPixmap('/home/linuxll/EODAnalyzer/png/PB.png'))
        self.PP.setPixmap(QtGui.QPixmap('/home/linuxll/EODAnalyzer/png/PP.png'))
        self.PVC.setPixmap(QtGui.QPixmap('/home/linuxll/EODAnalyzer/png/PVC.png'))
        self.RB.setPixmap(QtGui.QPixmap('/home/linuxll/EODAnalyzer/png/RB.png'))
        self.RM.setPixmap(QtGui.QPixmap('/home/linuxll/EODAnalyzer/png/RM.png'))
        self.RU.setPixmap(QtGui.QPixmap('/home/linuxll/EODAnalyzer/png/RU.png'))
        self.SN.setPixmap(QtGui.QPixmap('/home/linuxll/EODAnalyzer/png/SN.png'))
        self.SR.setPixmap(QtGui.QPixmap('/home/linuxll/EODAnalyzer/png/SR.png'))
        self.TA.setPixmap(QtGui.QPixmap('/home/linuxll/EODAnalyzer/png/TA.png'))
        self.WR.setPixmap(QtGui.QPixmap('/home/linuxll/EODAnalyzer/png/WR.png'))
        self.Y.setPixmap(QtGui.QPixmap('/home/linuxll/EODAnalyzer/png/Y.png'))
        self.ZN.setPixmap(QtGui.QPixmap('/home/linuxll/EODAnalyzer/png/ZN.png'))

        # self.lineEdit_contractNum.setText( )                            # 写入交易手数
        # self.lineEdit_profit.setText( )                                 # 写入盈亏
        # self.lineEdit_winrate.setText( )                                # 写入胜率'''
if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    window = TradeAnalysis()
    window.show()
    sys.exit(app.exec_())


# import re
# print re.match(r'\[(.*?)\]', "[abc]").groups()[0]
# pngpath = r'/home/linuxll/EODAnalyzer/png'
# os.chdir(pngpath)
# self.pnglist = os.listdir(pngpath)



        # pngAL = QtGui.QPixmap('/home/linuxll/png/AL.png')  # 载入交易图
        # # print pngAL
        # self.AL.setPixmap(pngAL)
        # self.tabWidget.addTab(self.tab, QIcon(QtGui.QPixmap("/home/linuxll/png/AL.png").scaled(129, 38)))

        # png=[0]*3
        # for i in contract_list:
        #     for j in range(len(contract_list)):
        #         # labelname = get_class('PyQt4.QtGui.QLabel')
        #         # # labelname=getattr(labelname,i)
        #         # print labelname
        #         # # i=labelname
        #         png[0]= QtGui.QPixmap('/home/linuxll/png/{}.png'.format(i))                      # 载入交易图
        #         self.AL.setPixmap(png[0])                                # label***换为各个品种标签名
        # 遍历交易的品种list，只为交易的品种建立tab,lab,绘图
        # for i in contract_list:
        #     for j in range(len(contract_list)):
        #         self.tab_new = QtGui.QWidget()
        #         self.tab_new.setObjectName(_fromUtf8(str('tab')+str(contract_list[j])))
            # self.tabWidget.addTab(self.tab, _fromUtf8(""))
            # self.bul_new = QtGui.QLabel(self.tab)
            # self.bul.setGeometry(QtCore.QRect(10, 10, 751, 411))
            # self.bul.setText(_fromUtf8(""))
            # self.bul.setObjectName(_fromUtf8("bul"))


    # def contractquery(self):
# class A(object):
#     def __init__(self, v):
#         self.v = v
#     def __reduce__(self):
#         return (self.__class__, (self.v,))
# def get_class( kls ):
#     parts = kls.split('.')
#     module = ".".join(parts[:-1])
#     m = __import__( module )
#     for comp in parts[1:]:
#         m = getattr(m, comp)
#     return m
#
# def str_to_class(str):
# # #     # return reduce(getattr, str.split("."), sys.modules[__name__])
#     return getattr(sys.modules[__name__], str)
#     def __init__(self):
#         dic={'a':'a1','b':'b1'}
#         for i in dic.keys():
#             setattr(self,i,dic[i])
#         print(self.a)
#         print(self.b)
# t=test()