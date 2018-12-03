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
N = int(sys.argv[5])
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
bind_port = 7735
server_socket.bind(('', bind_port))
server_socket.settimeout(10)

end_write = False
Window = []
CURRENT_SEQUENCE_NUMBER = 0
lock_on_window = threading.Lock()

def write_to_file(filename):
    global end_write
    global Window
    global lock_on_window
    global CURRENT_SEQUENCE_NUMBER
    with open(filename, 'w') as outfile:
        while True:
            with lock_on_window:
                elements = []
                for element in Window:
                    elements.append(element[0])
                print("````````",elements,'`````````',len(elements), '-----',CURRENT_SEQUENCE_NUMBER)
                if end_write:
                    while(len(Window)!=0):
                        print("WRITING:__", CURRENT_SEQUENCE_NUMBER)
                        outfile.write(Window[0][1].decode("utf-8"))
                        del Window[0]
                        CURRENT_SEQUENCE_NUMBER += 1
                    break
                elif len(Window) >= N:
                    if Window[0][0] == CURRENT_SEQUENCE_NUMBER:
                        print("WRITING:", CURRENT_SEQUENCE_NUMBER)
                        outfile.write(Window[0][1].decode("utf-8"))
                        del Window[0]
                        CURRENT_SEQUENCE_NUMBER += 1
                    elif Window[0][0] < CURRENT_SEQUENCE_NUMBER:
                        raise ValueError('sequence number more than first packet in window')
                    else:
                        CURRENT_SEQUENCE_NUMBER = Window[0][0]
    print("DONE WRITING.......")


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
            if (checksum == received_checksum and random.uniform(0, 1) > probability_of_loss):
                packet = Packet(int(data[0]), 43690)
                server_socket.sendto(packet.packetData, (client_ip, client_port_number))
                # print("ack: ", data[0])
                with lock_on_window:
                    # print(CURRENT_SEQUENCE_NUMBER, data[0], "---------------")
                    list_of_seq = []
                    for element in Window:
                        list_of_seq.append(element[0])
                    if data[0] >= CURRENT_SEQUENCE_NUMBER and int(data[0]) not in list_of_seq:
                        bisect.insort(Window,[int(data[0]), data[3]])
            # else:
            #     print("Packet loss, sequence number =", data[0])
    print("RTT: ", RTT)
except Exception as e:
   print(e)
   print("Connection broken")
write_thread.join()
