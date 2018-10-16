#!/bin/bash

if [ $1 == "s" ]; then
    py sender.py 127.0.0.1 8080 PDF/Test/test2.pdf 10 100 2 0.5 0.1 0.1 0.1 4 0.1 1000 473892
elif [ $1 == "r" ]; then
    py receiver.py 8080 "test0.pdf"
fi
