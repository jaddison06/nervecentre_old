#include <stdio.h>

int NativeHello(int arg1, char* arg2) {
    printf("Hello, World! %s\n");
    return arg1 * 2;
}