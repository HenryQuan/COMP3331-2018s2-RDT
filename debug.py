import sys, os
import datetime

DEBUG_MODE = True
LOG_FILE = 'stp.log'


# Debugging message
nprint = print
def print(*args, **kwargs):
    if DEBUG_MODE:
        nprint(*args, **kwargs)

# start is the starting time to get pure transmission time
def log(message, start):
    m = '- {0} --- {1}\n'.format(time_diff(start), message)
    print(m)
    log_file = open(LOG_FILE, 'a')
    log_file.write(m)
    log_file.close()

# Fatal error
def fatal(message):
    sys.exit(message)

# Get current system time in a string
def time_diff(start):
    return str(datetime.datetime.now() - start)
