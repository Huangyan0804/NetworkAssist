from socket import *
import multiprocessing
import time
import random
import queue


class TcpClient:
    def __init__(self, ip_address, port):
        super().__init__()
        # 192.168.101.15
        self.status = False
        self.socket = socket(AF_INET, SOCK_STREAM)
        self.socket.setsockopt(SO_REUSEADDR, True)
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
    def __init__(self, ip_address, port):
        super().__init__()
        # 192.168.101.15
        self.status = False
        self.socket = socket(AF_INET, SOCK_STREAM)
        self.socket.setsockopt(SO_REUSEADDR, True)
        self.socket.setblocking(False)
        self.dest_addr = (ip_address, int(port))
        self.socket.bind(self.dest_addr)

    def wait_connect(self):
        while self.status:
            dest_socket, dest_ip = self.socket.accept()
            while True:
                msg = dest_socket.recv(1024).decode('utf-8')
                if msg:
                    print("你有一条消息：" + msg)
                else:
                    break

    def shut_down(self):
        self.socket.close()

    def run(self):
        self.change_status()
        self.socket.listen(128)
        self.wait_connect()
        self.shut_down()

    def change_status(self):
        self.status = not self.status


class UdpClient:
    def __init__(self):
        super().__init__()
        # 192.168.101.15
        self.status = False
        self.socket = socket(AF_INET, SOCK_DGRAM)
        self.socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)  # 设置端口重复使用
        self.Trecv_msg = multiprocessing.Process(target=self.recv_msg)
        self.msg_queue = queue.Queue(100)
    # self.socket.setblocking(False)  # 设置非阻塞

        # 消息队列


    def send_msg(self, dest_ip, dest_port, msg):
        self.socket.sendto(msg.encode('utf-8'), (dest_ip, int(dest_port)))

    def recv_msg(self, msg_queue):
        while self.status:
            data = self.socket.recvfrom(1024)
            # data[0]是信息, data[1]是ip信息
            if data:
                self.msg_queue.put(data)
                print(data)
            else:
                return
            # print(data)
            pass

    def run(self, ip_address, port):
        dest_addr = (ip_address, int(port))
        self.socket.bind(dest_addr)
        self.change_status()
        self.Trecv_msg.start()

    def change_status(self):
        self.status = not self.status

    def shut_down(self):
        # self.Trecv_msg.join()
        self.Trecv_msg.terminate()
        self.socket.close()


def main():
    ip = '127.0.0.1'
    port = 8090
    socket = UdpClient()
    msg_queue = queue.Queue(100)
    socket.run(ip, port, msg_queue)
    socket.send_msg(ip, port, "hahaha")
    socket.change_status()



if __name__ == "__main__":
    main()
