"""
PLD should be able to take care of all these
• Drop packets
• Duplicate packets
• Create bit errors within packets (a single bit error)
• Transmits out of order packets
• Delays packets
"""
import random

# Emulate real life environment, too many arguments...
def sender_in_real_life(s, ip, host, time, seed, pDrop, pDup, pCorrupt, pOrder, maxOrder, pDelay, maxDelay):


# This condition pass ?? percent of the time
def lucky(percentage):
    that_number = random.randint(1, 100)
    range = int(percentage * 100)
    if (that_number <= range):
        return True
    else:
        # Unlucky one like me
        return False
