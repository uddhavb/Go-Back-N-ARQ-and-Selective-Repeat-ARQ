import socket
import sys
from Packet import Packet
from Packet import calculate2ByteChecksum
from Packet import extract_data
import time
import random
import bisect
import threading
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

end_write = False
Window = []
CURRENT_SEQUENCE_NUMBER = 0
lock_on_window = threading.Lock()

def write_to_file(filename):
    global Window
    global lock_on_window
    global CURRENT_SEQUENCE_NUMBER
    with open(filename, 'w') as outfile:
        while True:
            if end_write:
                break
            with lock_on_window:
                while len(Window) != 0:
                    if Window[0][0] == CURRENT_SEQUENCE_NUMBER:
                        outfile.write(Window[0][1].decode("utf-8"))
                        del Window[0]
                        CURRENT_SEQUENCE_NUMBER += 1

write_thread = threading.Thread(target=write_to_file, args = (filename,))
write_thread.daemon = True
write_thread.start()
# server.listen(5)  # max backlog of connections
RTT = 0
startRTTCalc = True
repeatSeq = 0
repeatSeqCount=0
try:
    with open(filename, 'w') as outfile:
        while True:
            request, address = server_socket.recvfrom(1024)
            # print(request)
            if request == b'END':
                end_write = True
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
            if (checksum == received_checksum and random.uniform(0, 1) > probability_of_loss):
                print(data[3].decode('utf8'))
                with lock_on_window:
                    exists = False
                    for pending_packet in Window:
                        if pending_packet[0] == data[0]:
                            exists = True
                    if not exists:
                        bisect.insort(Window,[int(data[0]), data[3]])
                packet = Packet(int(data[0]), 43690)
                server_socket.sendto(packet.packetData, (client_ip, client_port_number))
            else:
                print("Packet loss, sequence number =", data[0])
    print("RTT: ", RTT)
except Exception as e:
   print(e)
   print("Connection broken")
