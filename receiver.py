"""

"""
import sys
import socket
from debug import *
from packet import *

# receive should have multiple states
SYSTEM_INIT = 0
THREE_WAY_HANDSHAKE = 1
CONNECTION_ESTABLISHED = 2
TERMINATION = 3

# current state for reveiver
CURR_STATE = 0

def main():
    global CURR_STATE

    # get a list of arguments, there are should be only 2 of them
    arguments = sys.argv[1:]
    print('ARGV:', arguments, '\n')
    if (len(arguments) != 2):
        # 14 arguments are ... probably too many
        fatal('Usage: python receiver.py receiver_port file_r.pdf')
    else:
        port = int(arguments[0])
        file = arguments[1]
        host = 'localhost'

        receiver = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        receiver.bind((host, port))
        # Receiver is now started
        CURR_STATE = SYSTEM_INIT

        while True:
            if (CURR_STATE == SYSTEM_INIT):
                # do some setup if necessary
                print('# Reveiver is initialised\n')

            # data will be an array (bytes)
            data, sender = receiver.recvfrom(port)
            log(data)

            # deal with different state
            if (CURR_STATE == SYSTEM_INIT):
                packet = new_packet()
                receiver.sendto(bytes(packet), (host, port))
                log('ACK #1')

                # update state
                print('# Three way handshake mode entered\n')
                CURR_STATE = THREE_WAY_HANDSHAKE
            elif (CURR_STATE == THREE_WAY_HANDSHAKE):
                return
            elif (CURR_STATE == CONNECTION_ESTABLISHED):
                return
            elif (CURR_STATE == TERMINATION):
                return


# dont forget to run the function
main()
