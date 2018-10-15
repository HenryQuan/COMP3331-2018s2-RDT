'''

'''
import sys, os
import socket
from debug import *
from packet import *

# sender states
SYSTEM_INIT = 0
THREE_WAY_HANDSHAKE = 1
CONNECTION_ESTABLISHED = 2
TERMINATION = 3

# current state for sender
STATE = 0

def main():
    # get a list of arguments, there are should be 14 of them
    arguments = sys.argv[1:]
    print ('ARGV:', arguments, '\n')
    if (len(arguments) != 14):
        # 14 arguments are ... probably too many
        fatal('Usage: python sender.py receiver_host_ip receiver_port file.pdf MWS MSS gamma pDrop pDuplicate pCorrupt pOrder maxOrder pDelay maxDelay seed')
    else:
        host_ip = arguments[0]
        port = int(arguments[1])

        file_name = arguments[2]
        max_windows_size = arguments[3]
        min_segment_size = arguments[4]
        # for calculation of timeout value
        gamma = arguments[5]

        # From here, they are only used by the PLD module
        pDrop = float(arguments[6])
        if (pDrop < 0.0 and pDrop > 1.0):
            fatal('Invalid pDrop')

        pDup = float(arguments[7])
        if (pDrop < 0.0 and pDrop > 1.0):
            fatal('Invalid pDup')

        pCorrupt = float(arguments[8])
        if (pDrop < 0.0 and pDrop > 1.0):
            fatal('Invalid pCorrupt')

        pOrder = float(arguments[9])
        if (pDrop < 0.0 and pDrop > 1.0):
            fatal('Invalid pOrder')

        maxOrder = int(arguments[10])
        if (pDrop < 0 and pDrop > 6):
            fatal('Invalid maxOrder')

        pDelay = float(arguments[11])
        if (pDrop < 0.0 and pDrop > 1.0):
            fatal('Invalid pDelay')

        maxDelay = arguments[12]
        seed = arguments[13]

        if (os.path.isfile(file_name)):
            # setting up socket server
            sender = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            three_way_handshake(sender, host_ip, port)
            # update this to get proper timeout
            # sender.settimeout(gamma)

            print('Completed ^_^')
        else:
            fatal(file_name + ' is not found')

# for connection establishment, NO PAYLOAD (data)
def three_way_handshake(s, ip, port):
    global STATE
    packet = new_packet()
    set_syn_flag(packet)
    s.sendto(bytes(packet), (ip, port))
    log('! Handshake #1 - SYN sent')

    # check for response
    response, sender = s.recvfrom(port)
    if (check_syn_flag(response) and check_ack_flag(response)):
        log('! Handshake #2 - SYN-ACK received')
        packet = new_packet()
        set_ack_flag(packet)
        s.sendto(bytes(packet), (ip, port))
        log('! Handshake #3 - ACK sent')
        # Connection has been established
        log('! Connection is established')
        STATE = CONNECTION_ESTABLISHED
    else:
        log('! Handshake failure ' + response)
        fatal('Error: failed to handshake')

# perform RDT
def reliable_data_transfer():
    return

# four-segment connection termination (FIN, ACK, FIN, ACK)
def termination():
    return

# run everything
main()
