#include <netdb.h>
#include <netinet/in.h>
#include <string.h>
#include <stdio.h>



int fileSEND(char *server, int PORT, char *lfile, char *rfile){


    int socketDESC;
    struct sockaddr_in serverADDRESS;
    struct hostent *hostINFO;
    FILE * file_to_send;
    int ch;
    char toSEND[1];
    char remoteFILE[65536];
    int count1=1,count2=1, percent;


    hostINFO = gethostbyname("localhost");
    if (hostINFO == NULL)
    {
        printf("Problem interpreting host\n");
        return 1;
    }

    socketDESC = socket(AF_INET, SOCK_STREAM, 0);
    if (socketDESC < 0)
    {
        printf("Cannot create socket\n");
        return 1;
    }


    serverADDRESS.sin_family = AF_INET;
    serverADDRESS.sin_port = htons(PORT);
    serverADDRESS.sin_addr = *((struct in_addr *)hostINFO->h_addr_list);


    bzero(&(serverADDRESS.sin_zero),8);


    if (connect(socketDESC, (struct sockaddr *) &serverADDRESS, sizeof(serverADDRESS)) < 0)
    {
        printf("Cannot connect\n");
        return 1;
    }

    file_to_send = fopen (lfile,"r");
    if(!file_to_send)
    {
        printf("Error opening file\n");
        close(socketDESC);
        return 0;
    }
    else
    {
        long fileSIZE;
        fseek (file_to_send, 0, SEEK_END);
        fileSIZE =ftell (file_to_send);
        rewind(file_to_send);

        sprintf(remoteFILE,"FBEGIN:%s:%d\r\n", rfile, fileSIZE);
        send(socketDESC, remoteFILE, sizeof(remoteFILE), 0);

        percent = fileSIZE / 100;
        while((ch=getc(file_to_send))!=EOF)
        {
            toSEND[0] = ch;
            send(socketDESC, toSEND, 1, 0);
            if( count1 == count2 )
            {
                printf("33[0;0H");
                printf( "\33[2J");
                printf("Filename: %s\n", lfile);
                printf("Filesize: %d Kb\n", fileSIZE / 1024);
                printf("Percent : %d%% ( %d Kb)\n",count1 / percent ,count1 / 1024);
                count1+=percent;
            }
       count2++;

        }
    }
   fclose(file_to_send);
   close(socketDESC);

   return 0;

}
int main(int argc, char* argv[])
{

        if(argc!= 3)
        {
            printf("Invalid number of arguments\n");
            printf("Usage:./main program input_image output_image\n");
            exit(1);
        }
        else
        {
            fileSEND("localhost",0x3456, argv[1], argv[2]);
        }
        return 0;
}
