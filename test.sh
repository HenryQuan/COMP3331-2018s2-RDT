#!/bin/bash

type=.pdf
p=0.5

input="PDF/Test/test0$type"
output="test$type"

if [ $1 == 'diff' ]; then
    # compare input and output file
    diff "$input" "$output"
else
    # remove log and old output
    rm "$output"
    rm "sender.log" "receiver.log"
    if [ $1 == "s" ]; then
        py sender.py 127.0.0.1 8080 "$input" 10 100 2 $p $p $p $p 6 $p 1000 608
    elif [ $1 == "r" ]; then
        py receiver.py 8080 "$output"
    fi
fi
