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
    unsigned short port = 12580;
    if (argc > 1) {
        port = atoi(argv[1]);
    }
    int sockfd = socket(AF_INET, SOCK_STREAM, 0);
    if (sockfd < 0) {
        perror("socket");
        exit(-1);
    }
    struct sockaddr_in server_addr;
    memset(&server_addr, 0, sizeof(server_addr));
    server_addr.sin_family = AF_INET;
    server_addr.sin_port = htons(port);
    server_addr.sin_addr.s_addr = htonl(INADDR_ANY);

    // bind
    int error_log = bind(sockfd, (struct sockaddr*)&server_addr, sizeof(server_addr));
    char server_ip[16];
    inet_ntop(AF_INET, &server_addr.sin_addr, server_ip, 16);
    printf("%s\n", server_ip);
    if (error_log != 0) {
        perror("bind");
        exit(-1);
    }

    // listen
    error_log = listen(sockfd, 10); // passive
    if (error_log != 0) {
        perror("listen");
        close(sockfd);
        exit(-1);
    }

    printf("listen client @port = %d...\n", port);

    while(1)
    {

        struct sockaddr_in client_addr;
        char cli_ip[INET_ADDRSTRLEN] = "";
        socklen_t cliaddr_len = sizeof(client_addr);

        int connfd;
        // waiting for connect
        connfd = accept(sockfd, (struct sockaddr*)&client_addr, &cliaddr_len);
        if(connfd < 0)
        {
            perror("accept");
            continue;
        }

        inet_ntop(AF_INET, &client_addr.sin_addr, cli_ip, INET_ADDRSTRLEN);
        printf("----------------------------------------------\n");
        printf("client ip=%s,port=%d\n", cli_ip,ntohs(client_addr.sin_port));

        char recv_buf[512] = "";
        int recv_len = 1;
        while(recv_len > 0) // receive data
        {
            recv_len = recv(connfd, recv_buf, sizeof(recv_buf), 0) ;
            recv_buf[recv_len] = 0;
            printf("receive data: %s\n",recv_buf);
        }

        close(connfd);     // close
        printf("client closed!\n");
    }
    close(sockfd);
    return 0;
}
