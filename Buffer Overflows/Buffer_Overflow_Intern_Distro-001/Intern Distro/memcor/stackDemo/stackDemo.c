#include <stdio.h>
void myFunction(int number1, int number2, int number3);


void main(int argc, char* argv[]) 
{
	int number1 = 1;
	int number2 = 2;
	int number3 = 3;

	printf("Inside main() function\n");

    myFunction (number1, number2, number3); //Call function myFunction(), pass three integers

	printf("Back in main() function\n");    

    return;
}


void myFunction (int number1, int number2, int number3) 
{
    char buffer1[8] = {'A','A','A','A','A','A','A','A', };
    char buffer2[12] = {'B','B','B','B','B','B','B','B','B','B','B','B', };

    printf("Inside myFunction() function.\n");

    return; //Returns to main() 
}

