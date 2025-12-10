'''
This file contains all logic for the memory stage, for each 
instruction type that is supported by the assembler. This 
includes R, I, I*, S, SB, and U type instructions. 
'''

def memoryRType(instruction_data, cycle_data): 
    '''
    decode R-type instruction 
    syntax: opcode rd, rs1, rs2
    '''

    return instruction_data, cycle_data

def memoryI_LType(instruction_data, cycle_data):
    '''
    decode I-type load instructions
    '''
    cycle_data['MemRd'] = str(1) # read from data memory

    return instruction_data, cycle_data

def memoryI_AType(instruction_data, cycle_data):
    '''
    decode I-type (arithmetic) instructions 
    '''

    return instruction_data, cycle_data

def memorySType(instruction_data, cycle_data):
    '''
    decode S-type instruction
    syntax: opcode rs2, immediate(rs1)
    '''

    # write to data memory
    cycle_data["MemWr"] = str(1)

    return instruction_data, cycle_data

def memorySBType(instruction_data, cycle_data):
    '''
    decode SB-type instruction
    syntax: opcode rs1, rs2, immediate
    '''

    return instruction_data, cycle_data

def memoryUType(instruction_data, cycle_data):
    '''
    decode U-type instruction
    syntax: opcode, rd, immediate
    '''

    return instruction_data, cycle_data