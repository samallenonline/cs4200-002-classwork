''' 
This program contains the class which simulates the 5-stage 
pipeline for RISC-V instructions.
'''

import numpy as np
from Disassembler import *
from Disassembler import decodeInstruction
from FiveStages.Execute import *
from FiveStages.Memory import *

class PipelineStages:
    '''
    this class simulates the 5-stage pipeline, including methods for 
    each stage (referencing code from my previously written dissasembler)
    '''
    # class attributes 
    programCounter = 0
    branchingCounter = 0
    lastTwoInstructions = []

    # methods 
    def Fetch(self, encoded_instruction, instruction_data, cycle_data):
        # obtain encoded instruction based on program counter 
        # store instruction
        print("\nBinary instruction: " + np.binary_repr(encoded_instruction)) # for debugging

        self.programCounter += 1 # increment program counter 
        return instruction_data, cycle_data

    def Decode(self, encoded_instruction, instruction_data, cycle_data):
        # decode the fetched instruction 
        instruction_data, cycle_data = decodeInstruction(encoded_instruction, instruction_data, cycle_data)

        return instruction_data, cycle_data

    def Execute(self, instruction_data, cycle_data):
        # operation specified by the instruction is performed 
        # (arithmetic, calculate memory address, etc.)

        # handle based on opcode 
        opcode = instruction_data["Op"]

        if opcode == 0x33: # R-type instruction
            return executeRType(instruction_data, cycle_data)
        elif opcode == 0x03: # I-type instruction (load)
            return executeI_LType(instruction_data, cycle_data)
        elif opcode == 0x13: # I-type instruction (arithmetic)
            return executeI_AType(instruction_data, cycle_data)
        elif opcode == 0x23: # S-type instruction
            return executeSType(instruction_data, cycle_data)
        elif opcode == 0x63: # SB-type instruction 
            return executeSBType(instruction_data, cycle_data)
        elif opcode == 0x37 or opcode == 0x17: # U-type instruction
            return executeUType(instruction_data, cycle_data)
        else:
            raise ValueError(f"Could not identify instruction type: {opcode}")
    
    def Memory(self, instruction_data, cycle_data):
        # only useful for instructions that need access to memory
        # reads from memory or writes to memory

        # handle based on opcode 
        opcode = instruction_data["Op"]

        if opcode == 0x33: # R-type instruction
            return memoryRType(cycle_data)
        elif opcode == 0x03: # I-type instruction (load)
            return memoryI_LType(cycle_data)
        elif opcode == 0x13: # I-type instruction (arithmetic)
            return memoryI_AType(cycle_data)
        elif opcode == 0x23: # S-type instruction
            return memorySType(cycle_data)
        elif opcode == 0x63: # SB-type instruction 
            return memorySBType(cycle_data)
        elif opcode == 0x37 or opcode == 0x17: # U-type instruction
            return memoryUType(cycle_data)
        else:
            raise ValueError(f"Could not identify instruction type: {opcode}")
    
    def WriteBack(self, instruction_data, cycle_data):
        # write result to register file
        return instruction_data, cycle_data