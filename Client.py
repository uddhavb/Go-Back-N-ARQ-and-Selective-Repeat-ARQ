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
    print("new thread")
    global Window
    global lock_on_window
    while True:
        # time.sleep(3)
        ack, address = client.recvfrom(20)
        if ack != b'':
            ack = extract_data(ack)
            with lock_on_window:
                for index, element in enumerate(Window):
                    if element[0] == ack[0]:
                        number_of_elements_to_delete = index+1
                while number_of_elements_to_delete > 0:
                    del(Window[0])
                    number_of_elements_to_delete -= 1


# create an ipv4 (AF_INET) socket object using the tcp protocol (SOCK_STREAM)
# client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# # connect the client
# # client.connect((target, port))
# client.connect((hostname, port_number))
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client.bind(('',port_number))
client.settimeout(10)
# bind_ip = hostname
# bind_port = port_number
# # client.bind((bind_ip, bind_port))
ack_thread = threading.Thread(target=get_acks, args = (client,))
ack_thread.daemon = True
ack_thread.start()
with open(file_name, "rb") as f:
    sequence_number = 0
    mss = f.read(MSS)
    while mss:
        with lock_on_window:
            if len(Window) <= N:
                print("Send: ", mss)
                packet = Packet(sequence_number, 21845, mss)
                client.sendto(packet.packetData, (hostname, 7735))
                Window.append([sequence_number, packet.packetData, time.time()])
                sequence_number+=1
                mss = f.read(MSS)
            if time.time() - Window[0][2] > 0.5:
                print("Timeout, sequence number =", Window[0][0])
                new_window = []
                for window_element in Window:
                    print("Resend: ", window_element[1])
                    client.sendto(window_element[1], (hostname, 7735))
                    # client.send(window_element[1])
                    new_window.append([window_element[0], window_element[1], time.time()])
                Window = new_window


client.sendto(b'END', (hostname, 7735))
ack_thread.join()
