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

    # perform operation 
    instruction_data["ALUSrc"] = 0  # ALU second operand comes from register rs2

    return instruction_data, cycle_data

def executeI_LType(instruction_data,cycle_data):
    '''
    decode I-type load instructions
    '''

    # perform address calculation
    cycle_data["ALUSrc"] = str(1);  # second operand comes from immediate field

    return instruction_data, cycle_data

def executeI_AType(instruction_data, cycle_data):
    '''
    decode I-type (arithmetic) instructions 
    '''

    # perform calculation
    cycle_data["ALUSrc"] = str(1);  # second operand comes from immediate field

    return instruction_data, cycle_data

def executeSType(instruction_data, cycle_data):
    '''
    decode S-type instruction
    syntax: opcode rs2, immediate(rs1)
    '''

    # perform address calculation
    cycle_data["ALUSrc"] = str(1);  # second operand comes from immediate field

    return instruction_data, cycle_data

def executeSBType(instruction_data, cycle_data):
    '''
    decode SB-type instruction
    syntax: opcode rs1, rs2, immediate
    '''

    cycle_data["ALUSrc"] = str(0) # ALU performs comparison of registers

    return instruction_data, cycle_data

def executeUType(instruction_data, cycle_data):
    '''
    decode U-type instruction
    syntax: opcode, rd, immediate
    '''

    return instruction_data, cycle_data