#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <string.h>
#include <arpa/inet.h>

int PORT;
#define LOGLEN 8
#define MAX_ARGS 2
#define MAX_LINE_LENGTH 1024
#define MAX_IP_LENGTH 16  // Maximum length of an IP address (including null terminator)
int MAX_IP_COUNT;  // Maximum number of IP addresses to read from the file
int ENCLAVE_COUNT;

void outputEnclaveInfo(FILE *enclave) {
    fprintf(enclave, "s");
    printf("\nDone\n");
}

int readIPAddressesFromFile(const char* filename, char* ipAddresses[], int maxIPCount) {
    FILE* file = fopen(filename, "r");
    if (file == NULL) {
        perror("Error opening the file");
        return -1;
    }
    char buffer[MAX_IP_LENGTH];
    int ipCount = 0;
    // Read each line in the file until we reach the end or the maximum number of IPs
    while (ipCount < maxIPCount && fgets(buffer, sizeof(buffer), file) != NULL) {
        size_t len = strlen(buffer);
        // Remove the newline character at the end of the line
        if (len > 0 && buffer[len - 1] == '\n') {
            buffer[len - 1] = '\0';
        }
        // Allocate memory for the IP address and copy it to the array
        ipAddresses[ipCount] = (char*)malloc(len + 1); // +1 for null terminator
        if (ipAddresses[ipCount] == NULL) {
            perror("Memory allocation error");
            fclose(file);
            return -1;
        }
        strcpy(ipAddresses[ipCount], buffer);
        ipCount++;
        printf("%s\n", buffer);
    }
    // Close the file
    fclose(file);
    return ipCount;
}

void readEnvVarsFromFile(const char* filename) {
    FILE* file = fopen(filename, "r");
    if (file == NULL) {
        perror("Error opening the file");
        exit(EXIT_FAILURE);
    }

    // Read the first line and store the value in PORT
    if (fscanf(file, "%d", &PORT) != 1) {
        perror("Error reading PORT from the file");
        fclose(file);
        exit(EXIT_FAILURE);
    }

    // Read the second line and store the value in MAX_IP_COUNT
    if (fscanf(file, "%d", &MAX_IP_COUNT) != 1) {
        perror("Error reading MAX_IP_COUNT from the file");
        fclose(file);
        exit(EXIT_FAILURE);
    }

    if (fscanf(file, "%d", &ENCLAVE_COUNT) != 1) {
        perror("Error reading ENCLAVE_COUNT from the file");
        fclose(file);
        exit(EXIT_FAILURE);
    }


    fclose(file);
}

void handleClient(int clientSocket, char* response, char* args, struct sockaddr_in * dest) {
    char destIP[INET_ADDRSTRLEN]; // Buffer to store the IP address string
    uint16_t destPort; // Variable to store the port

    // Convert IP address to a human-readable string
    inet_ntop(AF_INET, &(dest->sin_addr), destIP, INET_ADDRSTRLEN);

    // Convert port number to host byte order
    destPort = ntohs(dest->sin_port);
    send(clientSocket, response, strlen(response), 0);
    printf("Sent: <%s> to <%s:%d>\n", response, destIP, destPort);
    if (strcmp(response, "logs") == 0) {
        int done = 0;
        int logNum = 0;
        char* sizeLogsString = (char*)malloc(999);
        int sizeLogs;
        if (recv(clientSocket, sizeLogsString, 999, 0) < 0) {
            perror("Error receiving size of array of logs");
            free(sizeLogsString);
            exit(1);
        }
        sizeLogs = atoi(sizeLogsString);
        free(sizeLogsString);
        char* logs[sizeLogs][LOGLEN];

        while (done == 0) {
            // Receive six strings from the client socket and store them in the receivedData array
            char** tempArray = (char**)malloc(LOGLEN * sizeof(char*));
            for (int i = 0; i < LOGLEN; i++) {
                tempArray[i] = (char*)malloc(999 * sizeof(char));
            }

            for (int i = 0; i < LOGLEN; i++) {
                char* temp = (char*)malloc(999);
                int success = recv(clientSocket, temp, 999, 0);
                if (success <= 0) {
                    perror("Error receiving data from client");
                    close(clientSocket);
                    free(temp);
                    return;
                }
                temp[success] = '\0';
                printf("%d bytes - %s\n", success, temp);
                if (i == 0 && strcmp(temp, "done") == 0) {
                    done = 1;
                    free(temp);
                    close(clientSocket);
                    free(tempArray);
                    return;
                }
                if (send(clientSocket, "next", strlen("next"), 0) < 0) {
                    perror("Failed to send next");
                    close(clientSocket);
                    free(temp);
                    return;
                }
                strcpy(tempArray[i], temp);
                free(temp);
            }
            /*
            for (int i = 0; i < 6; i++) {
                strncpy(logs[logNum][i], tempArray[i], strlen(tempArray[i]) + 1);
                free(tempArray[i]);
            }
            */
            FILE* file = fopen("allLogs.txt", "a");
            if (file == NULL) {
                perror("Error opening the file");
                exit(EXIT_FAILURE);
            }
            for (int i = 0; i < LOGLEN; i++) {
                printf("%s\t", tempArray[i]);
                if (i == 0) {
                    fprintf(file, "%s", tempArray[i]);
                } else {
                    fprintf(file, "|%s", tempArray[i]);
                }
            }
            fprintf(file, "\n");        
            fclose(file);

            free(tempArray);

            printf("\n");
            // Send "ack" to the client socket
            if (send(clientSocket, "ack", strlen("ack"), 0) < 0) {
                perror("Error sending acknowledgment to client");
                close(clientSocket);
                return;
            }
            logNum++;
        }
    } else if (strcmp(response, "download") == 0) {   
        char* temp = (char*)malloc(4);
        if (recv(clientSocket, temp, sizeof(temp), 0) < 0) {
            perror("Error receiving size of array of logs");
            free(temp);
            exit(1);
        }
        free(temp);
        if (send(clientSocket, args, strlen(args), 0) < 0) {
            perror("Error sending url to client");
            close(clientSocket);
            exit(1);
        }
    }
    close(clientSocket);
    printf("Socket closed\n");
}

