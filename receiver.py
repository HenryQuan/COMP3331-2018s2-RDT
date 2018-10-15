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
        port = int(arguments[0])
        file = arguments[1]

        receiver = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        receiver.bind(('localhost', port))
        while True:
            data, sender = receiver.recvfrom(port)
            print(data)

# dont forget to run the function
main()
