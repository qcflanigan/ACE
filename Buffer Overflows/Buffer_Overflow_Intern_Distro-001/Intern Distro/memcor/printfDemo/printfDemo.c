#include <stdio.h>
#include <stdlib.h>
#include <string.h>


int main(int argc, char *argv[]) {

	if (argc > 1)
		printf(argv[1]);
	else
		printf("Usage: %s input\n", argv[0]);

	return;
}




