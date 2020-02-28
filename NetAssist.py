#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
    Ubuntu下网络测试工具
    
"""


import sys
from PyQt5 import QtWidgets
from mainwindow import Ui_Form
from TcpUdp_01 import *


# TODO many things
class MyPyQT_Form(QtWidgets.QWidget, Ui_Form):
    def __init__(self):
        super(MyPyQT_Form, self).__init__()
        self.setupUi(self)
        my_ip = get_host_ip()
        self.lineEdit.setText(my_ip)
        self.lineEdit_3.setText(my_ip)
        self.Tshow_msg = threading.Thread(target=self.show_msg)
        self.Tshow_msg.setDaemon(True)
        self.Tshow_msg.start()
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
            try:
                self.socket.send_msg(dest_ip, dest_port, data)
                self.send_count += 1
                self.label_5.setText("发送计数：" + str(self.send_count))
            except Exception as ret:
                print(ret)
                pass

    def show_msg(self):
        print("=====threading start=====")
        while True:
            time.sleep(0.2)
            while msg_queue.qsize():
                data = msg_queue.get_nowait()
                print(data)
                # 追加文本
                ip_address = str(data[1][0])
                ip_port = str(data[1][1])
                msg = data[0].decode('utf-8')
                # 只传输非空数据
                if msg:
                    self.textEdit.append('端口' + ip_address + ':' + ip_port +
                                         '(' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                                         + ')：\n->' + msg)
                    self.get_count += 1
                    # 文本框显示到底部
                    self.textEdit.moveCursor(len(self.textEdit.toPlainText())+2)
            self.label_8.setText("接收计数：" + str(self.get_count))
        print("=====threading closed=====")

    def connect2net(self):
        """连接网络"""
        # 获取IP地址和端口
        if not self.socket.status:
            # self.dbg("yes")
            self.chose_mode()
            ip_address = self.lineEdit.text()
            ip_port = self.lineEdit_2.text()
            self.socket.run(ip_address, ip_port)
            self.pushButton_2.setText('断开网络')
            print('connected')
        else:
            self.socket.change_status()
            self.socket.shut_down()
            self.pushButton_2.setText('连接网络')
            print("closed")

        pass

    def chose_mode(self):
        if self.mode == 'UDP':
            self.socket = UdpClient()
            pass
        elif self.mode == 'TCP服务器':
            self.socket = TcpServer()
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
