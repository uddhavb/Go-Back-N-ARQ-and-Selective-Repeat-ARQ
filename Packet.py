class Packet:
    def __init__(self, sequence_number, is_data,data = None):
        self.sequence_number = sequence_number
        self.is_data = is_data
        self.data = data
        self.checksum = 0

    def calculate_checksum(sequence_number, is_data, data, checksum):
        new_checksum = 0
        sequence_number = sequence_number<<32
        new_checksum += ones_comp_add16()
        is_data = is_data<<16
        print(a)
        a = (int.from_bytes(a.en
        code(), 'big')
        print(a)
        a = int(a, 2)
        a = a.to_bytes((a.bit_length() + 7) // 8, 'big').decode()
        print(a)
        print("calculate checksum")
        for

    def ones_comp_add16(num1,num2):
        MOD = 1 << 16
        result = num1 + num2
        return result if result < MOD else (result+1) % MOD

    n1 = 0b1010001111101001
    n2 = 0b1000000110110101
    result = ones_comp_add16(n1,n2)

print('''\
  {:016b}
+ {:016b}
------------------
  {:016b}'''.format(n1,n2,result))
