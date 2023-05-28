#!/bin/bash

[[ -z $1 ]] && echo "You need to provide string as an argument" && exit 1

input=$1

chars=$(echo -n "$input" | wc -c)
words=$(echo -n "$input" | wc -w)
spaces=$(echo -n "$input" | tr -d -c " " | wc -m)
digits=$(echo -n "$input" | sed "s/[^0-9]//g" | wc -c)

printf "%-15s %s\n" "Chars" "$chars"
printf "%-15s %s\n" "Words" "$words"
printf "%-15s %s\n" "Spaces" "$spaces"
printf "%-15s %s\n" "Digits" "$digits"