#!/bin/bash

type=.pdf
p=0.01

if [ $1 == "s" ]; then
    py sender.py 127.0.0.1 8080 "PDF/Test/test1$type" 10 1000 2 $p $p $p $p 4 $p 1000 68
elif [ $1 == "r" ]; then
    py receiver.py 8080 "test$type"
fi
