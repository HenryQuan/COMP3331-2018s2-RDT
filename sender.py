'''
Send data to a certain address:port
It has many guards to enable data is all good
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
        random.seed(int(arguments[13]))

        # Check if file exists
        if (os.path.isfile(file_name)):
            # setting up socket server
            sender = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sender.settimeout(calc_timeout(gamma))
            three_way_handshake(sender, host_ip, port, gamma)

            # start data transfer
            reliable_data_transfer(sender, host_ip, port, gamma, file_name, max_segment_size, max_windows_size,
                pDrop, pDup, pCorrupt, pOrder, maxOrder, pDelay, maxDelay)
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
        log('[S] Handshake #1 - SYN sent')

        # check for response
        response, sender = s.recvfrom(port)
        if (check_syn_flag(response) and check_ack_flag(response)):
            log('[S] Handshake #2 - SYN-ACK received')
            packet = new_packet()
            set_ack_flag(packet)
            s.sendto(bytes(packet), (ip, port))
            log('[S] Handshake #3 - ACK sent')

            # Connection has been established
            log('[S] Connection is established')
            STATE = CONNECTION_ESTABLISHED
        else:
            log('[S] Handshake failure ' + response)
            fatal('Error: failed to handshake')
    except socket.timeout:
        log('[S] Handshake #1 - Timeout')
        # Retry Connection
        three_way_handshake(s, ip, port, gamma)

# perform RDT
def reliable_data_transfer(s, ip, port, gamma, file, segment_size, windows_size, pDrop, pDup, pCorrupt, pOrder, maxOrder, pDelay, maxDelay):
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
        """
        PLD should be able to take care of all these
        • Drop packets
        • Duplicate packets
        • Create bit errors within packets (a single bit error)
        • Transmits out of order packets
        • Delays packets
        """
        window = 0
        #while (window < windows_size):
        # This is for pipeline
        packet = new_packet()
        data = chunks[index]
        set_data(packet, data)
        data_len = len(chunks[index])
        # set seq and ack to enter correct packet is received
        seq = curr
        ack = seq + data_len
        set_seq(packet, seq)
        set_ack(packet, ack)
        if (lucky(pDrop)):
            # drop this packet
            log('[S] Packet dropped')
        elif (lucky(pDup)):
            # send packet twice
            s.sendto(pickle.dumps(packet), (ip, port))
            log('[S] Dup packet sent {0:.2f}% (SEQ {1} - ACK {2})'.format(curr / max * 100, seq, ack))
            try:
                s.settimeout(calc_timeout(gamma))
                response, sender = s.recvfrom(port)
                response = pickle.loads(response)
                # print(response, check_ack_flag(response), get_ack(response), ack)
                if (check_ack_flag(response)):
                    receiver_ack = get_ack(response)
                    log('[S] ACK {0} received'.format(receiver_ack))
                    if (receiver_ack == ack):
                        # data received
                        curr = ack
                        index = get_data_index(curr, segment_size)
                else:
                    log('[S] Corrupted')
            except socket.timeout:
                log('[S] Timeout')
        elif (lucky(pCorrupt)):
            # send some random data
            packet[4] = data + bytes(0)
            set_seq(packet, seq)
            set_ack(packet, ack)
            # make packet bytes object with dumps
            s.sendto(pickle.dumps(packet), (ip, port))

            # show current percentage, 2 decimals
            log('[S] Corrupted Packet sent {0:.2f}% (SEQ {1} - ACK {2})'.format(curr / max * 100, seq, ack))
            # check for response

            try:
                s.settimeout(calc_timeout(gamma))
                response, sender = s.recvfrom(port)
                response = pickle.loads(response)
                # print(response, check_ack_flag(response), get_ack(response), ack)
                if (check_ack_flag(response)):
                    receiver_ack = get_ack(response)
                    log('[S] ACK {0} received'.format(receiver_ack))
                    if (receiver_ack == ack):
                        # data received
                        curr = ack
                        index = get_data_index(curr, segment_size)
                else:
                    log('[S] Corrupted')
            except socket.timeout:
                log('[S] Timeout')
        elif (lucky(pOrder)):
            # send package index + 1
            data = chunks[index + 1]
            data_len = len(data)
            set_data(packet, data)
            set_seq(packet, seq + data_len)
            set_ack(packet, ack + data_len)
            s.sendto(pickle.dumps(packet), (ip, port))

            # show current percentage, 2 decimals
            log('[S] Reordered Packet sent {0:.2f}% (SEQ {1} - ACK {2})'.format(curr / max * 100, seq + data_len, ack + data_len))
            # check for response

            try:
                s.settimeout(calc_timeout(gamma))
                response, sender = s.recvfrom(port)
                response = pickle.loads(response)
                # print(response, check_ack_flag(response), get_ack(response), ack)
                if (check_ack_flag(response)):
                    receiver_ack = get_ack(response)
                    log('[S] ACK {0} received'.format(receiver_ack))
                    if (receiver_ack == ack):
                        # data received
                        curr = ack
                        index = get_data_index(curr, segment_size)
                else:
                    log('[S] Corrupted')
            except socket.timeout:
                log('[S] Timeout')
        else:
            # finally normal
            s.sendto(pickle.dumps(packet), (ip, port))
            log('[S] packet sent {0:.2f}% (SEQ {1} - ACK {2})'.format(curr / max * 100, seq, ack))
            try:
                s.settimeout(calc_timeout(gamma))
                response, sender = s.recvfrom(port)
                response = pickle.loads(response)
                # print(response, check_ack_flag(response), get_ack(response), ack)
                if (check_ack_flag(response)):
                    receiver_ack = get_ack(response)
                    log('[S] ACK {0} received'.format(receiver_ack))
                    if (receiver_ack == ack):
                        # data received
                        curr = ack
                        index = get_data_index(curr, segment_size)
                else:
                    log('[S] Corrupted')
            except socket.timeout:
                log('[S] Timeout')
    # update current state
    STATE = FILE_TRANSFERRED

# four-segment connection termination (FIN, ACK, FIN, ACK)
def termination(s, ip, port, gamma):
    global STATE
    while (STATE != TERMINATION):
        # send fin
        packet = new_packet()
        set_fin_flag(packet)
        s.sendto(pickle.dumps(packet), (ip, port))
        s.settimeout(calc_timeout(gamma))
        log('[S] FIN sent')
        try:
            ack, sender = s.recvfrom(port)
            ack = pickle.loads(ack)
            if (check_ack_flag(ack)):
                log('[S] ACK received')
                fin, sender = s.recvfrom(port)
                if (check_fin_flag(fin)):
                    log('[S] FIN received')
                    # send fin
                    packet = new_packet()
                    set_ack_flag(packet)
                    s.sendto(bytes(packet), (ip, port))
                    # longer timeout to ensure connection is closed
                    s.settimeout(10)
                    log('[S] ACK sent')
                    # TODO: Add timeout here
                    STATE = TERMINATION
                else:
                    log('[S] Packet is corrupted (FIN)')
            else:
                log('[S] Packet is corrupted (ACK)')
        except socket.timeout:
            log('[S] Timeout')

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

# This condition pass ?? percent of the time
def lucky(percentage):
    that_number = random.randint(1, 100)
    range = int(percentage * 100)
    if (that_number <= range):
        return True
    else:
        # Unlucky one like me
        return False

# get index base on sequence number
def get_data_index(size, segment):
    return int(size / segment)

# calculate estimated timeout
def calc_timeout(gamma):
    return EstimatedRTT + gamma * DevRTT

main() # Run sender
