"""
Receive data from port and save it as file
It has multiple states and check out of order packet
"""
import sys, pickle, os
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

        max_size = 0
        total = 0
        dup = 0
        corrupted = 0
        reorder = 0

        while (STATE != TERMINATION):
            if (STATE == SYSTEM_INIT):
                # do some setup if necessary
                print('[R] Reveiver is initialised\n')

            # data will be an array (bytes)
            data, sender = receiver.recvfrom(port)

            # deal with different state
            if (STATE == SYSTEM_INIT):
                # syn from sender for handshake
                if (check_syn_flag(data)):
                    log('[R] Handshake #1 - SYN received')
                    packet = new_packet()
                    set_syn_flag(packet)
                    set_ack_flag(packet)
                    # 0 is sender ip and 1 is sender port
                    receiver.sendto(bytes(packet), (sender[0], sender[1]))
                    log('[R] Handshake #2 - SYN-ACK sent')

                    # enter THREE_WAY_HANDSHAKE
                    STATE = THREE_WAY_HANDSHAKE
                    print('[R] Three way handshake mode entered\n')
            elif (STATE == THREE_WAY_HANDSHAKE):
                # for the final ack
                if (check_ack_flag(data)):
                    log('[R] Handshake #3 - ACK received')
                    # enter CONNECTION_ESTABLISHED
                    STATE = CONNECTION_ESTABLISHED
                    print('[R] Connection is now established\n')
            elif (STATE == CONNECTION_ESTABLISHED):
                # check for get_checksum
                data = pickle.loads(data)
                total += 1

                # check for fin
                if (check_fin_flag(data)):
                    log('[R] FIN received')
                    termination(receiver, sender)
                    STATE = FIN
                    continue

                binary = get_data(data)
                # to check if received correct amount of data
                binary_len = len(binary)
                if (calc_checksum(binary) == get_checksum(data)):
                    data_ack = get_ack(data)
                    data_seq = get_seq(data)
                    # print(data_seq, data_ack, ack)
                    if (data_ack == ack + binary_len):
                        # This is what we want, append to file
                        max_size += binary_len
                        transferred = open(file, 'ab')
                        transferred.write(binary)
                        transferred.close()

                        log('[R] Packet received')
                        ack += binary_len
                        packet = new_packet()
                        set_ack_flag(packet)
                        set_ack(packet, ack)
                        receiver.sendto(pickle.dumps(packet), (sender[0], sender[1]))
                        log('[R] ACK {0} sent'.format(ack))
                    elif (data_ack <= ack):
                        dup += 1
                        # dup
                        packet = new_packet()
                        set_ack_flag(packet)
                        set_ack(packet, ack)
                        receiver.sendto(pickle.dumps(packet), (sender[0], sender[1]))
                        log('[R] Duplicate, ACK {0}'.format(ack))
                    elif (data_ack > ack + binary_len):
                        reorder += 1
                        # Reordered data
                        packet = new_packet()
                        set_ack_flag(packet)
                        set_ack(packet, ack)
                        receiver.sendto(pickle.dumps(packet), (sender[0], sender[1]))
                        log('[R] Packet is Reordered, ACK {0}'.format(ack))
                else:
                    corrupted += 1
                    packet = new_packet()
                    set_ack_flag(packet)
                    set_ack(packet, ack)
                    receiver.sendto(pickle.dumps(packet), (sender[0], sender[1]))
                    log('[R] Packet is corrupted, ACK {0}'.format(ack))
            elif (STATE == FIN):
                if (check_ack_flag(data)):
                    # Data is received
                    log('[R] ACK received, closed')
                    STATE = TERMINATION
                else:
                    # Corrupted
                    log('[R] Corrupted, retry')
                    termination(receiver, sender)
        log('[R] STATISTICS\n', time=False)
        log('[R] File size: {0}\n'.format(max_size), False)
        log('[R] Duplicate: {0}\n'.format(dup), False)
        log('[R] Corrupted: {0}\n'.format(corrupted), False)
        log('[R] Reordered: {0}\n'.format(reorder), False)
        log('[R] Total: {0}\n'.format(total), False)

def termination(receiver, sender):
    # ACK
    packet = new_packet()
    set_ack_flag(packet)
    receiver.sendto(pickle.dumps(packet), (sender[0], sender[1]))
    log('[R] ACK sent')
    # FIN
    packet = new_packet()
    set_fin_flag(packet)
    receiver.sendto(pickle.dumps(packet), (sender[0], sender[1]))
    log('[R] FIN sent')


# dont forget to run the function
main()
print('Thanks for everything. Bye!')
