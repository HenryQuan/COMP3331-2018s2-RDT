import sys
import datetime

DEBUG_MODE = True

# Debugging message
nprint = print
def print(*args, **kwargs):
    if DEBUG_MODE:
        nprint(*args, **kwargs)

# Fatal error
def fatal(message):
    sys.exit(message)

# Get current system time in a string
def time_now():
    return str(datetime.datetime.now())
