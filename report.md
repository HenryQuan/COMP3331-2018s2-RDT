# Report
Python (3.7.0) is the language used for implementation.

## Features
- Stop and Wait

The maximum segment size possible is around 8000(8kb) and any value higher will throw a IOError.

## Header
- Sequence number
- Acknowledgement
- Flags (ACK, SYN, FIN, DATA)
- Checksum
- Payload (data)

Sequence number and acknowledgement are for confirming the transmission and also,
it could prevent incorrect order. Flags are used for checking the type of packet.
Checksum is calculated using hashlib with md5 encryption (32 bits) to check if packet is corrupted.
Payload stores the data and it is cut by the maximum segment size from the original file.

## Design
The main issue with this design is that it is rushed in two weeks. The only goal in mind is too finished this protocol quickly. It has a rather simple header and the header is converted from a list which depends on pickle. If pickle somehow fails, the transmission could not proceed. It also consumes a large amount of ram when transmitting large files (>100M). In this case, a 400MB file is being transmitted.
![It is like Chrome](Memory.png)
