from socket import *
import threading
import time
import random
import queue

msg_queue = queue.Queue(100)


def get_host_ip():
    try:
        s = socket(AF_INET, SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception as ret:
        print(ret)



class TcpClient:
    def __init__(self, ip_address, port):
        super().__init__()
        # 192.168.101.15
        self.status = False
        self.socket = socket(AF_INET, SOCK_STREAM)
        # self.socket.bind((ip_address, int(port)))
        self.dest_addr = (ip_address, int(port))

    def send_msg(self):
        while self.status:
            msg = input("input your message: ")
            self.socket.send(msg.encode('utf-8'))
            time.sleep(0.5)

    def shut_down(self):
        self.socket.close()

    def run(self):
        self.change_status()
        self.socket.connect(self.dest_addr)
        self.send_msg()
        self.shut_down()

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
        # self.socket.setblocking(False)  # 设置非阻塞

    def send_msg(self, dest_ip, dest_port, msg):
        try:
            self.socket.send(msg.encode('utf-8'))
        except Exception as ret:
            print(ret)

    def recv_msg(self):
        self.socket.listen(10)
        while self.status:
            try:
                dest_socket, dest_ip = self.socket.accept()
                while True:
                    try:
                        msg = dest_socket.recv(1024)
                        # print(msg)
                        if msg:
                            msg_queue.put_nowait((msg, dest_ip))
                        else:
                            break
                    except Exception as ret:
                        # print(ret)
                        pass
            except Exception as ret:
                # print(ret)
                pass

    def run(self, my_ip, my_port):
        self.socket.bind((my_ip, int(my_port)))
        self.change_status()
        self.Trecv_msg.start()

    def shut_down(self):
        self.socket.close()

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
                msg_queue.put_nowait(data)
                # print(self.msg_queue)
                print(data)
            except BlockingIOError:
                pass

    def run(self, my_ip, my_port):
        self.socket.bind((my_ip, int(my_port)))
        self.change_status()
        self.Trecv_msg.start()

    def change_status(self):
        self.status = not self.status

    def shut_down(self):
        self.socket.close()


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
