#include <stdio.h>
#include <arpa/inet.h>
#include <sys/socket.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <netinet/in.h>

int main(int argc, char *argv[]) {
    unsigned short port = 8080; // server port
    char server_ip[] = "192.168.153.1"; // server ip

    // main pass para
    if (argc > 2) {
        port = atoi(argv[2]);
    }

    int sockfd;
    sockfd = socket(AF_INET, SOCK_DGRAM, 0); // create UDP socket
    if (sockfd < 0) {
        perror("socket"); // print error
        exit(-1);
    }

    // socket addr

    struct sockaddr_in dest_addr;
    bzero(&dest_addr, sizeof(dest_addr)); // clear content
    dest_addr.sin_family = AF_INET;  // ipv4
    dest_addr.sin_port = htons(port); // change port 2 Big-endian
    inet_pton(AF_INET, server_ip, &dest_addr.sin_addr); // set ip
    printf("send data to UDP server %s:%d!\n", server_ip, port);



    char send_buf[1024];
    // while get str
    while (fgets(send_buf, sizeof(send_buf), stdin)) {
        send_buf[strlen(send_buf)-1] = 0;
        // send len
        int len = sendto(sockfd, send_buf, strlen(send_buf), 0, (
        struct sockaddr*)&dest_addr, sizeof(dest_addr));
        printf("len = %d\n", len);
    }
    close(sockfd);
    return 0;
}