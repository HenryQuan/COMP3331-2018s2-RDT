import sys

DEBUG_MODE = False

# Debuggin message
nprint = print
def print(*args, **kwargs):
    if DEBUG_MODE:
        nprint(*args, **kwargs)
