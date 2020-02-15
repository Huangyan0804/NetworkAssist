#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys
"""
    Ubuntu下网络测试工具
    
"""


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.init_window()
        self.init_ui()
        self.show()

    def init_window(self):
        self.resize(800, 600)
        self.center()
        self.setWindowTitle('网络调试助手')

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def init_ui(self):
        self.init_textedit()

    def init_textedit(self):
        te = QTextEdit()
        te.resize(te.sizeHint())
        te.move(100, 100)




def main():
    app = QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()