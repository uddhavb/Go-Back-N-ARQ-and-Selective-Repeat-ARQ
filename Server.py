import socket
import sys
from Packet import Packet
from Packet import calculate2ByteChecksum
from Packet import extract_data
import time

# Simple_ftp_server port# file-name p
port_number = int(sys.argv[1])
filename = sys.argv[2]

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
bind_ip = '127.0.0.1'
bind_port = port_number
server.bind((bind_ip, bind_port))
server.listen(5)  # max backlog of connections

print('Listening on {}:{}'.format(bind_ip, bind_port))

def drop_packets(prob, packet):
    print("drop packets")

client_socket, address = server.accept()
Window = []
print('Accepted connection from {}:{}'.format(address[0], address[1]))
with open(filename, 'w') as outfile:
    while True:
        request = client_socket.recv(1024)
        print("request: ",request)
        # request = request.decode("utf-8")
        checksum = calculate2ByteChecksum(request)

        # print(data[0],data[1],data[2],data[3])


        # print("checksum: ", checksum)
        if checksum != 0:
            print("Packet is corrupted!! Seq num:", request[0])
        else:
            data = extract_data(request)
            print("DATA:\n",data[3].decode("utf-8"))
            outfile.write(data[3].decode("utf-8"))
            print("ACK for: ", data[0])
            packet = Packet(int(data[0]), 43690)
            print("ACK: ", packet.packetData)
            server.send(packet.packetData)
time.sleep(5)
