#!/bin/bash

[[ -z $1 ]] && echo "You need to provide string as an argument" && exit 1

echo $1 | awk '{print length}'