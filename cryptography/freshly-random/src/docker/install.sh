#!/bin/sh

# This function will check that the content is
# for python module installation or
# just list of binary file
check_style()
{
    CONTENT="$(cat $1)"
    PTRN=$(expr "$CONTENT" : '\(\#[\ ]*binary\_list\)')
    if [ -z $PTRN ]; then
        RETURN_STYLE="python"
    else
        RETURN_STYLE="binary"
    fi
}

run_install()
{
    if [ "$RETURN_STYLE" = "python" ]; then
        pip3 install -r $1
    else
        while read line; do
            cp $line /home/ctf/$line
        done < $1
    fi
}

if [ $# -eq 1 ]; then
    check_style $1
    run_install $1
elif [ $# -eq 2 ]; then
    check_style $1
    run_install $1

    check_style $2
    run_install $2
else 
    echo "Usage: install.sh FILE1 [FILE2]"
fi