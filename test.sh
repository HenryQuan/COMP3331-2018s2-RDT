#!/bin/bash

type=.pdf
p=0.01

input="PDF/Test/test1$type"
output="test$type"

if [ $1 == "s" ]; then
    py sender.py 127.0.0.1 8080 "$input" 10 8000 2 $p $p $p $p 4 $p 1000 68
elif [ $1 == "r" ]; then
    py receiver.py 8080 "$output"
elif [ $1 == 'diff' ]; then
    # compare input and output file
    diff "$input" "$output"
fi
