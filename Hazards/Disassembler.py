''' 
This program will serve as a dissasembler for RISC-V instructions.
It will read binary encoded instructions, interpret them, and present
them back to the user in a human readable assembly language. 

Note: This dissasembler only works for R, I, I*, S, SB, and U type 
instructions. 

THIS CODE IS BASED ON MY DISASSEMBLER ASSIGNMENT SUBMISSION
'''

import numpy as np
from Decode import *

def decodeInstruction(encoded_instruction):
    '''
    this method decodes a single binary RISC-V instruction into text
    '''
    # extract the opcode
    opcode = encoded_instruction & 0x7F

    # using the opcode, determine the instruction type
    if opcode == 0x33: # R-type instruction
        return decodeRType(encoded_instruction)
    elif opcode == 0x03: # I-type instruction (load)
        return decodeI_LType(encoded_instruction)
    elif opcode == 0x13: # I-type instruction (arithmetic)
        return decodeI_AType(encoded_instruction)
    elif opcode == 0x23: # S-type instruction
        return decodeSType(encoded_instruction)
    elif opcode == 0x63: # SB-type instruction 
        return decodeSBType(encoded_instruction)
    elif opcode == 0x37 or opcode == 0x17: # U-type instruction
        return decodeUType(encoded_instruction, opcode)
    else:
        raise ValueError(f"Could not identify instruction type: {encoded_instruction}")
 