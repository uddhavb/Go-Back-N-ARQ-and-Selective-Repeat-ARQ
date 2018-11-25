import socket
import sys

# Simple_ftp_client client-host-name server-port# file-name N MSS
hostname = sys.argv[1]
port_number = sys.argv[2]
file_name = sys.argv[3]
N = sys.argv[4]
MSS = sys.argv[5]

# create an ipv4 (AF_INET) socket object using the tcp protocol (SOCK_STREAM)
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# connect the client
# client.connect((target, port))
client.connect((hostname, port_number))

with open(file_name, "rb") as f:
    length_of_packet = 1
    byte = f.read(1)
    while byte:
        data = []
        while byte and length_of_packet <= MSS:
            # update length_of_packet
            data.append(byte)
            length_of_packet += 1
            byte = f.read(1)
        length_of_packet = 0
        # convert the list of bytes to a single stream
        data = b''.join(data)
        # data = bytearray(data, 'utf8')
        client.send(data)
        ack = client.recv(1024)
    	ack = ack.decode("utf-8")
