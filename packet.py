"""
This is packet manager
"""

import hashlib

# index for header
seq = 0
ack_num = 1
flag = 2
checksum = 3
data = 4

# flags, allow multiple mode together
syn = 0b0001
ack = 0b0010
fin = 0b0100
data_flag = 0b1000

# create a new package
def new_packet():
    header = [
        0,  # sequence number
        0,  # acknowledge
        0,  # flag
        0,  # checksum
        0   # data
    ]
    return header

'''
Sequence number and acknowledgement
'''
def set_seq(packet, number):
    packet[seq] = number

def get_seq(packet):
    return packet[seq]

def set_ack(packet, number):
    packet[ack] = number

def get_ack(packet):
    return packet[ack]

'''
Update and check for packet's flag
'''
def set_syn_flag(packet):
    # set syn flag
    packet[flag] |= syn

def check_syn_flag(packet):
    # check for syn flag
    return packet[flag] & syn == syn

def set_ack_flag(packet):
    # set ack flag
    packet[flag] |= ack

def check_ack_flag(packet):
    # check for syn flag
    return packet[flag] & ack == ack

def set_fin_flag(packet):
    # set ack flag
    packet[flag] |= fin

def check_fin_flag(packet):
    # check for syn flag
    return packet[flag] & fin == fin

'''
Get and set data and checksum
'''
def set_data(packet, file):
    # set data and checksum
    packet[data] = file
    packet[checksum] = calc_checksum(file)

def get_data(packet):
    return packet[data]

def get_checksum(packet):
    return packet[checksum]

def calc_checksum(file):
    if type(file) is str:
        return hashlib.md5(file).hexdigest()
    else:
        return ''
