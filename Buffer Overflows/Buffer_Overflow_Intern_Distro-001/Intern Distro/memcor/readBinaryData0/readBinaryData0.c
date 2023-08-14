#include <stdio.h>
#include <stdlib.h>
#include <string.h>
void myFunction(char * fileName);

void main(int argc, char* argv[]) {

	if (!(setuid(0)==0))
		printf("\nSetuid failed.\n");

	if (argc == 2)
		myFunction(argv[1]);
	else
		printf("Reads data from a file. Usage: %s [fileName]\n", argv[0]);

	return;
}


void myFunction(char * fileName) {
	char dataBuffer[16] = {'A','A','A','A','A','A','A','A','A','A','A','A','A','A','A','A',};
	FILE* filePointer;


	printf("Press any key to read from ");
	printf(fileName);

	getchar(); //Get key from user and discard

	filePointer = fopen(fileName, "r"); //Open the file to read from it.
	if (filePointer == NULL)	
	{
		printf("\nFailed to open file. Exiting.\n");
		exit(0);
	} else {

		fread(dataBuffer, 1, 400, filePointer); //Read up to 400 bytes or End-of-File, whichever is first.
	}


	printf("File contents: \n"); //Display file contents.
	printf(dataBuffer);

	return;	
}
