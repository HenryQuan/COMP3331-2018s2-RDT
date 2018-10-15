"""

"""
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
    # get a list of arguments, there are should be only 2 of them
    arguments = sys.argv[1:]
    print (arguments)
    if (len(arguments) != 2):
        # 14 arguments are ... probably too many
        sys.exit('Usage: python receiver.py receiver_port file_r.pdf')
    else:
        receiver_port = arguments[0]
        file_received = arguments[1]

        client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        client.sendto("Hello World", (host_ip, receiver_port))

# dont forget to run the function
main()
