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
	FILE* filePointer;
	char dataBuffer[20] = {'\0'};
	
	printf("Sorry, no address hint.");

	printf("Press any key to read from ");
	printf(fileName);

	getchar(); //Get key from user and discard

	filePointer = fopen(fileName, "r"); //Open the file to read from it.
	if (filePointer == NULL)	
	{
		printf("\nFailed to open file. Exiting.\n");
		exit(0);
	} else {

		fscanf(filePointer, "%s", dataBuffer); //Read the first string from the file.
	}
	
	printf("File contents: \n"); //Display file contents.
	printf(dataBuffer);
	printf("\n");

	return;	
}