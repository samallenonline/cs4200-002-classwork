'''
This file contains all logic for decoding each instruction type
that is supported by the assembler. This includes R, I, I*, S, 
SB, and U type instructions. 
'''

def decodeRType(encoded_instruction, instruction_data, cycle_data): 
    '''
    decode R-type instruction 
    syntax: opcode rd, rs1, rs2
    '''
    # print("R-type")

    # extract fields
    rd = (encoded_instruction >> 7) & 0x1F
    funct3 = (encoded_instruction >> 12) & 0x7
    rs1 = (encoded_instruction >> 15) & 0x1F
    rs2 = (encoded_instruction >> 20) & 0x1F
    funct7 = (encoded_instruction >> 25) & 0x7F

    # based on funct3, determine the exact instruction
    instruction = ""
    match funct3:
        case 0:
            if funct7 == 0:
                instruction = "add"
            else:
                instruction = "sub"
        case 1:
            instruction = "sll"
        case 2:
            instruction = "slt"
        case 3:
            instruction = "sltu"
        case 4:
            instruction = "xor"
        case 5:
            # funct7 value is also needed to determine the exact instruction
            if funct7 == 0:
                instruction = "sra"
            else:
                instruction = "srl"
        case 6:
            instruction = "or"
        case 7:
            instruction = "and"

    rtype = f" x{rd}, x{rs1}, x{rs2}"
    decoded_instruction = rtype
    
    print(f"RISC-V instruction: {decoded_instruction}")
    return instruction_data, cycle_data

def decodeI_LType(encoded_instruction, instruction_data, cycle_data):
    '''
    decode I-type load instructions
    '''
    # print("I-type (load)")

    # extract fields 
    rd = (encoded_instruction >> 7) & 0x1F
    funct3 = (encoded_instruction >> 12) & 0x7
    rs1 = (encoded_instruction >> 15) & 0x1F
    immediate = (encoded_instruction >> 20) & 0xFFF

    # sign-extend 12-bit immediate
    if immediate & 0x800:
        immediate = immediate - (1 << 12)
    
    # determine instruction using funct3
    opcode_map = {
        0: 'lb', 1: 'lh', 2: 'lw', 4: 'lbu', 5: 'lhu'
    }

    instruction = opcode_map.get(funct3, 'tbd')

    i_ltype = f"{instruction} x{rd}, {immediate}(x{rs1})"
    decoded_instruction = i_ltype

    print(f"RISC-V instruction: {decoded_instruction}")

    ##### store fields in instruction_data #####
    instruction_data["Instr"] = str(instruction)
    instruction_data["Rd"] = str(rd)
    instruction_data["Fct3"] = str(funct3)
    instruction_data["Rs1"] = str(rs1)
    instruction_data["Imm"] = str(immediate)

    return instruction_data, cycle_data

def decodeI_AType(encoded_instruction, instruction_data, cycle_data):
    '''
    decode I-type (arithmetic) instructions 
    '''
    # print("I-type (arithmetic)")

    # extract fields
    rd = (encoded_instruction >> 7) & 0x1F
    funct3 = (encoded_instruction >> 12) & 0x7
    rs1 = (encoded_instruction >> 15) & 0x1F
    immediate = (encoded_instruction >> 20) & 0xFFF

    # sign extend 12-bit immediate
    if immediate & 0x800:
        immediate = immediate - (1 << 12)
    
    # use funct3 to determine instruction
    instruction = ""

    match funct3:
        case 0:
            instruction = "addi"
        case 2:
            instruction = "slti"
        case 3:
            instruction = "sltiu"
        case 4:
            instruction = "xori"
        case 6:
            instruction = "ori"
        case 7:
            instruction = "andi"
        case 1 | 5: # I* type instructions
            immediate4_0 = immediate & 0x1F # lower 5 bits
            funct7 = (encoded_instruction >> 25) & 0x7F

            ##### store fields in instruction_data #####
            instruction_data["Fct7"] = str(funct7)

            # determine instruction using funct3 and funct7
            if funct3 == 1:
                instruction = 'slli'
            elif funct7 == 0:
                instruction = 'srli'
            else:
                instruction = 'srai'
        
    i_atype = f"{instruction} x{rd}, x{rs1}, {immediate}"  
    decoded_instruction = i_atype

    print(f"RISC-V instruction: {decoded_instruction}")

    ##### store fields in instruction_data #####
    instruction_data["Instr"] = str(instruction)
    instruction_data["Rd"] = str(rd)
    instruction_data["Fct3"] = str(funct3)
    instruction_data["Rs1"] = str(rs1)
    instruction_data["Imm"] = str(immediate)

    return instruction_data, cycle_data

