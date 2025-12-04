''' 
This program will serve as an assembler for RISC-V instructions.
It will read instructions in string format, interpret them, and 
present them back to the user in binary format.

Note: This assembler only works for R, I, I*, S, SB, and U type 
instructions. 
'''

import numpy as np
from Encode import *

def encodeInstruction(instruction):
    '''
    this method encodes a single RISC-V instruction into binary 
    '''

    # clean and parse string 
    cleaned_instruction = instruction.replace(',', '') # remove comma
    cleaned_instruction = cleaned_instruction.replace('(', ' ') # remove parenthesis
    cleaned_instruction = cleaned_instruction.replace(')', ' ')
    
    unwanted_char = ' '
    cleaned_instruction = cleaned_instruction.strip(unwanted_char) # remove white space 

    print(cleaned_instruction)
    segments = cleaned_instruction.split(' ') # split segments and save in list
    # print(segments)

    # initial encoded instruction 
    encoded_instruction = 0

    # extract instruction type to determine opcode 
    opcode_str = segments[0]

    # encode instruction depending on opcode
    if opcode_str in ['add', 'sub', 'sll', 'slt', 'sltu', 'xor', 'srl', 'sra', 'or', 'and']:
        # R-type instruction 
        encoded_instruction = encodeRType(segments, encoded_instruction)
    elif opcode_str in ['addi', 'slli', 'slti', 'sltiu', 'xori', 'ori', 'andi']:
        # I-type instruction (arithmetic)
        encoded_instruction = encodeI_AType(segments, encoded_instruction)
    elif opcode_str in ['lb', 'lh', 'lw', 'lbu', 'lhu']:
        # I-type instruction (load)
        encoded_instruction = encodeI_LType(segments, encoded_instruction)
    elif opcode_str in ['slli', 'srli', 'srai']:
        # I*-type instruction 
        encoded_instruction = encodeI_SType(segments, encoded_instruction)
    elif opcode_str in ['sb','sh','sw']:
        # S-type instruction 
        encoded_instruction = encodeSType(segments, encoded_instruction)
    elif opcode_str in ['beq','bne','blt','bge','bltu','bgeu']:
        # SB-type instruction 
        encoded_instruction = encodeSBType(segments, encoded_instruction)
    elif opcode_str in ['lui','auipc']:
        # U-type instruction
        encoded_instruction = encodeUType(segments, encoded_instruction)
    else:
        raise ValueError(f"Could not identify instruction type: {instruction}")

    # call writeEncoded() to write the instruction to a binary file
    return encoded_instruction

def writeEncoded(instruction, file_name):
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

    with open(file_name, 'ab') as rv_file:
        rv_file.write(all_bytes_array)

def binaryToString(num):
    '''
    this method returns a string with all bits in binary and the beginning
    0b removed
    '''
    unsigned = num & 0xFFFFFFFF
    return format(unsigned, '032b')

#### TESTING ####

def main():
    instructions = ["lw x7, 0(x10)", "addi x5, x0, 3", "lw x6, 0(x7)", "xori x6, x6, 32", "sw x6, 0(x7)", 
        "addi x7, x7, 4", "addi x5, x5, -1", "bne x5, x0, -40"]

    file_name = "test.bin"

    for instruction in instructions:
        encoded_instruction = encodeInstruction(instruction)
        encoded_instruction = binaryToString(encoded_instruction)
        print(encoded_instruction)
        writeEncoded(encoded_instruction, file_name)

        print("\n")

    return 0

if __name__ == "__main__":
    main()