'''

'''
import sys, os, random
import pickle
import socket, datetime
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
STARTING_TIME = datetime.datetime.now()

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
            three_way_handshake(sender, host_ip, port, gamma)

            # start data transfer
            reliable_data_transfer(sender, host_ip, port, gamma, file_name, max_segment_size, max_windows_size)
            # termination
            termination(sender, host_ip, port, gamma)

            print('Completed ^_^\nThank you for using STP')
        else:
            fatal(file_name + ' is not found')

# for connection establishment, NO PAYLOAD (data)
def three_way_handshake(s, ip, port, gamma):
    global STATE
    packet = new_packet()
    set_syn_flag(packet)
    s.settimeout(calc_timeout(gamma))
    try:
        s.sendto(bytes(packet), (ip, port))
        log('! Handshake #1 - SYN sent', STARTING_TIME)

        # check for response
        response, sender = s.recvfrom(port)
        if (check_syn_flag(response) and check_ack_flag(response)):
            log('! Handshake #2 - SYN-ACK received', STARTING_TIME)
            packet = new_packet()
            set_ack_flag(packet)
            s.sendto(bytes(packet), (ip, port))
            log('! Handshake #3 - ACK sent', STARTING_TIME)

            # Connection has been established
            log('! Connection is established', STARTING_TIME)
            STATE = CONNECTION_ESTABLISHED
        else:
            log('! Handshake failure ' + response, STARTING_TIME)
            fatal('Error: failed to handshake')
    except Exception:
        log('! Handshake #1 - Timeout', STARTING_TIME)
        # Retry Connection
        three_way_handshake(s, ip, port, gamma)

# perform RDT
def reliable_data_transfer(s, ip, port, gamma, file, segment_size, windows_size):
    global STATE

    # get the size of file
    max = os.path.getsize(file)
    # print(max)
    # get array for chunks
    chunks = cut_into_chunks(file, segment_size)

    curr = 0
    index = 0
    # keep sending data until file is transferred
    while (curr < max):
        packet = new_packet()
        set_data(packet, chunks[index])
        data_len = len(chunks[index])
        # set seq and ack to enter correct packet is received
        seq = curr
        ack = seq + data_len
        set_seq(packet, seq)
        set_ack(packet, ack)
        # make packet bytes object with dumps
        s.sendto(pickle.dumps(packet), (ip, port))
        s.settimeout(calc_timeout(gamma))
        # show current percentage, 2 decimals
        log('! Packet sent {0:.2f}% (SEQ {1} - ACK {2})'.format(curr / max * 100, seq, ack), STARTING_TIME)
        # check for response
        try:
            response, sender = s.recvfrom(port)
            response = pickle.loads(response)
            # print(response, check_ack_flag(response), get_ack(response), ack)
            if (check_ack_flag(response) and get_ack(response) == ack):
                curr += data_len
                index += 1
            else:
                log('! Corrupted', STARTING_TIME)
        except Exception:
            log('! Timeout', STARTING_TIME)

    # update current state
    STATE = FILE_TRANSFERRED


# four-segment connection termination (FIN, ACK, FIN, ACK)
def termination(s, ip, port, gamma):
    if (STATE == FILE_TRANSFERRED):
        # send fin
        packet = new_packet()
        set_fin_flag(packet)
        s.sendto(pickle.dumps(packet), (ip, port))
        log('! FIN sent', STARTING_TIME)
        s.settimeout(calc_timeout(gamma))
        try:
            ack, sender = s.recvfrom(port)
            # print(response, check_ack_flag(response), get_ack(response), ack)
            if (check_ack_flag(ack)):
                fin, sender = s.recvfrom(port)
                if (check_fin_flag(fin)):
                    # send fin
                    packet = new_packet()
                    set_ack_flag(packet)
                    s.sendto(bytes(packet), (ip, port))
                    log('! ACK sent', STARTING_TIME)
                    # TODO: Add timeout here
                else:
                    log('! Packet is corrupted', STARTING_TIME)
                    termination(s, ip, port, gamma)
            else:
                log('! Packet is corrupted', STARTING_TIME)
                termination(s, ip, port, gamma)
        except Exception:
            log('! Timeout', STARTING_TIME)
            # try again
            termination(s, ip, port, gamma)

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
def calc_timeout(gamma):
    return EstimatedRTT + gamma * DevRTT

main() # Run sender
