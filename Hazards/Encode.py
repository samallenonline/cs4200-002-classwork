'''
This file contains all logic for encoding each instruction type
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

    # identify and store segments 
    opcode_str = segments[0]
    rd_int = int(segments[1].replace('x', ''))
    rs1_int = int(segments[2].replace('x', ''))
    rs2_int = int(segments[3].replace('x', ''))

    # translate segments to binary and set 
    encoded_instruction |= 0b0110011   # opcode
    encoded_instruction |= (rd_int << 7) # rd

    # mapping for funct3 value depending on opcode 
    funct3_map = {
        'add': 0b000, 'sub': 0b000, 'and': 0b111, 'or': 0b110, 'xor': 0b100, 'sll': 0b001,
        'srl': 0b101, 'sra': 0b101, 'slt': 0b010, 'sltu': 0b011
    }

    encoded_instruction |= (funct3_map[opcode_str] << 12)   # funct3
    encoded_instruction |= (rs1_int << 15)   # rs1
    encoded_instruction |= (rs2_int << 20)   # rs2

    # mapping for funct7 value depending on opcode 
    funct7_map = {
        'add': 0b0000000, 'sub': 0b0100000, 'and': 0b0000000, 'or': 0b0000000, 'xor': 0b0000000, 'sll': 0b0000000,
        'srl': 0b0000000, 'sra': 0b0100000, 'slt': 0b0000000, 'sltu': 0b0000000
    }

    encoded_instruction |= (funct7_map[opcode_str] << 25)   # funct7

    return encoded_instruction

def encodeI_AType(segments, encoded_instruction):
    '''
    encode I-type instruction (arithmetic) 
    syntax: opcode rd, rs1, immediate
    '''
    print("I-type Arithmetic")
    print(segments)

    # identify and store segments 
    opcode_str = segments[0]
    rd_int = int(segments[1].replace('x', ''))
    rs1_int = int(segments[2].replace('x', ''))
    immediate = int(segments[3])

    # translate segments to binary and set
    encoded_instruction |= 0b0010011    # opcode
    encoded_instruction |= (rd_int << 7)    # rd

    # mapping for funct3 value depending on opcode 
    funct3_map = {
        'addi': 0b000, 'andi': 0b111, 'ori': 0b110, 'xori': 0b100, 'slti': 0b010, 'sltiu': 0b011
    }

    encoded_instruction |= (funct3_map[opcode_str] << 12)   # funct3
    encoded_instruction |= (rs1_int << 15)  # rs1

    # set immediate 
    # handle negatives with 2s complement 
    if immediate < 0:
        immediate = (1 << 12) + immediate
    
    encoded_instruction |= (immediate & 0xFFF) << 20    # immediate

    return encoded_instruction

def encodeI_LType(segments, encoded_instruction):
    '''
    encode I-type instruction (load) 
    syntax: opcode rd, immediate(rs1)
    '''
    print("I-type Load")
    print(segments)

    # identify and store segments 
    opcode_str = segments[0]
    rd_int = int(segments[1].replace('x', ''))
    immediate = int(segments[2])
    rs1_int = int(segments[3].replace('x', ''))

    # translate segments to binary and set
    encoded_instruction |= 0b0000011    # opcode
    encoded_instruction |= (rd_int << 7)    # rd

    # mapping for funct3 value depending on opcode
    funct3_map = {
        'lb': 0b000, 'lbu': 0b100, 'lh': 0b001, 'lhu': 0b101, 'lw': 0b010, 
    }

    encoded_instruction |= (funct3_map[opcode_str] << 12)   # funct3
    encoded_instruction |= (rs1_int << 15)  # rs1

    # set immediate 
    # handle negatives with sign extension
    if immediate < 0:
        immediate = (1 << 12) + immediate
    
    encoded_instruction |= (immediate & 0xFFF) << 20    # immediate

    return encoded_instruction

def encodeI_SType(segments, encoded_instruction):
    '''
    encode I*-type instruction
    syntax: opcode rd, rs1, immediate
    '''
    print("I*-type")
    print(segments)

    # identify and store segments
    opcode_str = segments[0]
    rd_int = int(segments[1].replace('x', ''))
    rs1_int = int(segments[2].replace('x', ''))
    immediate = int(segments[3])

    # translate segments to binary and set 
    encoded_instruction |= 0b0010011 # opcode
    encoded_instruction |= (rd_int << 7)    # rd
    
    # mapping for funct3 value based on opcode 
    funct3_map = {
        'slli': 0b001, 'srli': 0b101, 'srai': 0b101
    }

    encoded_instruction |= (funct3_map[opcode_str] << 12)   # funct3
    encoded_instruction |= (rs1_int << 15)  # rs1
    encoded_instruction |= ((immediate & 0x1F) << 20) # immediate

    # mapping for funct7 value based on opcode
    funct7_map = {
        'slli': 0b0000000, 'srli': 0b0000000, 'srai': 0b0100000
    }

    encoded_instruction |= (funct7_map[opcode_str] << 25)

    return encoded_instruction

def encodeSType(segments, encoded_instruction):
    '''
    encode S-type instruction
    syntax: opcode rs2, immediate(rs1)
    '''
    print("S-type")
    print(segments)

    # identify and store segments 
    opcode_str = segments[0]
    rs2_int = int(segments[1].replace('x', ''))
    immediate = int(segments[2])
    rs1_int = int(segments[3].replace('x', ''))

    # translate segments to binary and set
    encoded_instruction |= 0b0100011 # opcode 

    imm4_0 = immediate & 0x1F   # get lower 5 bits of offset
    encoded_instruction |= (imm4_0 << 7)    # immediate[4:0]

    # mapping for funct3 value depending on opcode 
    funct3_map = {
        'sb': 0b000, 'sh': 0b001, 'sw': 0b010
    }

    encoded_instruction |= (funct3_map[opcode_str] << 12)   # funct3
    encoded_instruction |= (rs1_int << 15)  # rs1
    encoded_instruction |= (rs2_int << 20)  # rs2

    # set immediate 
    imm11_5 = (immediate >> 5) & 0x7F # get upper 7 bits of offset
    encoded_instruction |= (imm11_5 << 25)  # immediate[11:5]

    return encoded_instruction

def encodeSBType(segments, encoded_instruction):
    '''
    encode SB-type instruction
    syntax: opcode rs1, rs2, immediate
    '''
    print("SB-type")
    print(segments)

    # identify and store segments
    opcode_str = segments[0]
    rs1_int = int(segments[1].replace('x', ''))
    rs2_int = int(segments[2].replace('x', ''))
    immediate = int(segments[3])

    # translate segments to binary and set 
    encoded_instruction |= 0b1100011    # opcode

    # set immediate 
    # handle negative immediates using 2s complement 
    if immediate < 0:
        immediate_13bit = (1 << 13) + immediate
    else:
        immediate_13bit = immediate

    immediate_13bit = immediate_13bit & 0x1FFF # ensure 13 bits 

    # store immediate segments
    imm12 = (immediate_13bit >> 12) & 0x1   # bit 12
    imm11 = (immediate_13bit >> 11) & 0x1   # bit 11
    imm10_5 = (immediate_13bit >> 5) & 0x3F # bits 10:5
    imm4_1 = (immediate_13bit >> 1) & 0xF   # bits 4:1

    # set immediate segments 
    encoded_instruction |= (imm11 << 7)     # immediate[11]
    encoded_instruction |= (imm4_1 << 8)    # immediate[4:1]
    encoded_instruction |= (imm10_5 << 25)  # immediate[10:5]
    encoded_instruction |= (imm12 << 31)

    # mapping for funct3 based on opcode 
    funct3_map = {
        'beq': 0b000, 'bge': 0b101, 'bgeu': 0b111, 'blt': 0b100, 'bltu': 0b110, 'bne': 0b001
    }

    encoded_instruction |= (funct3_map[opcode_str] << 12)    # funct3
    encoded_instruction |= (rs1_int << 15)  # rs1
    encoded_instruction |= (rs2_int << 20)  # rs2

    return encoded_instruction

def encodeUType(segments, encoded_instruction):
    '''
    encode U-type instruction
    syntax: opcode, rd, immediate
    '''
    print("U-type")
    print(segments)

    # identify and store segments
    opcode_str = segments[0]
    rd_int = int(segments[1].replace('x', ''))
    immediate = int(segments)[2]

    # translate segments to binary and set 
    # mapping for binary opcode based on string opcode 
    opcode_map = {
        'auipc': 0b0010111, 'lui': 0b0110111
    }

    encoded_instruction |= opcode_map[opcode_str]   # opcode 
    encoded_instruction |= (rd_int << 7)    # rd

    # set immediate
    # handle negatives with 2s complement 
    if immediate < 0:
        immediate_20bit = (1 << 20) + immediate
    else:
        immediate_20bit = immediate
    
    immediate_20bit = immediate_20bit & 0xFFFFF # ensure 20 bits
    encoded_instruction |= (immediate_20bit << 12)    # immediate[31:12]

    return encoded_instruction