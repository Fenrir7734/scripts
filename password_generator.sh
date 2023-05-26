#!/bin/bash

if [[ "$1" && $1 = "-h" ]]; then
    echo -e "
password_generator.sh [LENGTH] [ALPHABET] [COUNT]

    LENGTH
        lenght of the password to generate
    
    ALPHABET
        characters from which the password will be created. Allowed values: alnum, alpha, digit, punct

    COUNT
        number of passwords to generate
"
    exit 0
fi

LENGTH=${1:-10}

case $2 in
    "alnum"|"alpha"|"digit")
        ALPHABET="[:$2:]"
        ;;
    "punct")
        ALPHABET="[:alnum:][:punct:]"
        ;;
    *)
        ALPHABET="[:alnum:]"
        ;;
esac

COUNT=${3:-1}

for (( i=0; i<=$COUNT; i++ ))
do
    tr -cd $ALPHABET </dev/urandom | head -c$LENGTH
    echo -e \n
done