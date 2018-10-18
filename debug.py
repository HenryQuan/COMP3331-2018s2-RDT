import sys
import datetime

DEBUG_MODE = True

# Debugging message
nprint = print
def print(*args, **kwargs):
    if DEBUG_MODE:
        nprint(*args, **kwargs)

# start is the starting time to get pure transmission time
def log(message, start):
    print('- {0} -\n{1}\n'.format(time_diff(start), message))

# Fatal error
def fatal(message):
    sys.exit(message)

# Get current system time in a string
def time_diff(start):
    return str(datetime.datetime.now() - start)
