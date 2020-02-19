#!/usr/bin/env python
# -*- coding: UTF-8 -*-


import sys
"""
    Ubuntu下网络测试工具
    
"""



from PyQt5 import QtCore, QtGui, QtWidgets

import sys
from PyQt5 import QtWidgets
from mainwindow import Ui_Form


class MyPyQT_Form(QtWidgets.QWidget,Ui_Form):
    def __init__(self):
        super(MyPyQT_Form,self).__init__()
        self.setupUi(self)

    #实现pushButton_click()函数，textEdit是我们放上去的文本框的id
    def slot1(self):
        """发送数据"""
        self.textEdit.setText("你点击了按钮")

    def slot2(self):
        """连接网络"""
        pass

    def slot3(self):
        """选择协议模式"""
        pass

    def slot4(self):
        """清空接收区"""
        pass

    def slot5(self):
        """复位计数"""
        pass


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    my_pyqt_form = MyPyQT_Form()
    my_pyqt_form.show()
    sys.exit(app.exec_())
