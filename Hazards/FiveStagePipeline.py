''' 
This program contains the class which simulates the 5-stage 
pipeline for RISC-V instructions.
'''

import numpy as np
from Disassembler import *
from Disassembler import decodeInstruction

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
    def Fetch(self, encoded_instruction):
        # obtain encoded instruction based on program counter 
        # store instruction
        print("\nBinary instruction: " + np.binary_repr(encoded_instruction)) # for debugging

        self.programCounter += 1 # increment program counter 
        return 0

    def Decode(self, encoded_instruction):
        # decode the fetched instriction 
        decodeInstruction(encoded_instruction)

        return 0

    def Execute(self, instruction):
        # operation specified by the instruction is performed 
        # (arithmetic, calculate memory address, etc.)
        return 0
    
    def Memory(self, instruction):
        # only useful for instructions that need access to memory
        # reads from memory or writes to memory
        return 0 
    
    def WriteBack(self, instruction):
        # write result to register file
        return 0