// compile command: gcc -O0 -o maze-dec -fno-stack-protector -zexecstack maze-dec.c
#include <stdio.h>
#include <time.h>
#include <string.h>
#include <sys/mman.h>

#define CODESIZE 300
int dec_xor(int k, char code[][CODESIZE]) {
    char tmp[CODESIZE];
    for (int i=0;i<CODESIZE;i++){
        tmp[i] = code[k][i] ^ (k & 0xff);
    }

    int (*f) (char[][CODESIZE]) = (void*)tmp;
    return f(code);
}

int dec_flip(int k, char code[][CODESIZE]) {
    char tmp[CODESIZE];
    for (int i=0;i<CODESIZE;i++){
        tmp[i] = code[k][i] ^ 0xff;
    }

    int (*f) (char[][CODESIZE]) = (void*)tmp;
    return f(code);
}

int dec_rev(int k, char code[][CODESIZE]) {
    unsigned char tmp[CODESIZE];
    for (int i=0;i<CODESIZE;i++){
        int cnt = 8;
        int n = code[k][i];
        tmp[i] = code[k][i];
        while(cnt--) {
            tmp[i] = ((tmp[i] << 1) | (n & 1));
            n >>= 1;
        }
    }

    int (*f) (char[][CODESIZE]) = (void*)tmp;
    return f(code);
}

int dec_right(int k, char code[][CODESIZE]) {
    char tmp[CODESIZE];
    int s = k % 8;
    for (int i=0;i<CODESIZE;i++){
        unsigned char n = code[k][i];
        tmp[i] = (n >> (8 - s)) | (n << s) & 0xff;
    }

    int (*f) (char[][CODESIZE]) = (void*)tmp;
    return f(code);
}

int dec_left(int k, char code[][CODESIZE]) {
    char tmp[CODESIZE];
    int s = k % 8;
    for (int i=0;i<CODESIZE;i++){
        unsigned char n = code[k][i];
        tmp[i] = (n >> (s)) | (n << (8 - s)) & 0xff;
    }

    int (*f) (char[][CODESIZE]) = (void*)tmp;
    return f(code);
}

unsigned char code[160][CODESIZE];
unsigned char c1[] = "\xf9\x87\x0f\x7d\xaa\x24\xc4\xf2\x24\xc4\xbe\x74\xe3\xa2\x7c\xff\xff\xff\xff\xe3\xa2\x7e\xe1\x00\x00\x00\xc0\xa2\x7e\x18\x0d\x00\x00\x24\xc5\xa2\x74\x24\x82\xed\x21\x00\x00\xc5\xaa\x7e\x44\x28\x00\x44\x38\x80\xe0\x75\x08\x44\x28\x01\x44\x38\x81\xc0\xa2\x7e\xf1\xca\x00\x00\x24\xc5\xa2\x74\x24\x82\x8f\xac\x00\x00\xc5\xaa\x7e\x44\x28\x00\x44\x38\x80\xe0\x75\x08\x44\x28\x01\x44\x38\x81\xc5\xa2\x7c\xae\xe1";
int main() {
    memset(code, 0, sizeof(code));
    memcpy(code[152], c1, sizeof(c1));
    dec_left(152, code);
    for (int i = 140; i < 155; i++) {
        printf("%d: %d %d %d %d\n", i, code[i][15], code[i][16], code[i][17], code[i][18]);
    }
}