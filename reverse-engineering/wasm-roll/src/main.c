#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>
#include <time.h>
#include <emscripten/emscripten.h>

static bool log_stored = false;

static void init() {
    if (!log_stored) {
        EM_ASM({
            Module.roll = () => {
                Module.ccall('f_af9a16d2279f483ab0687076b7badd6c', 'void', [], []);
            }
        });
        log_stored = true;
    }
    return;
}

static void print_flag() {
    int flag[] = {
         77,  89,  87,  90,  80,  79,  93,  94,  59,  61, 
        133,  62,  82,  62, 105,  62,  88,  58, 126,  82, 
         61,  92, 105,  58,  88,  61, 105,  58,  80, 105, 
        126,  82,  61, 125,  61, 105,  62,  82,  62, 105, 
         61, 114,  61, 105, 108,  65,  61,  67,  61, 107, 
         59, 112,  60, 111, 135
    };

    char nyeh[sizeof(flag)] = {};

    for (size_t i = 0; i < sizeof(flag); i++)
    {
        nyeh[i] = flag[i] - 10;
    }

    char addr[20] = {};
    sprintf(addr, "%p", nyeh);

    EM_ASM({
        Module.print("JACKPOT! Here's the address of the flag: " + UTF8ToString($0) + "<br>Roll again?")
    }, addr);
}

void EMSCRIPTEN_KEEPALIVE f_af9a16d2279f483ab0687076b7badd6c() {
    int chance = rand() % 2000;

    if (chance < 1) print_flag();
    else if (chance < 200) {
        EM_ASM({
            Module.print("You win! But you get nothing. <br>Care to roll again?")
        });
    } else {
        EM_ASM({
            Module.print("You lose! :( <br>Roll again?")
        });
    }
};

int main() {
    srand(time(0));
    init();
}