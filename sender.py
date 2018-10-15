'''

'''
import sys
import socket
from debug import *
from packet import *

def main():
    # get a list of arguments, there are should be 14 of them
    arguments = sys.argv[1:]
    print (arguments)
    if (len(arguments) > 14):
        # 14 arguments are ... probably too many
        fatal('Usage: python sender.py receiver_host_ip receiver_port file.pdf MWS MSS gamma pDrop pDuplicate pCorrupt pOrder maxOrder pDelay maxDelay seed')
    else:
        host_ip = arguments[0]
        port = int(arguments[1])
        '''
        file_name = arguments[2]
        max_windows_size = arguments[3]
        min_segment_size = arguments[4]
        # for calculation of timeout value
        gamma = arguments[5]

        # From here, they are only used by the PLD module
        pDrop = double(arguments[6])
        if (pDrop < 0.0 && pDrop > 1.0) fatal('Invalid pDrop')

        pDup = double(arguments[7])
        if (pDrop < 0.0 && pDrop > 1.0) fatal('Invalid pDup')

        pCorrupt = double(arguments[8])
        if (pDrop < 0.0 && pDrop > 1.0) fatal('Invalid pCorrupt')

        pOrder = double(arguments[9])
        if (pDrop < 0.0 && pDrop > 1.0) fatal('Invalid pOrder')

        maxOrder = int(arguments[10])
        if (pDrop < 0 && pDrop > 6) fatal('Invalid maxOrder')

        pDelay = double(arguments[11])
        if (pDrop < 0.0 && pDrop > 1.0) fatal('Invalid pDelay')

        maxDelay = arguments[12]
        seed = arguments[13]
        '''

        # setting up socket server
        sender = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        three_way_handshake(sender, host_ip, port)
        # update this to get proper timeout
        # sender.settimeout(gamma)

        print('Completed ^_^')

# for connection establishment, NO PAYLOAD (data)
def three_way_handshake(sender, host_ip, port):
    packet = new_packet()
    sender.sendto(bytes(packet), (host_ip, port))
    print(time_now(), 'Handshake #1')

# perform RDT
def reliable_data_transfer():
    return

# four-segment connection termination (FIN, ACK, FIN, ACK)
def termination():
    return

# run everything
main()
