#include <stdio.h>
#include <arpa/inet.h>
#include <sys/socket.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <netinet/in.h>

#pragma clang diagnostic push
#pragma clang diagnostic ignored "-Wmissing-noreturn"
int main(int argc, char* argv[]) {
    unsigned short port = 8000;
    if (argc > 1) {
        port = atoi(argv[1]);
    }
    int sockfd;
    // create socket
    sockfd = socket(AF_INET, SOCK_DGRAM, 0);

    if (sockfd < 0) {
        perror("socket");
        exit(-1);
    }

    // bind sock address
    struct sockaddr_in my_addr;
    bzero(&my_addr, sizeof(my_addr));
    my_addr.sin_port = htons(port); // change port to big-endian
    my_addr.sin_family = AF_INET;
    my_addr.sin_addr.s_addr = htonl(INADDR_ANY); // bind all ip addresses
    printf("Binding server to port %d\n", port);
    int err_log;
    // binding
    err_log = bind(sockfd, (struct sockaddr*)&my_addr, sizeof(my_addr));
    if (err_log != 0) {
        perror("bind");
        close(sockfd);
        exit(-1);
    }

    printf("receive data...\n");

    while (1) {
        int recv_len;
        char recv_buf[1024];
        struct sockaddr_in client_addr;
        char cli_ip[INET_ADDRSTRLEN];
        socklen_t cliaddr_len = sizeof(client_addr);

        // receive data
        recv_len = recvfrom(sockfd, recv_buf, sizeof(recv_buf), 0, (struct sockaddr*)&client_addr,&cliaddr_len);
        recv_buf[recv_len] = 0;
        inet_ntop(AF_INET,&client_addr.sin_addr, cli_ip, INET_ADDRSTRLEN);
        printf("\nip:%s ,port:%d\n",cli_ip, ntohs(client_addr.sin_port));
        printf("data(%d):%s\n",recv_len,recv_buf);
    }
    close(sockfd);
    return 0;
}
#pragma clang diagnostic pop