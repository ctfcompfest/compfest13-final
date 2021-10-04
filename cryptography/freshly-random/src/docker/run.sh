#!/bin/sh
ARG=$1
CHALL_BIN=${ARG:-}
if [ -z "${CHALL_BIN}" ]; then
    echo "You didn't set CHALL_BIN environment variable yet."
    exit 0
fi

PTRN=$(expr "$CHALL_BIN" : '\(.*\.py$\)')

if [ -z "${PTRN}" ]; then
    ./$CHALL_BIN
else
    export HOME=/
    export LD_LIBRARY_PATH=/usr/local/lib:$LD_LIBRARY_PATH

    python3 $CHALL_BIN
fi