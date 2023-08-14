#include <stdio.h>
#include <unistd.h>
#include <sys/types.h>
#include <stdio.h>
#include <stdlib.h>

void main(int argc, char *argv[])
{
	static uid_t ruid;
	ruid = getuid();//Save current user id

	printf("Before setuid:\n");
	system("id"); //print real and effective user and group IDs



	if (!(setuid(0)==0)) 	//Get root(owner) priviledges
		printf("\nSetuid failed.\n");

	printf("\nAfter setuid:\n");
	system("id");

	if (!(setuid(ruid)==0)) 	//Drop priviledges back to user id
		printf("\nSetuid failed.\n");

	printf("\nAfter setuid restore:\n");
	system("id");

	return;
}