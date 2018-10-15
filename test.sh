#!/bin/bash

if [ $1 == "s" ]; then
    py sender.py 127.0.0.1 8080
elif [ $1 == "r" ]; then
    py receiver.py 8080 "nothing"
fi
