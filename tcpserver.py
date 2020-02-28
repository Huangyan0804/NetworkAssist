#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from socket import *
import threading
import time
import random
import queue


def get_host_ip():
    try:
        s = socket(AF_INET, SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception as ret:
        print(ret)


def main():

    ip = get_host_ip()
    port = 8080
    print(ip)
    sock = socket(AF_INET, SOCK_STREAM)
    sock.bind((ip, 8080))

    sock.listen(10)
    sock.accept()
    data = sock.recv(1024)
    print(data)
    sock.close()


if __name__ == '__main__':
    main()
