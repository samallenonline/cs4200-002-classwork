'''
This file contains all logic for decoding each instruction type
that is supported by the assembler. This includes R, I, I*, S, 
SB, and U type instructions. 
'''

def encodeRType(segments, encoded_instruction): 
    '''
    encode R-type instruction 
    syntax: opcode rd, rs1, rs2
    '''
    print("R-type")
    print(segments)

    return encoded_instruction

def encodeI_AType(segments, encoded_instruction):
    '''
    encode I-type instruction (arithmetic) 
    syntax: opcode rd, rs1, immediate
    '''
    print("I-type Arithmetic")
    print(segments)

    return encoded_instruction

def encodeI_LType(segments, encoded_instruction):
    '''
    encode I-type instruction (load) 
    syntax: opcode rd, immediate(rs1)
    '''
    print("I-type Load")
    print(segments)

    return encoded_instruction

def encodeI_SType(segments, encoded_instruction):
    '''
    encode I*-type instruction
    syntax: opcode rd, rs1, immediate
    '''
    print("I*-type")
    print(segments)

    return encoded_instruction

def encodeSType(segments, encoded_instruction):
    '''
    encode S-type instruction
    syntax: opcode rs2, immediate(rs1)
    '''
    print("S-type")
    print(segments)

    return encoded_instruction

def encodeSBType(segments, encoded_instruction):
    '''
    encode SB-type instruction
    syntax: opcode rs1, rs2, immediate
    '''
    print("SB-type")
    print(segments)

    return encoded_instruction

def encodeUType(segments, encoded_instruction):
    '''
    encode U-type instruction
    syntax: opcode, rd, immediate
    '''
    print("U-type")
    print(segments)

    return encoded_instruction