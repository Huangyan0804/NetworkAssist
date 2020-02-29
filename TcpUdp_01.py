from socket import *
import threading
import time
import random
import queue

msg_queue = queue.Queue(100)
"""
    消息队列格式说明
    (option, msg, (dest_ip. dest_port))
    option : 0 --> 网络消息
             1 --> 锁定目标ip文本框
"""


def get_host_ip():
    """获取本机IP"""
    try:
        s = socket(AF_INET, SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception as ret:
        print(ret)


class TcpClient:
    def __init__(self):
        super().__init__()
        # 192.168.101.15
        self.status = False
        self.socket = socket(AF_INET, SOCK_STREAM)
        # self.socket.bind(('', 8099))
        self.socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)  # 设置端口重复使用
        self.Trecv_msg = threading.Thread(target=self.recv_msg)
        self.Trecv_msg.setDaemon(True)
        self.dest_ip = get_host_ip()
        self.dest_port = 8080
        self.socket.setblocking(False)  # 设置非阻塞

    def send_msg(self, dest_ip, dest_port, msg):
        if not self.status:
            return
        try:
            self.socket.send(str(msg).encode('utf-8'))
        except Exception as ret:
            print('send error: ' + str(ret))

    def recv_msg(self):
        while self.status:
            try:
                msg = self.socket.recv(1024)
                if msg:
                    msg_queue.put_nowait((0, msg, (self.dest_ip, self.dest_port)))
            except Exception as ret:
                # print(ret)
                pass

    def connect_server(self, dest_ip, dest_port):
        try:
            self.socket.connect((dest_ip, int(dest_port)))
            print('connected')
        except Exception as ret:
            print('connect error: ' + str(ret))
            pass
        finally:
            msg_queue.put_nowait((1, '0', (dest_ip, dest_port)))
            print('locket dest addr')

    def run(self, my_ip, my_port, *args):
        self.socket.bind((my_ip, int(my_port)))
        self.change_status()
        self.connect_server(args[0], args[1])
        self.Trecv_msg.start()

    def shut_down(self):
        msg_queue.put_nowait((1, '1', (self.dest_ip, self.dest_port)))
        self.socket.close()
        print("closed")

    def change_status(self):
        self.status = not self.status


class TcpServer:
    def __init__(self):
        super().__init__()
        # 192.168.101.15
        self.status = False
        self.socket = socket(AF_INET, SOCK_STREAM)
        # self.socket.bind(('', 8099))
        self.socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)  # 设置端口重复使用
        self.Trecv_msg = threading.Thread(target=self.recv_msg)
        self.Trecv_msg.setDaemon(True)
        self.socket.setblocking(False)  # 设置非阻塞
        self.dest_socket = get_host_ip()
        self.dest_addr = 8080

    def send_msg(self, dest_ip, dest_port, msg):
        if not self.status:
            return
        try:
            self.dest_socket.send(msg.encode('utf-8'))
        except Exception as ret:
            print(ret)

    def recv_msg(self):
        self.socket.listen(10)
        while self.status:
            try:
                self.dest_socket, self.dest_addr = self.socket.accept()
                msg_queue.put_nowait((1, '0', self.dest_addr))
                while True:
                    try:
                        msg = self.dest_socket.recv(1024)
                        if msg:
                            msg_queue.put_nowait((0, msg, self.dest_addr))
                        else:
                            # 消息为空，说明客户端断开连接，服务器则断开与客户端的连接
                            self.dest_socket.close()
                            msg_queue.put_nowait((1, '0', ('', '')))
                            print("client closed")
                            break
                    except Exception as ret:
                        # print(ret)
                        pass
            except Exception as ret:
                # print(ret)
                pass

    def run(self, my_ip, my_port, *args):
        self.socket.bind((my_ip, int(my_port)))
        self.change_status()
        self.Trecv_msg.start()

    def shut_down(self):
        self.socket.close()
        print("closed")

    def change_status(self):
        self.status = not self.status


class UdpClient:
    def __init__(self):
        super().__init__()
        # 192.168.101.15
        self.status = False
        self.socket = socket(AF_INET, SOCK_DGRAM)
        self.socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)  # 设置端口重复使用
        self.Trecv_msg = threading.Thread(target=self.recv_msg)
        self.Trecv_msg.setDaemon(True)
        self.socket.setblocking(False)  # 设置非阻塞

    def send_msg(self, dest_ip, dest_port, msg):
        try:
            self.socket.sendto(msg.encode('utf-8'), (dest_ip, int(dest_port)))
        except Exception as ret:
            print(ret)

    def recv_msg(self):
        global msg_queue
        while self.status:
            try:
                # data[0]是信息, data[1]是ip信息
                data = self.socket.recvfrom(1024)
                msg_queue.put_nowait(0, data)
                # print(self.msg_queue)
                print(data)
            except BlockingIOError:
                pass

    def run(self, my_ip, my_port, *args):
        self.socket.bind((my_ip, int(my_port)))
        self.change_status()
        self.Trecv_msg.start()

    def change_status(self):
        self.status = not self.status

    def shut_down(self):
        self.socket.close()
        print("closed")


def main():
    ip = get_host_ip()
    port = 8080
    print(ip)
    # socket = UdpClient()
    # socket.run(ip, port)
    # socket.send_msg(ip, port, "hahaha")
    # socket.send_msg(ip, port, "111")
    # socket.change_status()
    # socket.shut_down()

    sock = socket(AF_INET, SOCK_STREAM)
    sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    sock.bind((ip, 8998))
    sock.connect((ip, 8080))
    msg = 'hhhhhh'
    sock.send(msg.encode('utf-8'))
    sock.close()
    # socket.

    sock = socket(AF_INET, SOCK_STREAM)
    sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    sock.bind((ip, 9998))
    sock.connect((ip, 8080))
    msg = 'aaaaaaaaaaaa'
    sock.send(msg.encode('utf-8'))
    sock.close()


if __name__ == "__main__":
    main()