// Function to remove a string from a string array
char** removeStringFromArray(char* array[], int* size, char* target) {
    int newSize = *size;
    for (int i = 0; i < *size; i++) {
        if (strcmp(array[i], target) == 0) {
            // Found the target string, remove it from the array
            for (int j = i; j < *size - 1; j++) {
                array[j] = array[j + 1];
            }
            newSize--;
            break; // Exit loop since we found and removed the string
        }
    }
    *size = newSize;
    return array;
}

int isStringInArray(char* array[], int size, char* target) {
    for (int i = 0; i < size; i++) {
        if (strcmp(array[i], target) == 0) {
            array[i] = "";
            return 1; // String found in the array
        }
    }
    return 0; // String not found in the array
}

int main(int argc, char *argv[]) {
    
    int IPCount = 10000;
    const char* title =
    "\n"
    " ██████  ██████  ███    ██      ██ ██    ██ ██████  ███████ \n"
    "██      ██    ██ ████   ██      ██ ██    ██ ██   ██ ██      \n"
    "██      ██    ██ ██ ██  ██      ██ ██    ██ ██████  █████   \n"
    "██      ██    ██ ██  ██ ██ ██   ██ ██    ██ ██   ██ ██      \n"
    " ██████  ██████  ██   ████  █████   ██████  ██   ██ ███████ \n"
    "                                                            \n";

    printf("%s", title);
    printf("===========================================================\n\n\n\n");

    if (argc == 1 || strcmp(argv[1],"--help") == 0 || strcmp(argv[1],"-h") == 0) {
        printf("usage: [OPTION]\n");
        printf("Give instructions to all simulated Users on the network\n\n");
        printf(" -h, --help\tview valid command line arguments\n");
        printf(" -p, --pause\tpause all user simulations\n");
        printf(" -c, --continue\tcontinue all paused user simulations\n");
        printf(" -l, --logs\tquery all user simulations for a log of events\n");
        printf(" -e, --end\tend all user simulations and query them for logs\n");

        printf("\nusage: [OPTION] [PARAMETER]\n");
        printf(" -i, --maxip [max_ip_number]\tset the max number of IPs to PARAMETER\n");
        printf(" -l, --port [port]\t\tset the socket port to PARAMETER\n");
        printf(" -n, --enclaves [count]\t\tspecify the number of enclaves\n");
        printf(" -d, --download [VM_IP] [url]\tdownload from a specific website\n");
        return 0;
    } else {
        readEnvVarsFromFile("envvar.txt");
    }    

    char* ipAddresses[MAX_IP_COUNT];
    

    int serverSocket, clientSocket;
    struct sockaddr_in serverAddr, clientAddr;
    socklen_t clientAddrLen = sizeof(clientAddr);

    // Create a socket
    serverSocket = socket(AF_INET, SOCK_STREAM, 0);
    if (serverSocket < 0) {
        perror("Error creating socket");
        exit(1);
    }

    //const char* ipAddress = "192.168.12.252";
    
    // Set the SO_REUSEADDR option to allow immediate reuse of the address
    int reuse = 1;
    if (setsockopt(serverSocket, SOL_SOCKET, SO_REUSEADDR, &reuse, sizeof(reuse)) < 0) {
        perror("Error setting socket options");
        exit(1);
    }

    // Set up the server address
    serverAddr.sin_family = AF_INET;
    serverAddr.sin_port = htons(PORT);
    serverAddr.sin_addr.s_addr = INADDR_ANY;
    //serverAddr.sin_addr.s_addr = inet_pton(AF_INET, ipAddress, &(serverAddr.sin_addr));
    /*
    if (inet_pton(AF_INET, ipAddress, &(serverAddr.sin_addr)) <= 0) {
        perror("Invalid IP address");
        exit(1);
    }
    */
    // Bind the socket to the server address
    int bindError = bind(serverSocket, (struct sockaddr*)&serverAddr, sizeof(serverAddr));
    if (bindError < 0) {
        perror("Error binding");
        printf("Error code [%i]",bindError);
        exit(1);
    }

    // Start listening for connections
    if (listen(serverSocket, 99999999) < 0) {
        perror("Error listening");
        exit(1);
    }

    if (argc == 2) {
        printf("Extracting IP addresses of all VMs\n");
        for (int i = 0; i < ENCLAVE_COUNT; i++) {
            char * filename = (char*) malloc(strlen("enclaveInfo//networkDetails.txt") + sizeof(i));
            sprintf(filename, "enclaveInfo/%d/networkDetails.txt", i);
            IPCount = readIPAddressesFromFile(filename, ipAddresses, MAX_IP_COUNT);
            free(filename);
        }
        if (IPCount <= 0) {
            printf("There are no IPs to connect to");
            exit(1);
        }
        for (int i = 0; i<IPCount; i++) {
            /*
            if (strcmp(argv[1],"--pause") == 0 || strcmp(argv[1],"-p") == 0) {
                clientSocket = accept(serverSocket, (struct sockaddr*)&clientAddr, &clientAddrLen);
                
                //Check if the clientAddress is in the array ipAddresses
                //If it is, remove it from the array and keep running
                //If it is not, continue the for loop to the next value

                if (clientSocket < 0) {
                    perror("Error accepting connection");
                    exit(1);
                }
                // Handle client request
                handleClient(clientSocket, "pause", &clientAddr);
            }
            */
            if (strcmp(argv[1], "--pause") == 0 || strcmp(argv[1], "-p") == 0) {
                clientSocket = accept(serverSocket, (struct sockaddr*)&clientAddr, &clientAddrLen);
                if (clientSocket < 0) {
                    perror("Error accepting connection");
                    exit(1);
                }                
                char clientIp[INET_ADDRSTRLEN];
                inet_ntop(AF_INET, &clientAddr.sin_addr, clientIp, INET_ADDRSTRLEN);
                int sizeArray = IPCount - i - 1;
                if (isStringInArray(ipAddresses, IPCount, clientIp)) {
                    //ipAddresses = strcpy(removeStringFromArray(ipAddresses, &sizeArray, clientIp), ipAddresses);
                    // Handle the client request since it's in the ipAddresses array
                    handleClient(clientSocket, "pause", "", &clientAddr);
                } else {
                    // Client not in the array, continue the loop
                    i--;
                }
            }
            if (strcmp(argv[1],"--continue") == 0 || strcmp(argv[1],"-c") == 0) {
                clientSocket = accept(serverSocket, (struct sockaddr*)&clientAddr, &clientAddrLen);
                if (clientSocket < 0) {
                    perror("Error accepting connection");
                    exit(1);
                }                
                char clientIp[INET_ADDRSTRLEN];
                inet_ntop(AF_INET, &clientAddr.sin_addr, clientIp, INET_ADDRSTRLEN);
                int sizeArray = IPCount - i - 1;
                if (isStringInArray(ipAddresses, IPCount, clientIp)) {
                    //ipAddresses = strcpy(removeStringFromArray(ipAddresses, &sizeArray, clientIp), ipAddresses);
                    // Handle the client request since it's in the ipAddresses array
                    handleClient(clientSocket, "continue", "", &clientAddr);
                } else {
                    // Client not in the array, continue the loop
                    i--;
                }
            }
            if (strcmp(argv[1],"--logs") == 0 || strcmp(argv[1],"-l") == 0) {
                clientSocket = accept(serverSocket, (struct sockaddr*)&clientAddr, &clientAddrLen);
                if (clientSocket < 0) {
                    perror("Error accepting connection");
                    exit(1);
                }                
                char clientIp[INET_ADDRSTRLEN];
                inet_ntop(AF_INET, &clientAddr.sin_addr, clientIp, INET_ADDRSTRLEN);
                int sizeArray = IPCount - i - 1;
                if (isStringInArray(ipAddresses, IPCount, clientIp)) {
                    //ipAddresses = strcpy(removeStringFromArray(ipAddresses, &sizeArray, clientIp), ipAddresses);
                    // Handle the client request since it's in the ipAddresses array
                    handleClient(clientSocket, "logs", "", &clientAddr);
                } else {
                    // Client not in the array, continue the loop
                    i--;
                }
            }
            if (strcmp(argv[1],"--cousin") == 0 || strcmp(argv[1],"-k") == 0) {
                clientSocket = accept(serverSocket, (struct sockaddr*)&clientAddr, &clientAddrLen);
                if (clientSocket < 0) {
                    perror("Error accepting connection");
                    exit(1);
                }                
                char clientIp[INET_ADDRSTRLEN];
                inet_ntop(AF_INET, &clientAddr.sin_addr, clientIp, INET_ADDRSTRLEN);
                int sizeArray = IPCount - i - 1;
                if (isStringInArray(ipAddresses, IPCount, clientIp)) {
                    //ipAddresses = strcpy(removeStringFromArray(ipAddresses, &sizeArray, clientIp), ipAddresses);
                    // Handle the client request since it's in the ipAddresses array
                    handleClient(clientSocket, "cousin", "", &clientAddr);
                } else {
                    // Client not in the array, continue the loop
                    i--;
                }
            }
            if (strcmp(argv[1],"--end") == 0 || strcmp(argv[1],"-e") == 0) {
                clientSocket = accept(serverSocket, (struct sockaddr*)&clientAddr, &clientAddrLen);
                if (clientSocket < 0) {
                    perror("Error accepting connection");
                    exit(1);
                }
                // Handle client request
                handleClient(clientSocket, "end", "", &clientAddr);
            }
        }
    } else if (argc == 3) {
        if (strcmp(argv[1],"--port") == 0 || strcmp(argv[1],"-l") == 0) {
            int temp = atoi(argv[2]); // try convert the input into an integer
            if (temp == 0) {
                printf("Invalid port number: %s\n", argv[2]); // exit if invalid
            } else {
                FILE* file = fopen("envvar.txt", "w");
                if (file == NULL) {
                    perror("Error opening the file\n"); // exit if can't open file
                } else {
                    if (fprintf(file, "%d\n%d\n%d", temp, MAX_IP_COUNT, ENCLAVE_COUNT) < 0) {
                        perror("Failed to write to the file\n"); // exit if error when writing to file
                    } else {
                        printf("Port number successfully changed from %d to %d\n", PORT, temp);
                        PORT = temp;
                    }
                }
                fclose(file);
            }
        } 
        if (strcmp(argv[1],"--maxip") == 0 || strcmp(argv[1],"-i") == 0) {
            int temp = atoi(argv[2]);
            if (temp == 0) {
                printf("Invalid max IP count: %s\n", argv[2]);
            } else {
                FILE* file = fopen("envvar.txt", "w");
                if (file == NULL) {
                    perror("Error opening the file\n");
                } else {
                    if (fprintf(file, "%d\n%d\n%d", PORT, temp, ENCLAVE_COUNT) < 0) {
                        perror("Failed to write to the file\n");
                    } else {
                        printf("Max IP count successfully changed from %d to %d\n", MAX_IP_COUNT, temp);
                        MAX_IP_COUNT = temp;
                    }
                }
                fclose(file);
            }
        }
        if (strcmp(argv[1],"--enclaves") == 0 || strcmp(argv[1],"-n") == 0) {
            int temp = atoi(argv[2]);
            if (temp == 0) {
                printf("Invalid enclave count: %s\n", argv[2]);
            } else {
                FILE* file = fopen("envvar.txt", "w");
                if (file == NULL) {
                    perror("Error opening the file\n");
                } else {
                    if (fprintf(file, "%d\n%d\n%d", PORT, MAX_IP_COUNT, temp) < 0) {
                        perror("Failed to write to the file\n");
                    } else {
                        printf("Enclave count successfully changed from %d to %d\n", ENCLAVE_COUNT, temp);
                        ENCLAVE_COUNT = temp;
                    }
                }
            }
        }
    } else {
        if (strcmp(argv[1],"--download") == 0 || strcmp(argv[1],"-d") == 0) {
            int waiting = 1;
            while (waiting) {
                char* ipAddress = argv[2];
                clientSocket = accept(serverSocket, (struct sockaddr*)&clientAddr, &clientAddrLen);
                if (clientSocket < 0) {
                    perror("Error accepting connection");
                    exit(1);
                }                
                char clientIp[INET_ADDRSTRLEN];
                inet_ntop(AF_INET, &clientAddr.sin_addr, clientIp, INET_ADDRSTRLEN);
                if (strcmp(argv[2], clientIp) == 0) {
                    handleClient(clientSocket, "download", argv[3], &clientAddr);
                    waiting = 0;
                } else {
                    close(clientSocket);
                }
            }
        }
    }
    close(serverSocket);
    return 0;
}