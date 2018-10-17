'''

'''
import sys, os, random
import pickle
import socket
from debug import *
from packet import *

# sender states
SYSTEM_INIT = 0
THREE_WAY_HANDSHAKE = 1
CONNECTION_ESTABLISHED = 2
FILE_TRANSFERRED = 3
TERMINATION = 4

# some global values
EstimatedRTT = 0.5
DevRTT = 0.25

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
        max_windows_size = int(arguments[3])
        max_segment_size = int(arguments[4])
        # for calculation of timeout value
        gamma = float(arguments[5])

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

        # set the seed
        random.seed(int(arguments[13]))

        # Check if file exists
        if (os.path.isfile(file_name)):
            # setting up socket server
            sender = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            three_way_handshake(sender, host_ip, port)

            # start data transfer
            reliable_data_transfer(sender, host_ip, port, file_name, max_segment_size, max_windows_size)

            print('Completed ^_^')
        else:
            fatal(file_name + ' is not found')

# for connection establishment, NO PAYLOAD (data)
def three_way_handshake(s, ip, port):
    global STATE
    packet = new_packet()
    set_syn_flag(packet)
    s.settimeout(calc_timeout())
    try:
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
    except Exception:
        log('! Handshake #1 - Timeout')
        # Retry Connection
        three_way_handshake(s, ip, port)

# perform RDT
def reliable_data_transfer(s, ip, port, file, segment_size, windows_size):
    global STATE

    # get the size of file
    max = os.path.getsize(file)
    print(max)
    # get array for chunks
    chunks = cut_into_chunks(file, segment_size)

    curr = 0
    index = 0
    # keep sending data until file is transferred
    while (curr < max):
        packet = new_packet()
        set_data(packet, chunks[index])
        # make packet bytes object with dumps
        s.sendto(pickle.dumps(packet), (ip, port))
        s.settimeout(calc_timeout())
        # show current percentage, 2 decimals
        log('! Packet sent {0:.2f}%'.format(curr / max * 100))
        # check for response
        try:
            response, sender = s.recvfrom(port)
            if (check_ack_flag(response)):
                curr += segment_size
                index += 1
        except Exception:
            log('! Timeout')

    # update current state
    STATE = FILE_TRANSFERRED


# four-segment connection termination (FIN, ACK, FIN, ACK)
def termination():
    return

# cut the file into smaller chunks
def cut_into_chunks(file, size):
    data = open(file, 'rb')
    chunks = []
    # start reading from data
    while True:
        chunk = data.read(size)
        # chunk is not defined or 0 length
        if not chunk or len(chunk) is 0:
            break
        else:
            chunks.append(chunk)

    return chunks

# calculate estimated timeout
def calc_timeout():
    return EstimatedRTT + 4 * DevRTT


main() # Run sender
