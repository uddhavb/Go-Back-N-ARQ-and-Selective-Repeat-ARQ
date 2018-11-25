import socket
import sys

# Simple_ftp_server port# file-name p
port_number = sys.argv[1]
filename = sys.argv[2]

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
bind_ip = 127.0.0.1
bind_port = port_number
server.bind((bind_ip, bind_port))
server.listen(5)  # max backlog of connections

print('Listening on {}:{}'.format(bind_ip, bind_port))

def drop_packets(prob, packet):
    print("drop packets")

client_socket, address = server.accept()
print('Accepted connection from {}:{}'.format(address[0], address[1]))
while True:
    request = client_socket.recv(1024)
    request = request.decode("utf-8")
    request = request.split('\n')
    index = 0
    # do stuff

    # client_socket.send(bytearray(str_to_send, "utf8"))
    # send ack
