cmake_minimum_required(VERSION 3.14)
project(Linux_Network_prog C)

set(CMAKE_C_STANDARD 11)

add_executable(udp-send
        udp_send.c)
add_executable(udp-get
        udp_get.c tcp-client.c)

add_executable(tcp-client
        tcp-client.c)