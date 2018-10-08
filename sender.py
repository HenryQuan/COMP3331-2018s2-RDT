import sys
import socket

# for debugging only
DEBUG_MODE = True

# this is the normal print
nprint = print
def print(*args, **kwargs):
    if DEBUG_MODE:
        nprint(*args, **kwargs)

def main(): 
    # get a list of arguments, there are should be 14 of them
    arguments = sys.argv[1:]
    print (arguments)
    if (len(arguments) != 14):
        # 14 arguments are ... probably too many
        sys.exit('Usage: python sender.py receiver_host_ip receiver_port file.pdf MWS MSS gamma pDrop pDuplicate pCorrupt pOrder maxOrder pDelay maxDelay seed')
    else:
        host_ip = arguments[0]
        port = arguments[0]
        file_name = arguments[0]
        max_windows_size = arguments[0]
        min_segment_size = arguments[0]
        # for calculation of timeout value
        gamma = arguments[0]

        # From here, they are only used by the PLD module
        pDrop = arguments[0]
        pDup = arguments[0]
        pCorrupt = arguments[0]
        pOrder = arguments[0]
        maxOrder = arguments[0]
        pDelay = arguments[0]
        maxDelay = arguments[0]
        seed = arguments[0]
