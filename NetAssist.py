#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
    Ubuntu下网络测试工具
    
"""


import sys
from PyQt5 import QtWidgets
from mainwindow import Ui_Form
from TcpUdp_01 import *
import queue
import multiprocessing

# TODO many things
class MyPyQT_Form(QtWidgets.QWidget, Ui_Form):
    def __init__(self):
        super(MyPyQT_Form, self).__init__()
        self.setupUi(self)
        self.Tshow_msg = multiprocessing.Process(target=self.show_msg)
        # self.msg_queue = queue.Queue(100)
        self.socket = UdpClient()
        self.mode = "UDP"
        # self.lineEdit.setText(str())
        # 收/发计数
        self.get_count = 0
        self.send_count = 0

    def dbg(self, xxx):
        """调试控件"""
        self.textEdit.setText(xxx)

    # 实现函数
    def press_send(self):
        """发送数据"""
        data = self.textEdit_2.toPlainText()
        self.textEdit_2.clear()
        # self.dbg(data)
        dest_ip = self.lineEdit_3.text()
        dest_port = self.lineEdit_4.text()
        # 发送数据
        if self.socket.status:
            self.socket.send_msg(dest_ip, dest_port, data)
            self.send_count += 1

    def show_msg(self):
        while self.socket.status:
            if not self.socket.status:
                break
            while not self.socket.msg_queue.empty():
                data = self.socket.msg_queue.get_nowait()
                # 追加文本
                ip_address = str(data[1][0])
                ip_port = str(data[1][1])
                msg = data[0].decode('utf-8')
                self.textEdit.append(ip_address + ':' + ip_port + '发来一条消息：\n' + msg)
                self.get_count += 1

            self.label_5.setText("发送计数：" + str(self.send_count))
            self.label_8.setText("接收计数：" + str(self.send_count))

    def connect2net(self):
        """连接网络"""
        # 获取IP地址和端口
        if not self.socket.status:
            self.chose_mode()
            ip_address = self.lineEdit.text()
            ip_port = self.lineEdit_2.text()
            self.socket.run(ip_address, ip_port)
            try:
                self.Tshow_msg.start()
                print("yes")
            except:
                pass
            self.pushButton_2.setText('断开网络')
        else:
            self.socket.change_status()
            self.socket.shut_down()

            self.pushButton_2.setText('连接网络')
            self.Tshow_msg.terminate()
            print("closed")

        pass

    def chose_mode(self):
        if self.mode == 'UDP':
            self.socket = UdpClient()
            pass
        elif self.mode == 'TCP服务器':
            # self.socket = TcpServer()
            pass
        elif self.mode == 'TCP客户端':
            pass

    def change_mode(self, mode):
        """选择协议模式"""
        self.mode = mode

    def clear_msg(self):
        """清空接收区"""
        self.textEdit.clear()
        pass

    def slot5(self):
        """复位计数"""
        self.get_count = 0
        self.send_count = 0
        pass


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    my_pyqt_form = MyPyQT_Form()
    my_pyqt_form.show()
    sys.exit(app.exec_())