def decodeSType(encoded_instruction, instruction_data, cycle_data):
    '''
    decode S-type instruction
    syntax: opcode rs2, immediate(rs1)
    '''
    # print("S-type")

    # extract fields
    immediate4_0 = (encoded_instruction >> 7) & 0x1F
    funct3 = (encoded_instruction >> 12) & 0x7
    rs1 = (encoded_instruction >> 15) & 0x1F
    rs2 = (encoded_instruction >> 20) & 0x1F
    immediate11_5 = (encoded_instruction >> 25) & 0x7F

    # reconstruct immediate
    immediate = (immediate11_5 << 5) | immediate4_0

    # sign extend 12-bit immediate
    if immediate & 0x800:
        immediate = immediate - (1 << 12)

    # based on funct3, determine the exact instruction
    opcode_map = {
        0: 'sb', 1: 'sh', 2: 'sw'
    }

    instruction = opcode_map.get(funct3, 'tbd')
    stype = f"{instruction} x{rs2}, {immediate}(x{rs1})"
    decoded_instruction = stype

    print(f"RISC-V instruction: {decoded_instruction}")

    ##### store fields in instruction_data #####
    instruction_data["Instr"] = str(instruction)
    instruction_data["Fct3"] = str(funct3)
    instruction_data["Rs1"] = str(rs1)
    instruction_data["Rs2"] = str(rs2)
    instruction_data["Imm"] = str(immediate)

    return instruction_data, cycle_data

def decodeSBType(encoded_instruction, instruction_data, cycle_data):
    '''
    decode SB-type instruction
    syntax: opcode rs1, rs2, immediate
    '''
    # print("SB-type")

    # extract fields
    immediate11 = (encoded_instruction >> 7) & 0x1
    immediate4_1 = (encoded_instruction >> 8) & 0xF
    funct3 = (encoded_instruction >> 12) & 0x7
    rs1 = (encoded_instruction >> 15) & 0x1F
    rs2 = (encoded_instruction >> 20) & 0x1F
    immediate10_5 = (encoded_instruction >> 25) & 0x3F
    immediate12 = (encoded_instruction >> 31) & 0x1

    # reconstruct the immediate
    immediate = (immediate12 << 12) | (immediate11 << 11) | (immediate10_5 << 5) | (immediate4_1 << 1)

    # sign extend 12-bit immediate
    if immediate & 0x1000:
        immediate = immediate - (1 << 13)

    # determine instruction using funct3
    opcode_map = {
        0: 'beq', 1: 'bne', 4: 'blt', 5: 'bge', 6: 'bltu', 7: 'bgeu'
    }

    instruction = opcode_map.get(funct3, 'tbd')
    sbtype = f"{instruction} x{rs1}, x{rs2}, {immediate}"
    decoded_instruction = sbtype

    print(f"RISC-V instruction: {decoded_instruction}")
    return instruction_data, cycle_data

def decodeUType(encoded_instruction, opcode, instruction_data, cycle_data):
    '''
    decode U-type instruction
    syntax: opcode, rd, immediate
    '''
    # print("U-type")

    # extract fields
    rd = (encoded_instruction >> 7) & 0x1F
    immediate = (encoded_instruction >> 12) & 0xFFFFF

    immediate_32bit = immediate << 12 

    # determine instruction based on opcode
    if opcode == 0x37:
        instruction = "lui"
    elif opcode == 0x17:
        instruction = "auipc"

    utype = f"{instruction} x{rd}, {immediate_32bit}"
    decoded_instruction = utype

    print(f"RISC-V instruction: {decoded_instruction}")
    return instruction_data, cycle_data