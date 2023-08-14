#include <stdio.h>
#include <unistd.h>
#include <sys/types.h>
#include <stdio.h>
#include <stdlib.h>

void main(int argc, char *argv[])
{
	char buffer[16];

	printf("Address of buffer on stack: %p\n", &buffer);

	return;
}
