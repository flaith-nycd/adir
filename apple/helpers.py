# -*- coding: utf-8 -*-
"""
Some helpers
"""

__author__ = 'Nicolas Djurovic'
__version__ = '0.2'

BYTES_TO_DISPLAY = 16


def int2ascii(char):
    if char in range(32, 127):  # Check from ascii code $20 to $7E
        return chr(char)
    elif char in range(160, 255):  # if between $A0 to $FE
        return chr(char - 128)  # Substract $80 to go back between $20 to $7E
    else:
        return '.'


def split_array(arraylist, size):
    return [arraylist[i:i + size] for i in range(0, len(arraylist), size)]


def generate(arraylist, size):
    header = [' ' * 5]
    for i in range(size):
        header.append('{:02X} '.format(i))
    header = ''.join(header)

    hexa_list = []
    for char in arraylist:
        hexa_list.append("{:02X}".format(char))
    hexa_list = ' '.join(hexa_list)

    char_list = []
    for char in arraylist:
        char_list.append(int2ascii(char))
    char_list = ''.join(char_list)

    result_list = split_array(hexa_list, size * 2 + size)
    result_char = split_array(char_list, size)

    return header, result_list, result_char


def generate_header(value):
    # Format dumping display
    list_header, list_byte, list_text = generate(value, BYTES_TO_DISPLAY)
    return list_header, list_byte, list_text


def dump_display(list_byte, list_text):
    for index, (byte_row, text_row) in enumerate(zip(list_byte, list_text)):
        # width: __BYTES_TO_DISPLAY * 2 + __BYTES_TO_DISPLAY is the same value in function 'generate'
        # - 1 to remove the last space
        print('{:04X}:{:<{width}}  {}'.format(index * BYTES_TO_DISPLAY, byte_row.strip(), text_row,
                                              width=(BYTES_TO_DISPLAY * 3) - 1))


def dump_dos(value, track, sector):
    list_header, list_byte, list_text = generate_header(value)
    print('{}  T${:02X} S${:02X}'.format(list_header.rstrip(), track, sector))
    print()
    dump_display(list_byte, list_text)


def dump_prodos(value, block):
    list_header, list_byte, list_text = generate_header(value)
    print('{}  BLOCK ${:02X}'.format(list_header.rstrip(), block))
    print()
    dump_display(list_byte, list_text)
