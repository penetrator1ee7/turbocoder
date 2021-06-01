from reed_solomon import *
from Hamming import *
import math as m


def main():
    encoded_block_len = int(m.floor(m.log2(BLOCK_LEN))) + 1 + BLOCK_LEN
    message = str(input("Insert message. \n")).encode("utf-8")
    #message = b'Attack at dawn'

    errors = input("Specify, which bits will have an error. Insert order numbers, separated by commas. "
                   "There are " + str(len(message)*encoded_block_len) + " bits in message. \n")
    #errors = "1,3,18,19,25,43,56,81,108"

    print(str(message) + "----- Input")

    rs_encoded = rsc.encode(message)
    print(str(rs_encoded) + "----- RS encoded")

    hamming_encoded = inner_coder(rs_encoded, BLOCK_LEN)
    print(str(list_to_bits(hamming_encoded)) + "----- Hamming encoded")

    corrupted_message = insert_errors(hamming_encoded, errors)
    print(str(list_to_bits(corrupted_message)) + "----- Corrupted")

    hamming_decoded = inner_decoder(corrupted_message)
    print(str(hamming_decoded) + "----- Hamming decoded")

    try:
        rs_decoded = rsc.decode(hamming_decoded)
        print(str(rs_decoded) + "----- RS decoded")
    except Exception:
        print("Message cannot be decoded: Too many errors found by Chien Search.")
    return 0


if __name__ == '__main__':
    rsc = ReedSolomonCoder(4)
    BLOCK_LEN = 8
    main()
