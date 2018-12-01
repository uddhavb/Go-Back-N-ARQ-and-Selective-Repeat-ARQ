import socket
import sys
from Packet import Packet
from Packet import calculate2ByteChecksum
from Packet import extract_data
import time
import random

# Simple_ftp_server port# file-name p
client_ip = input(sys.argv[1])
client_port_number = int(sys.argv[2])
filename = sys.argv[3]
probability_of_loss = float(sys.argv[4])

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# client_ip = '127.0.0.1'
bind_port = 7735
server_socket.bind(('', bind_port))

server_socket.settimeout(10)
# server.listen(5)  # max backlog of connections
CURRENT_SEQUENCE_NUMBER = 0
# server_socket, address = server.accept()
Window = []
# print('Accepted connection from {}:{}'.format(address[0], address[1]))
try:
    with open(filename, 'w') as outfile:
        while True:
            request, address = server_socket.recvfrom(1024)
            # request = server_socket.recv(1024)
            checksum = calculate2ByteChecksum(request)
    #        print("Received data = " + str(request))
    #        print("Server Checksum = " + str(checksum))
            # print(data[0],data[1],data[2],data[3])
            received_checksum = request[4]<<8
            received_checksum = received_checksum + request[5]
            data = extract_data(request)
            print("calculated checksum: ", checksum, "received checksum: ", received_checksum)
            # if (time.time() - CURRENT_SEQUENCE_NUMBER[1]) > 3 and CURRENT_SEQUENCE_NUMBER[0] > data[0]:
            #     packet = Packet(CURRENT_SEQUENCE_NUMBER[0], 43690)
            #     server_socket.sendto(packet.packetData, (client_ip, client_port_number))
            #     CURRENT_SEQUENCE_NUMBER[1] = time.time()
            if CURRENT_SEQUENCE_NUMBER == int(data[0]) and (checksum == received_checksum or random.uniform(0, 1) > probability_of_loss):
                print("DATA:\t",data[3].decode("utf-8"))
                outfile.write(data[3].decode("utf-8"))
                packet = Packet(int(data[0]), 43690)
                server_socket.sendto(packet.packetData, (client_ip, client_port_number))
                CURRENT_SEQUENCE_NUMBER += 1
            else:
                print("Packet loss, sequence number =", data[0])
except Exception as e:
   print(e)
   print("Connection broken")
