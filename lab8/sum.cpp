#include <iostream>
#include <cassert>


int calcSum(char *arr, int size)
{
    int ones = (1 << 16) - 1;
    short int sum = 0;
    for (int i = 0; i < (size+1)/2; i++) {
        short int cur = arr[2*i];
        if (2*i + 1 < size) cur += arr[2*i+1] << 8;
        sum += cur;
    }

    return ones ^ sum;
}


bool checkSum(char *arr, int size, int expectedSum)
{
    int ones = (1 << 16) - 1;
    short int sum = 0;
    for (int i = 0; i < (size+1)/2; i++) {
        short int cur = arr[2*i];
        if (2*i + 1 < size) cur += arr[2*i+1] << 8;
        sum += cur;
    }

    return sum + expectedSum == ones;
}


void test1()
{
    char arr[4] = {1, 2, 3, 4};
    int sum = calcSum(arr, 4);
    int base = (1 << 8);
    assert(sum == (base-7)*base + base - 5);
    assert(checkSum(arr, 4, sum));
    assert(!checkSum(arr, 4, sum + 1));
}


void test2()
{
    char arr1[4] = {1, 2, 3, 4}, arr2[5] = {1, 0, 0, 0, 1};
    char arr3[5] = {0, 0, 1, 0, 1};
    int sum1 = calcSum(arr1, 4), sum2 = calcSum(arr2, 5);
    int base = (1 << 8);
    assert(sum2 == (base-1)*base + base - 3);
    assert(checkSum(arr2, 5, sum2));
    assert(!checkSum(arr2, 4, sum1));
    assert(checkSum(arr3, 5, sum2));
}


int main()
{
    test1();
    test2();
    return 0;
}
