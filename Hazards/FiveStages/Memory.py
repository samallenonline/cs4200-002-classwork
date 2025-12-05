'''
This file contains all logic for the memory stage, for each 
instruction type that is supported by the assembler. This 
includes R, I, I*, S, SB, and U type instructions. 
'''

def memoryRType(cycle_data): 
    '''
    decode R-type instruction 
    syntax: opcode rd, rs1, rs2
    '''

    return cycle_data

def memoryI_LType(cycle_data):
    '''
    decode I-type load instructions
    '''

    cycle_data['MemRd'] = str(1) # read from data memory

    return cycle_data

def memoryI_AType(cycle_data):
    '''
    decode I-type (arithmetic) instructions 
    '''

    return cycle_data

def memorySType(cycle_data):
    '''
    decode S-type instruction
    syntax: opcode rs2, immediate(rs1)
    '''

    return cycle_data

def memorySBType(cycle_data):
    '''
    decode SB-type instruction
    syntax: opcode rs1, rs2, immediate
    '''

    return cycle_data

def memoryUType(cycle_data):
    '''
    decode U-type instruction
    syntax: opcode, rd, immediate
    '''

    return cycle_data