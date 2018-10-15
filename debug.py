import sys
import datetime

DEBUG_MODE = True

# Debugging message
nprint = print
def print(*args, **kwargs):
    if DEBUG_MODE:
        nprint(*args, **kwargs)

def log(message):
    print('- {0} -\n{1}\n'.format(time_now(), message))

# Fatal error
def fatal(message):
    sys.exit(message)

# Get current system time in a string
def time_now():
    return str(datetime.datetime.now())
