//
// Created by howie on 2019/7/30.
//

#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <unistd.h>
#include <arpa/inet.h>
#include <sys/socket.h>
#include <netinet/in.h>


int main(int argc, char *argv[])
{
    unsigned int port = 8080;
    char *server_ip = "192.168.153.1";
    if (argc > 1) { // if has parameter, ip change to it
        server_ip = argv[1];
    }
    if (argc > 2) { // the same as above
        port = atoi(argv[2]);
    }

    int sockfd = socket(AF_INET, SOCK_STREAM, 0); // create socket
    if (sockfd < 0) {
        perror("socket");
        exit(-1);
    }

    // set server address struct
    struct sockaddr_in server_addr;
    memset(&server_addr, 0, sizeof(server_addr));
    server_addr.sin_family = AF_INET;
    server_addr.sin_port = htons(port);
    inet_pton(AF_INET, server_ip, &server_addr.sin_addr);

    // connect to server
    int err_log = connect(sockfd, (struct sockaddr*)&server_addr, sizeof(server_addr));
    if (err_log != 0){
        perror("connect");
        close(sockfd);
        exit(-1);
    }

    char send_buf[1024];
    printf("send data to %s:%d\n", server_ip, port);
    while (1) {
        printf("send:");
        fgets(send_buf, sizeof(send_buf), stdin);

        //send_buf[strlen(send_buf)-1] = 0;
        write(sockfd, send_buf, strlen(send_buf));
        write(sockfd, "\r\n", 3);
    }
    close(send_buf);
    return 0;
}

