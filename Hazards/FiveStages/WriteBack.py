'''
This file contains all logic for the write back stage, for each 
instruction type that is supported by the assembler. This 
includes R, I, I*, S, SB, and U type instructions. 
'''

def writeBackRType(cycle_data): 
    '''
    decode R-type instruction 
    syntax: opcode rd, rs1, rs2
    '''

    return cycle_data

def writeBackI_LType(cycle_data):
    '''
    decode I-type load instructions
    '''

    return cycle_data

def writeBackI_AType(cycle_data):
    '''
    decode I-type (arithmetic) instructions 
    '''

    return cycle_data

def writeBackSType(cycle_data):
    '''
    decode S-type instruction
    syntax: opcode rs2, immediate(rs1)
    '''

    return cycle_data

def writeBackSBType(cycle_data):
    '''
    decode SB-type instruction
    syntax: opcode rs1, rs2, immediate
    '''

    return cycle_data

def writeBackUType(cycle_data):
    '''
    decode U-type instruction
    syntax: opcode, rd, immediate
    '''

    return cycle_data