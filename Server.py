import socket
import sys
from Packet import Packet
from Packet import calculate2ByteChecksum
from Packet import extract_data
import time
import random
# Simple_ftp_server port# file-name p
client_ip = sys.argv[1]
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
Window = []
RTT = 0
startRTTCalc = True
repeatSeq = 0
repeatSeqCount=0
try:
    with open(filename, 'w') as outfile:
        while True:
            request, address = server_socket.recvfrom(1024)
 #           print(request)
            if request == b'END':
                print("Done sending")
                RTT = time.time() - RTT
                break
            if startRTTCalc:
                RTT = time.time()
                startRTTCalc = False
            checksum = calculate2ByteChecksum(request)
            received_checksum = request[4]<<8
            received_checksum = received_checksum + request[5]
            data = extract_data(request)
            # print("calculated checksum: ", checksum, "received checksum: ", received_checksum)
            if CURRENT_SEQUENCE_NUMBER == int(data[0]) and (checksum == received_checksum and random.uniform(0, 1) > probability_of_loss):
                # print("DATA:\t",data[3].decode("utf-8"))
                outfile.write(data[3].decode("utf-8"))
                packet = Packet(int(data[0]), 43690)
                server_socket.sendto(packet.packetData, (client_ip, client_port_number))
                repeatSeq = CURRENT_SEQUENCE_NUMBER
                CURRENT_SEQUENCE_NUMBER += 1
                repeatSeqCount = 0
            else:
                if repeatSeq == data[0]:
                        repeatSeqCount += 1
                if repeatSeqCount > 5:
                        packet = Packet(int(data[0]), 43690)
                        server_socket.sendto(packet.packetData, (client_ip, client_port_number))
                print("Packet loss, sequence number =", data[0], "curr_seq: ",CURRENT_SEQUENCE_NUMBER, " rece seq:", data[0], checksum, received_checksum)
    print("RTT: ", RTT)
except Exception as e:
   print(e)
   print("Connection broken")
