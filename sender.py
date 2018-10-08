import sys
import socket

# for debugging only
DEBUG_MODE = True

# this is the normal print
nprint = print
def print(*args, **kwargs):
    if DEBUG_MODE:
        nprint(*args, **kwargs)

# get a list of arguments, there are should be 14 of them
arguments = sys.argv[1:]
print (arguments)
if (len(arguments) != 14):
    # 14 is ... probably too much
    sys.exit('Usage: python sender.py receiver_host_ip receiver_port file.pdf MWS MSS gamma pDrop pDuplicate pCorrupt pOrder maxOrder pDelay maxDelay seed')
else:
    print('YES')
