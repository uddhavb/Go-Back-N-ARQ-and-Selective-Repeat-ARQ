import struct
from array import array
import sys

def calculate2ByteChecksum(packet):
    checksum = 0
    packet_to_byte = array("B", packet)
    i = 0
    while i < len(packet_to_byte)/2:
        # print(int.from_bytes(mystr[i*2:i*2+1], byteorder=sys.byteorder))
        checksum += int.from_bytes(packet_to_byte[i*2:i*2+1], byteorder=sys.byteorder)
        checksum += (packet_to_byte[i]<<8) + packet_to_byte[i+1]
        mask = 0b1111111111111111
        carry = (checksum ^ mask) >> 16
        while(carry != 0):
            checksum = checksum & mask
            checksum += carry
            carry = (checksum ^ mask) >> 16
        i += 2
    return checksum

class Packet:
    def __init__(self, sequence_number, is_data_or_ack, data = b''):
        checksum = 0
        sequence_number = sequence_number << 32
        header = sequence_number + (checksum << 16)
        header += is_data_or_ack
        header = struct.pack("!Q",header)
        packet_to_byte = struct.unpack("8B",header)
        packet_to_byte = list(packet_to_byte)
        data = array("B",data)
        packet_to_byte.extend(data)
        self.packetData = array('B',packet_to_byte).tostring()
        checksum = calculate2ByteChecksum(self.packetData)
        # print("checksum: ", checksum)
        byte_array = array('B',self.packetData)
        '''next 2 bytes give the checksum'''
        byte_array[4] = checksum>>8
        # print("byte_array[4] ", byte_array[4])
        mask = 0b11111111
        byte_array[5] = checksum&mask
        # print("byte_array[5] ",byte_array[5])
        self.packetData = array('B',byte_array).tostring()

def extract_data(packet): #packet is an attribute of above class
    sequence_number = 0
    byte_array = array('B',packet)
    print(byte_array, len(byte_array))
    '''get the seq num from the first 4 bytes'''
    for i in range(0,4):
        sequence_number = sequence_number + (byte_array[i]<<((3-i)*8))
    '''next 2 bytes give the checksum'''
    checksum = byte_array[4]<<8
    checksum = checksum + byte_array[5]
    '''next two bytes give the option'''
    is_data_or_ack = byte_array[6]<<8
    is_data_or_ack = is_data_or_ack + byte_array[7]
    '''rest is all data'''
    data = array('B',list(byte_array[8:])).tostring()
    return [sequence_number, checksum, is_data_or_ack, data]
