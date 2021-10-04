#!/usr/bin/env sh
gcc -O0 -o $(basename $1 .c) -zexecstack $1 -lncurses