import sys, os
import datetime

DEBUG_MODE = True
LOG_FILE = 'stp.log'

STARTING_TIME = None

# Debugging message
nprint = print
def print(*args, **kwargs):
    if DEBUG_MODE:
        nprint(*args, **kwargs)

# start is the starting time to get pure transmission time
def log(message):
    # update time when first called
    global STARTING_TIME
    if (STARTING_TIME is None):
        STARTING_TIME = datetime.datetime.now()

    m = '- {0} --- {1}\n'.format(time_diff(STARTING_TIME), message)
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
