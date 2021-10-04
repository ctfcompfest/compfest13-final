#include<stdio.h>
#include<stdlib.h>
#include<string.h>
#include <unistd.h>
#define EMPLOYEECNT 20
#define EMPLOYEENAMELENGTH 24
#define MSGLENGTH 250

struct Employee {
    char name[EMPLOYEENAMELENGTH];
    long bonus;
};

struct Employee employee[EMPLOYEECNT];

int min(int a, int b) {
    return a < b ? a : b;
}

void init() {
    setvbuf(stdout, NULL, _IONBF, 0);

    FILE *fp = fopen("employee.txt", "r");

    if (fp == NULL) {
        perror("Employee databases not found!\n");
        exit(1);
    }

    char ch;
    int now = 0, idx = 0;
    char tmp[EMPLOYEENAMELENGTH + 3];
    memset(tmp, 0, sizeof(tmp));

    while ((ch = fgetc(fp))!= EOF) {
        if (ch == '\n') {
            strncpy(employee[idx].name, tmp, min(strlen(tmp), EMPLOYEENAMELENGTH));
            employee[idx].bonus = 0;
            memset(tmp, 0, sizeof(tmp));
            idx++;
            now = 0;
        } else {
            tmp[now++] = ch;
        }
    }
    fclose(fp);
}

void greetings() {
    puts("Welcome, manager :D");
    puts("You looked tired, please have a seat.");
}

void giveBonus() {
    puts("Woah, you want to give us a bonus? Who will get it?");
    fwrite("> ", 1, 2, stdout);
    char name[EMPLOYEENAMELENGTH];
    read(0, name, EMPLOYEENAMELENGTH);

    puts("How many do you want to give?");
    fwrite("> ", 1, 2, stdout);
    char tmp[16];
    read(0, tmp, 16);
    long bonus = atol(tmp);

    fwrite("You give bonus to all employee named ", 1, 37, stdout);
    puts(name);
    for (int i = 0; i < EMPLOYEECNT; i++) {
        if (strncmp(name, employee[i].name, min(strlen(name), strlen(employee[i].name))) == 0) {
            employee[i].bonus += bonus;
        }
    }
    puts("Thanks Boss :D");
}

void viewEmployee() {
    puts("Who do you want to view the details?");
    char tmp[24];
    read(0, tmp, 24);
    long idx = atol(tmp);
    if (idx < 0) {
        puts("We never have that many employee, Boss.");
        return;
    }
    fwrite("Detail: ", 1, 8, stdout);
    fwrite(&employee[idx], 1, 0x20, stdout);
    puts("");
}

typedef struct {
    char msg[MSGLENGTH];
    FILE *fp;
} thankYouMessage;

void thankYou() {
    puts("A thank-you letter? Nice.");
    fwrite("> ", 1, 2, stdout);
    thankYouMessage _msg;
    _msg.fp = fopen("message.txt", "w+");
    read(0, _msg.msg, 300);
    fwrite(&(_msg.msg), 1, MSGLENGTH, _msg.fp);
}

int menu() {
    puts("\nWhat do you want to do?");
    puts("1. I want to give bonus to the employees");
    puts("2. I want to view details of our employees");
    puts("3. I want to write a thank-you letter for the employees");
    puts("4. Nothing");
    fwrite("> ", 1, 2, stdout);

    char choice[3];
    read(0, choice, 3);
    return atoi(choice);
}

int main() {
    init();
    greetings();
    
    while (1) {
        int choice = menu();
        if (choice == 1) {
            giveBonus();
        } else if (choice == 2) {
            viewEmployee();
        } else if (choice == 3) {
            thankYou();
        } else if (choice == 4) {
            puts("Bye Boss, have a good day.");
            break;
        }
    }
}