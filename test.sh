#!/bin/bash

type=.pdf

if [ $1 == "s" ]; then
    py sender.py 127.0.0.1 8080 "PDF/Test/test0$type" 10 1000 2 0.8 0.8 0.8 0.8 4 0.8 1000 680
elif [ $1 == "r" ]; then
    py receiver.py 8080 "test$type"
fi
