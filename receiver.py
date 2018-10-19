"""
Receive data from port and save it as file
It has multiple states and check out of order packet
"""
import sys, pickle
import socket, datetime
from debug import *
from packet import *

# receiver states
SYSTEM_INIT = 0
THREE_WAY_HANDSHAKE = 1
CONNECTION_ESTABLISHED = 2
FIN = 3
TERMINATION = 4

# current state for reveiver
STATE = 0

def main():
    global STATE

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
        STATE = SYSTEM_INIT
        ack = 0

        while (STATE != TERMINATION):
            if (STATE == SYSTEM_INIT):
                # do some setup if necessary
                print('# Reveiver is initialised\n')

            # data will be an array (bytes)
            data, sender = receiver.recvfrom(port)

            # deal with different state
            if (STATE == SYSTEM_INIT):
                # syn from sender for handshake
                if (check_syn_flag(data)):
                    log('# Handshake #1 - SYN received')
                    packet = new_packet()
                    set_syn_flag(packet)
                    set_ack_flag(packet)
                    # 0 is sender ip and 1 is sender port
                    receiver.sendto(bytes(packet), (sender[0], sender[1]))
                    log('# Handshake #2 - SYN-ACK sent')

                    # enter THREE_WAY_HANDSHAKE
                    STATE = THREE_WAY_HANDSHAKE
                    print('# Three way handshake mode entered\n')
            elif (STATE == THREE_WAY_HANDSHAKE):
                # for the final ack
                if (check_ack_flag(data)):
                    log('# Handshake #3 - ACK received')
                    # enter CONNECTION_ESTABLISHED
                    STATE = CONNECTION_ESTABLISHED
                    print('# Connection is now established\n')
            elif (STATE == CONNECTION_ESTABLISHED):
                # check for get_checksum
                data = pickle.loads(data)

                # check for fin
                if (check_fin_flag(data)):
                    log('# FIN received')
                    termination(receiver, sender)
                    STATE = FIN
                    continue

                binary = get_data(data)
                # to check if received correct amount of data
                binary_len = len(binary)
                if (calc_checksum(binary) == get_checksum(data) and get_ack(data) == ack + binary_len):
                    # append to file
                    transferred = open(file, 'ab')
                    transferred.write(binary)
                    transferred.close()

                    log('# Packet received')
                    ack += len(binary)
                    packet = new_packet()
                    set_ack_flag(packet)
                    set_ack(packet, ack)
                    receiver.sendto(pickle.dumps(packet), (sender[0], sender[1]))
                    log('# ACK {0} sent'.format(ack))
                else:
                    packet = new_packet()
                    set_ack_flag(packet)
                    set_ack(packet, ack)
                    receiver.sendto(pickle.dumps(packet), (sender[0], sender[1]))
                    log('# Packet is corrupted, ACK {0}'.format(ack))
            elif (STATE == FIN):
                if (check_ack_flag(data)):
                    # Data is received
                    log('# ACK received, closed')
                    STATE = TERMINATION
                else:
                    # Corrupted
                    log('# Corrupted, retry')
                    termination(receiver, sender)

def termination(receiver, sender):
    # ACK
    packet = new_packet()
    set_ack_flag(packet)
    receiver.sendto(bytes(packet), (sender[0], sender[1]))
    log('# ACK sent')
    # FIN
    packet = new_packet()
    set_fin_flag(packet)
    receiver.sendto(bytes(packet), (sender[0], sender[1]))
    log('# FIN sent')


# dont forget to run the function
main()
print('Thanks for everything. Bye!')
