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
        port = arguments[1]
        file_name = arguments[2]
        max_windows_size = arguments[3]
        min_segment_size = arguments[4]
        # for calculation of timeout value
        gamma = arguments[5]

        # From here, they are only used by the PLD module
        pDrop = arguments[6]
        pDup = arguments[7]
        pCorrupt = arguments[8]
        pOrder = arguments[9]
        maxOrder = arguments[10]
        pDelay = arguments[11]
        maxDelay = arguments[12]
        seed = arguments[13]

# dont forget to run the function
main()