''' 
This program will serve as a dissasembler for RISC-V instructions.
It will read binary encoded instructions, interpret them, and present
them back to the user in a human readable assembly language. 

Note: This dissasembler only works for R, I, I*, S, SB, and U type 
instructions. 

THIS CODE IS BASED ON MY DISASSEMBLER ASSIGNMENT SUBMISSION
'''

import numpy as np
from FiveStages.Decode import *

def decodeInstruction(encoded_instruction, instruction_data, cycle_data):
    '''
    this method decodes a single binary RISC-V instruction into text
    '''

    # note: at this point, labels will just be a number representing the address.
    # i may add a code that explicitly tells the disassembler that the instruction
    # is indeed a label, but for now, i will assume that anything that gets past 
    # the assembler and is not recognized is a label

    # extract the opcode
    opcode = encoded_instruction & 0x7F

    instruction_data["Op"] = opcode

    # using the opcode, determine the instruction type
    if opcode == 0x33: # R-type instruction
        return decodeRType(encoded_instruction, instruction_data, cycle_data)
    elif opcode == 0x03: # I-type instruction (load)
        return decodeI_LType(encoded_instruction, instruction_data, cycle_data)
    elif opcode == 0x13: # I-type instruction (arithmetic)
        return decodeI_AType(encoded_instruction, instruction_data, cycle_data)
    elif opcode == 0x23: # S-type instruction
        return decodeSType(encoded_instruction, instruction_data, cycle_data)
    elif opcode == 0x63: # SB-type instruction 
        return decodeSBType(encoded_instruction, instruction_data, cycle_data)
    elif opcode == 0x37 or opcode == 0x17: # U-type instruction
        return decodeUType(encoded_instruction, opcode, instruction_data, cycle_data)
    else:   # temporary: assume is a label 
        instruction_data["Instr"] = "Label:"
        print(f"RISC-V instruction: {encoded_instruction}")
        # memory address pointed to by label is hardcoded
        return instruction_data, cycle_data
 