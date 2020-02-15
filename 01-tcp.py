from socket import *
import threading
import time
import random

class TcpClient(threading.Thread):
    def __init__(self, ip_address, port):
        super().__init__()
        # 192.168.101.15
        self.status = False
        self.tcp_socket = socket(AF_INET, SOCK_STREAM)
        # self.tcp_socket.bind((ip_address, int(port)))
        self.dest_addr = (ip_address, int(port))

    def send_msg(self):
        while self.status:
            msg = input("input your message: ")
            self.tcp_socket.send(msg.encode('utf-8'))
            time.sleep(0.5)

    def shut_down(self):
        self.tcp_socket.shutdown(2)
        self.tcp_socket.close()

    def run(self):
        self.change_status()
        self.tcp_socket.connect(self.dest_addr)
        self.send_msg()
        self.shut_down()

    def change_status(self):
        self.status = not self.status


class TcpServer(threading.Thread):
    def __init__(self, ip_address, port):
        super().__init__()
        # 192.168.101.15
        self.status = False
        self.tcp_socket = socket(AF_INET, SOCK_STREAM)
        self.dest_addr = (ip_address, int(port))
        self.tcp_socket.bind(self.dest_addr)

    def wait_connect(self):
        while self.status:
            dest_socket, dest_ip = self.tcp_socket.accept()
            while True:
                msg = dest_socket.recv(1024).decode('utf-8')
                if msg:
                    print("你有一条消息：" + msg)
                else:
                    break

    def shut_down(self):
        self.tcp_socket.shutdown(2)
        self.tcp_socket.close()

    def run(self):
        self.change_status()
        self.tcp_socket.listen(128)
        self.wait_connect()
        self.shut_down()

    def change_status(self):
        self.status = not self.status


def main():
    ip = '192.168.101.15'
    port = random.randint(5000, 6000)
    t1 = TcpServer(ip, port)
    t2 = TcpClient(ip, port)
    t1.start()
    t2.start()


if __name__ == "__main__":
    main()
