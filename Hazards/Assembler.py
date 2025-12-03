''' 
This program will serve as an assembler for RISC-V instructions.
It will read instructions in string format, interpret them, and 
present them back to the user in binary format.

Note: This dissasembler only works for R, I, I*, S, SB, and U type 
instructions. 
'''
import numpy as np

def encodeInstruction(instruction):
    '''
    this method will encode an instruction into binary
    '''
    # encodes a single RISC-V instruction into binary 
    # calls writeEncoded() to write the instruction to a binary file
    return 0

def writeEncoded(instruction):
    '''
    this method will write an encoded instruction to a binary file 
    '''
    # check if instruction is the correct length 
    if not len(instruction) == 32:
        raise ValueError("Not correct length (%s)" % (instruction))
    
    instruction = int(instruction, 2)

    all_bytes = []
    mask = 2**8 - 1
    all_bytes.append(instruction & mask)
    all_bytes.append((instruction >> 8) & mask)
    all_bytes.append((instruction >> 16) & mask)
    all_bytes.append((instruction >> 24) & mask)
    all_bytes_array = bytearray(all_bytes)

    bin(all_bytes_array[0]), bin(all_bytes_array[-1])

    with open("risc-v_instructions.bin", 'wb+') as rv_file:
        rv_file.write(all_bytes_array)

def binaryToString(num):
    '''
    this method returns a string with all bits in binary and the beginning
    0b removed
    '''
    return (bin(num)) [2:]