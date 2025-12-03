'''
CS4200-001 Computer Architecture I 
Hazards Assignment 
Sam Allen 

This program will simulate how instructions are processed in 
various scenarios, such as for an unrolled loop, when branching, 
when hazards are encountered, and in dynamic scheduling.
'''

'''
SECTION 1.1 CODE WITH 5-STAGES 
'''

from Assembler import *
from FiveStagePipeline import *
from FiveStagePipeline import PipelineStages

def main():
    file = 'Disassembler/risc-v_instructions.bin'
    print("\nReading from file " + file + "...")
    instructions_as_bytes = np.fromfile(file, dtype=np.int32)

    myPipeline = PipelineStages()

    for encoded_instruction in instructions_as_bytes:
        myPipeline.Fetch(encoded_instruction)
        myPipeline.Decode(encoded_instruction)
    return 0

if __name__ == "__main__":
    main()

'''
SECTION 1.2 UNROLLED SIMULATION 
'''

'''
SECTION 1.3 BRANCH SIMULATION 
'''

'''
SECTION 1.4 HAZARDS SIMULATION 
'''

'''
SECTION 1.5 DYNAMIC SCHEDULING 
'''