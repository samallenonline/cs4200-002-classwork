''' 
This program will serve as a dissasembler for RISC-V instructions.
It will read binary encoded instructions, interpret them, and present
them back to the user in a human readable assembly language. 

Note: This dissasembler only works for R, I, I*, S, SB, and U type 
instructions. 
'''
import numpy as np

file = 'risc-v_instructions.bin'

# ask user if they want to read from specified file
#user_choice = input("\nDo you wish to decode instructions from " + file + "? (Y/N) ")
#if user_choice == "n" or user_choice == "N":
#    print("Goodbye!\n")
#    exit()
    
print("\nReading from file " + file + "...")
instructions_as_bytes = np.fromfile(file, dtype=np.int32)
# with open('risc-v_instructions.bin', 'rb') as rv_instrs:
#     binary_instructions = rv_instrs.read()
# print(bin(binary_instructions[0]))

# for every instruction in the file, process and interpret
for encoded_instruction in instructions_as_bytes:
    print("\nBinary instruction: " + np.binary_repr(encoded_instruction)) # for debugging

    # then, extract the opcode
    opcode = encoded_instruction & 0x7F
    #print(bin(opcode)) # for debugging
    
    length = len(np.binary_repr(encoded_instruction))
    padding = 32 - length
    #print("padding needed = " + str(padding))

    # using the opcode, determine the instruction type
    decoded_instruction = " "
    match opcode:
        case 51:
            # print("R-type")

            # check if instruction is negative 
            if (encoded_instruction >> 31) == -1:
                # generate a mask to use for sign extension 
                mask = (0xFFFFFFFF << length - 1) & 0xFFFFFFFF
                #print("mask = " + str(np.binary_repr(mask))) # for debugging

                encoded_instruction = np.int64(encoded_instruction) # to resolve issues with overflow
                encoded_instruction = encoded_instruction ^ mask
                #print(str(np.binary_repr(encoded_instruction)))
                encoded_instruction = np.int32(encoded_instruction)
            
            # extract the rd field and process 
            rd = (encoded_instruction >> 7) & 0x1F
            #print(bin(rd))

            # extract the funct3 field and process 
            funct3 = (encoded_instruction >> 12) & 0x7
            #print(bin(funct3))

            # extract the rs1 field and process 
            rs1 = (encoded_instruction >> 15) & 0x1F
            #print(bin(rs1))

            # extract the rs2 field and process 
            rs2 = (encoded_instruction >> 20) & 0x1F
            #print(bin(rs2))

            # extract the funct7 field and process
            funct7 = (encoded_instruction >> 25) & 0x7F
            #print(bin(funct7))

            # based on funct3, determine the exact instruction
            instruction = ""
            rtype = " x" + str(rd) + ", x" + str(rs1) + ", x" + str(rs2) + ""
            match funct3:
                case 0:
                    if funct7 == 0:
                        instruction = "add"
                        decoded_instruction = instruction + rtype
                    else:
                        instruction = "sub"
                        decoded_instruction = instruction + rtype
                case 1:
                    instruction = "sll"
                    decoded_instruction = instruction + rtype
                case 2:
                    instruction = "slt"
                    decoded_instruction = instruction + rtype
                case 3:
                    instruction = "sltu"
                    decoded_instruction = instruction + rtype
                case 4:
                    instruction = "xor"
                    decoded_instruction = instruction + rtype
                case 5:
                    # funct7 value is also needed to determine the exact instruction
                    if funct7 == 0:
                        instruction = "sra"
                        decoded_instruction = instruction + rtype
                    else:
                        instruction = "srl"
                        decoded_instruction = instruction + rtype
                case 6:
                    instruction = "or"
                    decoded_instruction = instruction + rtype
                case 7:
                    instruction = "and"
                    decoded_instruction = instruction + rtype

            # return decoded instruction
            #print(instruction)
            print("RISC-V instruction: " + str(decoded_instruction)) # for debugging 

        case 3 | 19: 
            #print("I-type")

            # check if instruction is negative 
            if (encoded_instruction >> 31) == -1:
                # generate a mask to use for sign extension 
                mask = (0xFFFFFFFF << length - 1) & 0xFFFFFFFF
                #print("mask = " + str(np.binary_repr(mask))) # for debugging

                encoded_instruction = np.int64(encoded_instruction) # to resolve issues with overflow
                encoded_instruction = encoded_instruction ^ mask
                #print(str(np.binary_repr(encoded_instruction)))
                encoded_instruction = np.int32(encoded_instruction)

            # extract the rd field and process
            rd = (encoded_instruction >> 7) & 0x1F
            #print(bin(rd)) # for debugging
            
            # extract the funct3 field and process 
            funct3 = (encoded_instruction >> 12) & 0x7
            #print(bin(funct3))

            # extract the rs1 field and process 
            rs1 = (encoded_instruction >> 15) & 0x1F
            #print(bin(rs1))

            # extract the immediate field and process (signed)
            immediate = (encoded_instruction >> 20) & 0xFFF
            #print(bin(immediate))

            # based on opcode and funct3, determine the exact instruction
            instruction = ""
            if opcode == 3:
                #print("I-Type: Load")
                itype_load = " x" + str(rd) + " " + str(immediate) + "(x" + str(rs1) + ")"

                match funct3:
                    case 0:
                        instruction = "lb"
                        decoded_instruction = instruction + itype_load
                    case 1: 
                        instruction = "lh"
                        decoded_instruction = instruction + itype_load
                    case 2:
                        instruction = "lw"
                        decoded_instruction = instruction + itype_load
                    case 4:
                        instruction = "lbu"
                        decoded_instruction = instruction + itype_load
                    case 5:
                        instruction = "lhu"
                        decoded_instruction = instruction + itype_load

            if opcode == 19:
                #print("I-Type: Arithmetic")
                itype_arithmetic = " x" + str(rd) + ", x" + str(rs1) + ", " + str(immediate)

                match funct3:
                    case 0:
                        instruction = "addi"
                        decoded_instruction = instruction + itype_arithmetic
                    case 1: # I* type instruction
                        instruction = "slli"
                        decoded_instruction = instruction + itype_arithmetic
                    case 2:
                        instruction = "slti"
                        decoded_instruction = instruction + itype_arithmetic
                    case 3:
                        instruction = "sltiu"
                        decoded_instruction = instruction + itype_arithmetic
                    case 4:
                        instruction = "xori"
                        decoded_instruction = instruction + itype_arithmetic
                    case 5: # I* type instructions
                        #print("I* Type")
                        # re-extract bits 20-31

                        # extract immediate[4:0] field and process 
                        immediate4_0 = (encoded_instruction >> 20) & 0x7F
                        #print(bin(immediate4_0))

                        # extract funct7 field and process
                        funct7 = (encoded_instruction >> 25) & 0x7F
                        #print(bin(funct7))

                        if funct7 == 0:
                            instruction = "srli"
                            decoded_instruction = instruction + itype_arithmetic
                        else:
                            instruction = "srai"
                            decoded_instruction = instruction + itype_arithmetic
                    case 6:
                        instruction = "ori"
                        decoded_instruction = instruction + itype_arithmetic
                    case 7:
                        instruction = "andi"
                        decoded_instruction = instruction + itype_arithmetic
        
            # return decoded instruction
            #print(instruction)
            print("RISC-V instruction: " + str(decoded_instruction)) # for debugging 

        case 35:
            #print("S-type")

            # check if instruction is negative 
            if (encoded_instruction >> 31) == -1:
                # generate a mask to use for sign extension 
                mask = (0xFFFFFFFF << length - 1) & 0xFFFFFFFF
                #print("mask = " + str(np.binary_repr(mask))) # for debugging

                encoded_instruction = np.int64(encoded_instruction) # to resolve issues with overflow
                encoded_instruction = encoded_instruction ^ mask
                #print(str(np.binary_repr(encoded_instruction)))
                encoded_instruction = np.int32(encoded_instruction)

            # extract the rd field and process 
            rd = (encoded_instruction >> 7) & 0x1F
            #print(bin(rd))

            # extract the funct3 field and process 
            funct3 = (encoded_instruction >> 12) & 0x7
            #print(bin(funct3))

            # extract the rs1 field and process 
            rs1 = (encoded_instruction >> 15) & 0x1F
            #print(bin(rs1))

            # extract the rs2 field and process 
            rs2 = (encoded_instruction >> 20) & 0x1F
            #print(bin(rs2))

            # extract the immediate field and process
            immediate = (encoded_instruction >> 25) & 0x7F
            #print(bin(immediate))

            # based on funct3, determine the exact instruction
            instruction = ""
            stype = " x" + str(rs2) + " " + str(immediate) + "(x" + str(rs1) + ")"

            match funct3:
                case 0:
                    instruction = "sb"
                    decoded_instruction = instruction + stype
                case 1:
                    instruction = "sh"
                    decoded_instruction = instruction + stype
                case 2:
                    instruction = "sw"
                    decoded_instruction = instruction + stype

            # return decoded instruction
            #print(instruction)
            print("RISC-V instruction: " + str(decoded_instruction)) # for debugging 

        case 99:
            #print("SB-type")

            # (had a really difficult time with this section)
            # check if instruction is negative 
            if (encoded_instruction >> 31) == -1:
                # generate a mask to use for sign extension 
                mask = (0xFFFFFFFF << length - 1) & 0xFFFFFFFF
                #print("mask = " + str(np.binary_repr(mask))) # for debugging

                encoded_instruction = np.int64(encoded_instruction) # to resolve issues with overflow
                encoded_instruction = encoded_instruction ^ mask
                #print(str(np.binary_repr(encoded_instruction)))
                encoded_instruction = np.int32(encoded_instruction)

            # extract the immediate[11] field and process 
            immediate11 = (encoded_instruction >> 7) & 0x1
            #print("immediate11 = " + str(bin(immediate11)))

            # extract the immediate[4:1] field and process
            immediate4_1 = (encoded_instruction >> 8) & 0xF
            #print(bin(immediate4_1))

            # extract the funct3 field and process
            funct3 = (encoded_instruction >> 12) & 0x7
            #print(bin(funct3))

            # extract the rs1 field and process 
            rs1 = (encoded_instruction >> 15) & 0x1F
            #print(bin(rs1))

            # extract the rs2 field and process 
            rs2 = (encoded_instruction >> 20) & 0x1F
            #print(bin(rs2))

            # extract the immediate[10:5] field and process 
            immediate10_5 = (encoded_instruction >> 26) & 0x3F
            #print(bin(immediate10_5))

            # extract the immediate[12] field and process 
            immediate12 = (encoded_instruction >> 27) & 0x1
            #print(bin(immediate12))
            #print("type of immediate = " + str(type(immediate12)))

            # reconstruct the immediate
            # treat every immediate as a mask so we can xor them all together later 
            immediate4_1 = immediate4_1 << 1 # shifted over one to account for branch offset
            immediate10_5 = immediate10_5 << 5
            immediate11 = immediate11 << 11
            immediate12 = immediate12 << 12
            # print("immediate 4_1 = " + str(np.binary_repr(immediate4_1)))
            # print("immediate 10_5 = " + str(np.binary_repr(immediate10_5)))
            # print("immediate 11 = " + str(np.binary_repr(immediate11)))
            # print("immediate 12 = " + str(np.binary_repr(immediate12)))

            immediate = immediate4_1 ^ immediate10_5 ^ immediate11 ^ immediate12
            #print("immediate = " + str(bin(immediate)))

            # based on funct3, determine the exact instruction
            instruction = ""
            sbtype = " x" + str(rs1) + ", x" + str(rs2) + ", " + str(immediate)

            match funct3:
                case 0:
                    instruction = "beq"
                    decoded_instruction = instruction + sbtype
                case 1: 
                    instruction = "bne"
                    decoded_instruction = instruction + sbtype
                case 4:
                    instruction = "blt"
                    decoded_instruction = instruction + sbtype
                case 5: 
                    instruction = "bge"
                    decoded_instruction = instruction + sbtype
                case 6: 
                    instruction = "bltu"
                    decoded_instruction = instruction + sbtype
                case 7: 
                    instruction = "bgeu"
                    decoded_instruction = instruction + sbtype

            # return decoded instruction
            #print(instruction)
            print("RISC-V instruction: " + str(decoded_instruction)) # for debugging 

        case 55 | 23:
            #print("U-type")

            # check if instruction is negative 
            if (encoded_instruction >> 31) == -1:
                # generate a mask to use for sign extension 
                mask = (0xFFFFFFFF << length - 1) & 0xFFFFFFFF
                #print("mask = " + str(np.binary_repr(mask))) # for debugging

                encoded_instruction = np.int64(encoded_instruction) # to resolve issues with overflow
                encoded_instruction = encoded_instruction ^ mask
                #print(str(np.binary_repr(encoded_instruction)))
                encoded_instruction = np.int32(encoded_instruction)

            # extract the rd field and process 
            rd = (encoded_instruction >> 7) & 0x1F
            #print(bin(rd))

            # extract the immediate field and process 
            immediate = (encoded_instruction >> 12) & 0xFFFFF
            #print(bin(rd))

            # based on opcode, determine the exact instruction
            instruction = ""
            utype = " x" + str(rd) + " " + str(immediate)

            match opcode:
                case 55:
                    instruction = "lui"
                    decoded_instruction = instruction + utype

                case 23: 
                    instruction = "auipc"
                    decoded_instruction = instruction + utype

            # return decoded instruction
            #print(instruction)
            print("RISC-V instruction: " + str(decoded_instruction)) # for debugging 