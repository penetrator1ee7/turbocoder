import bitstring as bstr


def insert_errors(message, errors):
    errors = errors.replace(' ', '').split(',')
    for number in errors:
        block_number = int(number) // len(message[0])
        bit_number = int(number) % len(message[0])
        error = bstr.BitArray("0b" + message[block_number].pop(bit_number))
        error = ~error
        message[block_number].insert(bit_number, str(error.uint))
    return message


def list_to_bits(list):
    bits = ""
    for block in list:
        bits += ''.join(block)
    while len(bits) % 16 != 0:
        bits += '0'
    bits = bytearray.fromhex(bstr.BitArray("0b" + bits).hex)
    return bits


def place_checkbit_placeholders(bitlist):
    new_bitlist = list('00') + list(bitlist[0])
    if len(bitlist) >= 2:
        new_bitlist += list('0') + bitlist[1:4]
    if len(bitlist) >= 5:
        new_bitlist += list('0') + bitlist[4:11]
    if len(bitlist) >= 9:
        new_bitlist += list('0') + bitlist[11:]
    return new_bitlist


def determine_checkbit(double_list):
    checkbit = []
    for x in double_list:
        checkbit.extend(x if isinstance(x, list) else [x])
    return checkbit.count('1') % 2


def calculate_checkbits(bitlist):
    bits_to_check = []
    bits_to_check.append([bitlist[i] for i in range(0, len(bitlist), 2)])
    bits_to_check.append([bitlist[i:i + 2] for i in range(1, len(bitlist), 4)])
    if len(bitlist) >= 4:
        bits_to_check.append([bitlist[i:i + 4] for i in range(3, len(bitlist), 8)])
    if len(bitlist) >= 8:
        bits_to_check.append([bitlist[i:i + 8] for i in range(7, len(bitlist), 16)])
    if len(bitlist) >= 16:
        bits_to_check.append([bitlist[i:i + 16] for i in range(15, len(bitlist), 32)])
    checkbits = []
    for i in range(len(bits_to_check)):
        checkbits.append(determine_checkbit(bits_to_check[i]))
    return checkbits


def inner_coder(message, block_length):
    bit_array = list(bstr.BitArray(message).bin)
    bit_array = [bit_array[i:i + block_length] for i in range(0, len(bit_array), block_length)]
    i = 0
    for block in bit_array:
        block = place_checkbit_placeholders(block)
        checkbits = calculate_checkbits(block)
        block[0] = str(checkbits[0])
        block[1] = str(checkbits[1])
        if len(checkbits) >= 3:
            block[3] = str(checkbits[2])
        if len(checkbits) >= 4:
            block[7] = str(checkbits[3])
        if len(checkbits) >= 5:
            block[15] = str(checkbits[4])
        bit_array[i] = block
        i += 1
    return bit_array


def inner_decoder(msg):
    message = msg
    i = 0
    for block in message:
        checkbits = calculate_checkbits(block)
        syndrome = bstr.BitArray()
        for bit in checkbits:
            syndrome.append("0b" + str(bit))
        syndrome.reverse()
        syndrome = syndrome.uint
        if syndrome != 0 and syndrome <= len(block):
            crashed_bit = ~ bstr.BitArray("0b" + block.pop(syndrome - 1))
            block.insert(syndrome - 1, str(crashed_bit.uint))
        block.pop(0)
        block.pop(0)
        if len(block) >= 2:
            block.pop(1)
        if len(block) >= 5:
            block.pop(4)
        if len(block) >= 12:
            block.pop(11)
        message[i] = block
        i += 1
    return list_to_bits(message)
