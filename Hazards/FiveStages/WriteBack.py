'''
This file contains all logic for the write back stage, for each 
instruction type that is supported by the assembler. This 
includes R, I, I*, S, SB, and U type instructions. 
'''

def writeBackRType(instruction_data, cycle_data): 
    '''
    decode R-type instruction 
    syntax: opcode rd, rs1, rs2
    '''

    # write ALU result to destination register
    instruction_data["RegWrite"] = 1    # write to register file 
    instruction_data["WBSel"] = 0   # ALU result --> register file

    return instruction_data, cycle_data

def writeBackI_LType(instruction_data, cycle_data):
    '''
    decode I-type load instructions
    '''

    # write to register file 
    cycle_data["RegWrite"] = 1
    cycle_data["WBSel"] = 1 # from memory data

    return instruction_data, cycle_data

def writeBackI_AType(instruction_data, cycle_data):
    '''
    decode I-type (arithmetic) instructions 
    '''

    # write to register file 
    cycle_data["RegWrite"] = str(1)
    cycle_data["WBSel"] = str(0)    # from ALU result
    

    return instruction_data, cycle_data

def writeBackSType(instruction_data, cycle_data):
    '''
    decode S-type instruction
    syntax: opcode rs2, immediate(rs1)
    '''

    return instruction_data, cycle_data

def writeBackSBType(instruction_data, cycle_data):
    '''
    decode SB-type instruction
    syntax: opcode rs1, rs2, immediate
    '''

    return instruction_data, cycle_data

def writeBackUType(instruction_data, cycle_data):
    '''
    decode U-type instruction
    syntax: opcode, rd, immediate
    '''

    return instruction_data, cycle_data