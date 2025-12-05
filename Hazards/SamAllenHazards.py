'''
CS4200-001 Computer Architecture I 
Hazards Assignment 
Sam Allen 

This program will simulate how instructions are processed in 
various scenarios, such as for an unrolled loop, when branching, 
when hazards are encountered, and in dynamic scheduling.
'''

import csv
from Assembler import *
from FiveStagePipeline import *
from FiveStagePipeline import PipelineStages

def main():
    '''
    SECTION 1.1 CODE WITH 5-STAGES 
    '''
    print("\n########## SECTION 1.1 CODE WITH 5-STAGES ##########\n")
    
    ### ASSEMBLER/DISASSEMBLER TESTING ###
    '''

    file_name = 'Hazards/BinaryResults/test.bin'
    instructions = ["lw x7, 0(x10)", "addi x5, x0, 3", "lw x6, 0(x7)", "xori x6, x6, 32", "sw x6, 0(x7)", 
        "addi x7, x7, 4", "addi x5, x5, -1", "bne x5, x0, -40"]

    important_segments = []

    # encode instructions
    print("ENCODING...")
    for instruction in instructions:
        encoded_instruction = encodeInstruction(instruction)
        encoded_instruction = binaryToString(encoded_instruction)
        print(f"Binary instruction: {encoded_instruction}")
        writeEncoded(encoded_instruction, file_name)

        print("\n")

    print("Reading from file " + file_name + "...\n")
    instructions_as_bytes = np.fromfile(file_name, dtype=np.int32)

    myPipeline = PipelineStages()

    # enter pipeline — decode instructions
    print("DECODING...")
    for encoded_instruction in instructions_as_bytes:
        myPipeline.Fetch(encoded_instruction, important_segments)
        myPipeline.Decode(encoded_instruction, important_segments)
     
    ###
    '''

    '''
    SECTION 1.2 UNROLLED SIMULATION 
    '''
    print("\n########## SECTION 1.2 UNROLLED SIMULATION ##########\n")

    file_name = "Hazards/BinaryResults/unrolled_sim.bin"
    instructions = ["lw x7, 0(x10)", "lw x6, 0(x7)", "addi x6, x6, 1", "sw x6, 0(x7)", "lw x6, 4(x7)", 
        "addi x6, x6, 1", "sw x6, 4(x7)", "lw x6, 8(x7)", "addi x6, x6, 1", "sw x6, 8(x7)"]

    # encode instructions
    print("ENCODING...")
    for instruction in instructions:
        encoded_instruction = encodeInstruction(instruction)
        encoded_instruction = binaryToString(encoded_instruction)
        print(f"Binary instruction: {encoded_instruction}")
        writeEncoded(encoded_instruction, file_name)

        print("\n")

    print("Reading from file " + file_name + "...\n")
    instructions_as_bytes = np.fromfile(file_name, dtype=np.int32)

    myPipeline = PipelineStages()

    # create list to hold dictionaries for all instructions in the program 
    program_data = []
    cycle_num = 0

    # enter pipeline — decode instructions
    print("DECODING...")
    for encoded_instruction in instructions_as_bytes:
        # create initial dictionary for instruction
        instruction_data = {
            "Stage": "",    # added this
            "Cycle": "",
            "Instr": "",
            "Op": "",
            "Fct3": "",
            "Fct7": "", # added this 
            "Rd": "",
            "Rs1": "",
            "Rs2": "",
            "Imm": "",  # added this
            "RegWrite": "",
            "ALUSrc": "",
            "FwdA": "",
            "FwdB": "",
            "MemRd": "",
            "MemWr": "",
            "WBSel": "",
            "bne": ""
        }
        
        for stage_num, stage_name in enumerate(["Fetch", "Decode", "Execute", "Memory", "Write Back" ], 1):
            cycle_num += 1  # increment cycle

            # create initial dictionary for cycle data
            cycle_data = instruction_data.copy()
            # set stage and cycle
            cycle_data["Stage"] = stage_name
            cycle_data["Cycle"] = cycle_num

            if stage_num == 1:
                cycle_data["Stage"] = stage_name
                instruction_data, cycle_data = myPipeline.Fetch(encoded_instruction, instruction_data, cycle_data)
            elif stage_num == 2:
                cycle_data["Stage"] = stage_name
                instruction_data, cycle_data = myPipeline.Decode(encoded_instruction, instruction_data, cycle_data)
            elif stage_num == 3:
                cycle_data["Stage"] = stage_name
                instruction_data, cycle_data = myPipeline.Execute(instruction_data, cycle_data)
            elif stage_num == 4:
                cycle_data["Stage"] = stage_name
                cycle_data = myPipeline.Memory(instruction_data, cycle_data)
            elif stage_num == 5:
                cycle_data["Stage"] = stage_name
                instruction_data, cycle_data = myPipeline.WriteBack(instruction_data, cycle_data)

            print("PRINTING CYCLE DATA")
            print(cycle_data)

            # update only if value is empty (avoids overwriting issue)
            for key in instruction_data:
                if instruction_data[key] not in ["", None]:
                    cycle_data[key] = instruction_data[key]

            # append row (representing instruction data)
            program_data.append(cycle_data)

    # set up csv file 
    with open('Hazards/CSVResults/unrolled_sim.csv', 'w', newline='') as csvfile:
        fieldnames = ['Stage', 'Cycle', 'Instr', 'Op', 'Fct3', 'Fct7', 'Rd', 'Rs1', 'Rs2', 'Imm', 'RegWrite', 'ALUSrc', 'FwdA', 'FwdB',
        'MemRd', 'MemWr', 'WBSel', 'bne']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(program_data)
    
    '''
    SECTION 1.3 BRANCH SIMULATION 
    '''
    print("\n########## SECTION 1.3 BRANCH SIMULATION ##########\n")

    file_name = "Hazards/branching_sim.bin"
    instructions = ["lw x7, 0(x10)", "addi x5, x0, 3", "Loop:", "lw x6, 0(x7)", "addi x6, x6, 1", 
        "sw x6, 0(x7)", "addi x7, x7, 4", "addi x5, x5, -1", "bne x5, x0, Loop"]

    '''
    SECTION 1.4 HAZARDS SIMULATION 
    '''
    print("\n########## SECTION 1.4 HAZARDS SIMULATION ##########\n")

    file_name = "Hazards/hazards_sim.bin"
    instructions = ["sub x2, x1, x3", "and x12, x2, x5", "or x13, x6, x2", "and x2, x12, x13", 
        "add x14, x2, x2"]

    '''
    SECTION 1.5 DYNAMIC SCHEDULING 
    '''
    print("\n########## SECTION 1.5 DYNAMIC SCHEDULING ##########\n")

    file_name = "Hazards/scheduling_sim.bin"

    return 0

if __name__ == "__main__":
    main()
