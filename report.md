# Report
Python (3.7.0) is the language used for implementation because I think that Python might be the fastest in terms of development but for debugging, it might not be as good as Java and C is too hardcore for me to use.

The maximum segment size possible is around 8000(8kb) and any value higher will throw a IOError from Python.

## Features
- Stop and Wait + Pipeline (Go Back N)
- PLD module (emulate real life environment)
- RDT

## Header
- Sequence number
- Acknowledgement
- Flags (ACK, SYN, FIN, DATA)
- Checksum
- Payload (data)

Sequence number and acknowledgement are for confirming the transmission and also,
it could prevent incorrect order. Flags are used for checking the type of packet and also could know if the header is corrupted. Similarly, checksum is calculated using hashlib with md5 encryption (32 bits) to check if data is corrupted. Payload stores the data and it is cut by the maximum segment size from the original file.

## Design
The main issue with this design is that it is rushed in two weeks. The only goal in mind is too finished this protocol quickly. It has a rather simple header and the header is converted from a list which depends on pickle. If pickle somehow fails, the transmission could not proceed. It also consumes a large amount of ram when transmitting large files (>100M). In this case, a 400MB file is being transmitted. The reason is that the entire file is read and cut into chunks and stored in RAM.
![It is like Chrome](Memory.png)
Furthermore, STP could only transfer a single file but it could be solved by archiving multiple files. During three way handshake and termination, there are no error checking which is not so good but could be improved.

For pipeline, a windows will be reset as soon as out of order / duplicate ack has been received
