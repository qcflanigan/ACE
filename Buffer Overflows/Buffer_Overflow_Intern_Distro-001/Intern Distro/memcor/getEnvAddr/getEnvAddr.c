#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(int argc, char *argv[]) {

	if (argc <2) {
		printf("Usage: getEnvAddr [Environment Variable]\n");		
	} else {
		printf("Address of %s: %p\n", argv[1], getenv(argv[1]));
	}
	return 0;
}
