#include <stdio.h>
#include <stdlib.h>
#include <string.h>
int fibonacci (int n);

//Fibonacci Series
// X[n] = X[n-1] + X[n-2], where X[0] = 0 and X[1] = 1
// 0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, ...

void main () {
	int seriesNum;
	int result;

	printf("Calculate Fibonacci series value for N = ");

	scanf("%d", &seriesNum); //Get input from user

	result = fibonacci(seriesNum); //Call the Fibonacci function


	printf("Fibonacci(%d) = %d \n", seriesNum, result); 

	return;
}


int fibonacci (int n) {
	if (n == 0 || n == 1) {
		return n;
	}
	else {
		return fibonacci(n-1) + fibonacci(n-2);
	}

}