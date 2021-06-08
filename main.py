from reed_solomon import *
from Hamming import *
import math as m


def main():

    mode = input("Type 'encode' to enter encoding mode or 'decode' to enter decoding mode. \n")
    if mode == 'encode':
        rsc = ReedSolomonCoder(int(input("Insert amount of redundant characters to Reed Solomon coder: \n")))

        block_len = int(input("Insert block length to Hamming coder: \n"))

        message = str(input("Insert message. \n")).encode("utf-8")

        """errors = input("Specify, which bits will have an error. Insert order numbers, separated by commas. "
                       "There are " + str(len(message)*encoded_block_len) + " bits in message. \n")"""

        print(str(message) + "----- Input")

        rs_encoded = rsc.encode(message)
        print(str(bytes(rs_encoded)) + "----- RS encoded")

        hamming_encoded = inner_coder(rs_encoded, block_len)
        print(str(list_to_hex(hamming_encoded)) + "----- Hamming encoded")

    elif mode == 'decode':

        rsc = ReedSolomonCoder(int(input("Insert amount of redundant characters to Reed Solomon coder: \n")))

        block_len = int(input("Insert block length to Hamming coder: \n"))
        block_len = int(m.floor(m.log2(block_len))) + 1 + block_len

        corrupted_message = '0x' + str(input("Insert message. \n")).replace(' ', '')

        hamming_decoded = inner_decoder(corrupted_message, block_len)
        print(str(hamming_decoded) + "----- Hamming decoded")

        try:
            rs_decoded = rsc.decode(hamming_decoded)
            print(str(rs_decoded) + "----- RS decoded")
        except Exception:
            print("Message cannot be decoded: Too many errors found by Chien Search.")
    else:
        print("Incorrect mode. \n")
    return 0


if __name__ == '__main__':
    main()
