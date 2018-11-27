import socket
import sys
from Packet import Packet
from Packet import calculate2ByteChecksum
from Packet import extract_data
import threading
import time
# Simple_ftp_client client-host-name server-port# file-name N MSS
hostname = sys.argv[1]
port_number = int(sys.argv[2])
file_name = sys.argv[3]
N = int(sys.argv[4])
MSS = int(sys.argv[5])

'''
maintain a list of size N
'''
Window = []
lock_on_window = threading.Lock()


def get_acks(client):
    global Window
    global lock_on_window
    while True:
        ack = client.recv(8)
        if ack != b'':
            ack = extract_data(ack)
            print("WIIIIIIIIIIIIIIIINDOW:\t\t\t", Window)
            print("ACCCCCCCCCCCCCKKKKKKK:\t\t\t",ack)
            with lock_on_window:
                number_of_elements_to_delete = Window.index(ack[0]) + 1
                while number_of_elements_to_delete > 0:
                    del(Window[0])
                    number_of_elements_to_delete -= 1


# create an ipv4 (AF_INET) socket object using the tcp protocol (SOCK_STREAM)
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# connect the client
# client.connect((target, port))
client.connect((hostname, port_number))
ack_thread = threading.Thread(target=get_acks, args = (client,))
ack_thread.daemon = True
ack_thread.start()

with open(file_name, "rb") as f:
    sequence_number = 0
    mss = f.read(MSS)
    while mss:
        with lock_on_window:
            if len(Window) <= N:
                packet = Packet(sequence_number, 21845, mss)
                print("MSS: ", mss)
                Window.append(sequence_number)
                sequence_number+=1
                # print("Sending: ", packet.packetData)
                client.send(packet.packetData)
                mss = f.read(MSS)
                time.sleep(0.1)

ack_thread.join()
