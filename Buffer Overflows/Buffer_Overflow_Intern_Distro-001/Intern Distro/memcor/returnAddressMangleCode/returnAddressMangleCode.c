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

void myFunction () 
{
	char dataBuffer[8] = {'A','A','A','A','A','A','A','A'};
	int* ret;
	//Set pointer to return address by adding 16 byte offset
	//Note: adds 4*4 due to pointer '+' definition
	ret = &ret + 4; 

	//Overwrite return address with the address of the instruction you want to execute
	(*ret) = 0x08048443; //Update this line

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
