#include <stdio.h>
#include <stdlib.h>
#include <string.h>
void myFunction ();
void losingFunction();
void winningFunction();

void main() 
{

	myFunction();

	losingFunction();

	winningFunction();
	
	return;
}

void myFunction() 
{
	FILE* filePointer;
	char dataBuffer[8] = {'A','A','A','A','A','A','A','A'};


	filePointer = fopen("input.txt", "r"); //Open the file to read from it.
	if (filePointer == NULL)	
	{
		printf("\nFailed to open file. Exiting.\n");
		return;
	} else {
		
		fscanf(filePointer, "%s", dataBuffer); //Read the first string from the file.
	}


	return;
}

void losingFunction() {
	printf("::: You lose :::\n");
	printf("::: You lose :::\n");
	printf("::: You lose :::\n");
	printf("::: You lose :::\n");
	printf("::: You lose :::\n");

	exit(0); //forced program exit.

	return;
}

void winningFunction() {
	printf("::: You win :::\n");
	printf("::: You win :::\n");
	printf("::: You win :::\n");
	printf("::: You win :::\n");
	printf("::: You win :::\n");

	return;
}
	







//fread(dataBuffer, 1, 40, filePointer); //Read up to 40 bytes or End-of-File, whichever is first.


