"""

"""
import sys
import socket
from debug import *
from packet import *

def main():
    # get a list of arguments, there are should be only 2 of them
    arguments = sys.argv[1:]
    print(arguments)
    if (len(arguments) != 2):
        # 14 arguments are ... probably too many
        fatal('Usage: python receiver.py receiver_port file_r.pdf')
    else:
        port = int(arguments[0])
        file = arguments[1]
        host = 'localhost'

        receiver = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        receiver.bind((host, port))
        while True:
            # data will be an array (bytes)
            data, sender = receiver.recvfrom(port)
            print(time_now(), data)

            packet = new_packet()
            #receiver.sendto(bytes(packet), (host, port))

# dont forget to run the function
main()
