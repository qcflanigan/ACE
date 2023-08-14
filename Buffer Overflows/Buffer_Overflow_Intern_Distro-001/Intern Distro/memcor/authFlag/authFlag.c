#include <stdio.h>
#include <stdlib.h>
#include <string.h>
int check_authentication();


int main(int argc, char *argv[]) {

	if(check_authentication())
	{
		printf("\n-=-=-=-=-=-=-=-=-=-=-=-=-=-\n");
		printf("      Access Granted.\n");
		printf("-=-=-=-=-=-=-=-=-=-=-=-=-=-\n");
	} 
	else 
	{
		printf("\nAccess Denied.\n");
	}
}


int check_authentication() {
	int auth_flag = 0;
	FILE* filePointer;
	char password_buffer[12] = {'A','A','A','A','A','A',
								'A','A','A','A','A','A',};

	filePointer = fopen("password.txt", "r"); //Open the file to read from it.
	if (filePointer == NULL)	
	{
		printf("\nFailed to open file. Exiting.\n");
		exit(0);
	} else {
		fscanf(filePointer, "%s", password_buffer); //Read the first string from the file.
	}


	//Check password, set flag to 1 if correct
	if(strcmp(password_buffer, "secret") == 0)
		auth_flag = 1;

	return auth_flag;
}


	