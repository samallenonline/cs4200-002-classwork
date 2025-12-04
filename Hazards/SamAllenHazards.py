'''
CS4200-001 Computer Architecture I 
Hazards Assignment 
Sam Allen 

This program will simulate how instructions are processed in 
various scenarios, such as for an unrolled loop, when branching, 
when hazards are encountered, and in dynamic scheduling.
'''

from Assembler import *
from FiveStagePipeline import *
from FiveStagePipeline import PipelineStages

def main():
    '''
    SECTION 1.1 CODE WITH 5-STAGES 
    '''
    print("\n########## SECTION 1.1 CODE WITH 5-STAGES ##########\n")
    
    # ASSEMBLER/DISASSEMBLER TESTING
    file = 'Hazards/test.bin'
    print("Reading from file " + file + "...")
    instructions_as_bytes = np.fromfile(file, dtype=np.int32)

    myPipeline = PipelineStages()

    for encoded_instruction in instructions_as_bytes:
        myPipeline.Fetch(encoded_instruction)
        myPipeline.Decode(encoded_instruction)

    '''
    SECTION 1.2 UNROLLED SIMULATION 
    '''
    print("\n########## SECTION 1.2 UNROLLED SIMULATION ##########\n")

    instructions = ["lw x7, 0(x10)", "lw x6, 0(x7)", "addi x6, x6, 1", "sw x6, 0(x7)", "lw x6, 4(x7)", 
        "addi x6, x6, 1", "sw x6, 4(x7)", "lw x6, 8(x7)", "addi x6, x6, 1", "sw x6, 8(x7)"]

    file_name = "unrolled_sim.bin"

    for instruction in instructions:
        encoded_instruction = encodeInstruction(instruction)
        encoded_instruction = binaryToString(encoded_instruction)
        print(encoded_instruction)
        writeEncoded(encoded_instruction, file_name)

        print("\n")

    '''
    SECTION 1.3 BRANCH SIMULATION 
    '''
    print("\n########## SECTION 1.3 BRANCH SIMULATION ##########\n")

    instructions = ["lw x7, 0(x10)", "addi x5, x0, 3", "Loop:", "lw x6, 0(x7)", "addi x6, x6, 1", 
        "sw x6, 0(x7)", "addi x7, x7, 4", "addi x5, x5, -1", "bne x5, x0, Loop"]

    '''
    SECTION 1.4 HAZARDS SIMULATION 
    '''
    print("\n########## SECTION 1.4 HAZARDS SIMULATION ##########\n")

    instructions = ["sub x2, x1, x3", "and x12, x2, x5", "or x13, x6, x2", "and x2, x12, x13", 
        "add x14, x2, x2"]

    '''
    SECTION 1.5 DYNAMIC SCHEDULING 
    '''
    print("\n########## SECTION 1.5 DYNAMIC SCHEDULING ##########\n")

    return 0

if __name__ == "__main__":
    main()