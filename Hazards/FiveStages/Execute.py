'''
This file contains all logic for the execute stage, for each 
instruction type that is supported by the assembler. This 
includes R, I, I*, S, SB, and U type instructions. 
'''

def executeRType(instruction_data, cycle_data): 
    '''
    decode R-type instruction 
    syntax: opcode rd, rs1, rs2
    '''

    return instruction_data, cycle_data

def executeI_LType(instruction_data,cycle_data):
    '''
    decode I-type load instructions
    '''

    return instruction_data, cycle_data

def executeI_AType(instruction_data, cycle_data):
    '''
    decode I-type (arithmetic) instructions 
    '''

    return instruction_data, cycle_data

def executeSType(instruction_data, cycle_data):
    '''
    decode S-type instruction
    syntax: opcode rs2, immediate(rs1)
    '''

    return instruction_data, cycle_data

def executeSBType(instruction_data, cycle_data):
    '''
    decode SB-type instruction
    syntax: opcode rs1, rs2, immediate
    '''

    return instruction_data, cycle_data

def executeUType(instruction_data, cycle_data):
    '''
    decode U-type instruction
    syntax: opcode, rd, immediate
    '''

    return instruction_data, cycle_data