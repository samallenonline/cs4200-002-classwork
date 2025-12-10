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

    file_name = "Hazards/BinaryResults/unrolled_sim.bin"
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
                instruction_data, cycle_data = myPipeline.Memory(instruction_data, cycle_data)
            elif stage_num == 5:
                cycle_data["Stage"] = stage_name
                instruction_data, cycle_data = myPipeline.WriteBack(instruction_data, cycle_data)

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

    file_name = "Hazards/BinaryResults/branching_sim.bin"
    # allowed to hardcore the address pointed to by the label 
    # Loop: = 64
    label = {"Label:": 64}
    # bne x5, x0, Loop = bne x5, x0, 64

    instructions = ["lw x7, 0(x10)", "addi x5, x0, 3", label, "lw x6, 0(x7)", "addi x6, x6, 1", 
        "sw x6, 0(x7)", "addi x7, x7, 4", "addi x5, x5, -1", "bne x5, x0, 64"]
    
    # encode instructions
    print("ENCODING...")
    for instruction in instructions:
        encoded_instruction = encodeInstruction(instruction)
        encoded_instruction = binaryToString(encoded_instruction)

        # if is a label
        if (isinstance(instruction, dict)):
            memory_address = encoded_instruction["Label:"]
            print(f"Binary instruction: {bin(memory_address)}")
            print("> This value has been shifted to ensure correct decoding")
        else:
            print(f"Binary instruction: {encoded_instruction}")

        writeEncoded(encoded_instruction, file_name)
        print("\n")

    print("Reading from file " + file_name + "...\n")
    instructions_as_bytes = np.fromfile(file_name, dtype=np.int32)

    myPipeline = PipelineStages()

    # create list to hold dictionaries for all instructions in the program 
    program_data = []
    cycle_num = 0

    # variables for looping logic 
    loopFinished = False
    # register x5 is being used as the counter. this register is initialized
    # with the value 3 in the second instruction, addi x5, x0, 3.
    loopCounter = 3 
    loopIteration = 0
    instructionIndex = 0
    
    while (not loopFinished):
        # enter pipeline — decode instructions
        print("DECODING...")
        while instructionIndex < len(instructions_as_bytes):
            encoded_instruction = instructions_as_bytes[instructionIndex]

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
                elif stage_num == 3 and instruction_data["Instr"] != "Label:":
                    cycle_data["Stage"] = stage_name
                    instruction_data, cycle_data = myPipeline.Execute(instruction_data, cycle_data)
                elif stage_num == 4 and instruction_data["Instr"] != "Label:":
                    cycle_data["Stage"] = stage_name
                    instruction_data, cycle_data = myPipeline.Memory(instruction_data, cycle_data)
                elif stage_num == 5 and instruction_data["Instr"] != "Label:":
                    cycle_data["Stage"] = stage_name
                    instruction_data, cycle_data = myPipeline.WriteBack(instruction_data, cycle_data)

                # update only if value is empty (avoids overwriting issue)
                for key in instruction_data:
                    if instruction_data[key] not in ["", None]:
                        cycle_data[key] = instruction_data[key]

                # append row (representing instruction data)
                program_data.append(cycle_data)
                
                # if any bne is reached, jump to label
                if cycle_data["Instr"] == "bne" and cycle_data["Stage"] == "Write Back":     # reached the bne instruction
                    print("> Loop iteration = ", loopIteration)
                    print("> Register x5 (counter) = ", loopCounter)
                    
                    # prepare for jump 
                    instructionIndex = 3 # lw x6, 0(x7)

                    # if counter equals 0
                    if loopCounter == 0:
                        loopFinished = True
                        break   
                    else:
                        loopCounter -= 1
                
            
            # move to next instruction
            # instructionIndex += 1
            
            if instruction_data["Instr"] != "bne":
                instructionIndex += 1
            
            if loopFinished:
                break    
        # break out of while
        if instructionIndex >= len(instructions_as_bytes):
            loopFinished = True
    
    # set up csv file 
    with open('Hazards/CSVResults/branching_sim.csv', 'w', newline='') as csvfile:
        fieldnames = ['Stage', 'Cycle', 'Instr', 'Op', 'Fct3', 'Fct7', 'Rd', 'Rs1', 'Rs2', 'Imm', 'RegWrite', 'ALUSrc', 'FwdA', 'FwdB',
        'MemRd', 'MemWr', 'WBSel', 'bne']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(program_data)

    '''
    SECTION 1.4 HAZARDS SIMULATION 
    '''
    print("\n########## SECTION 1.4 HAZARDS SIMULATION ##########\n")

    file_name = "Hazards/BinaryResults/hazards_sim.bin"
    instructions = ["sub x2, x1, x3", "and x12, x2, x5", "or x13, x6, x2", "and x2, x12, x13", 
        "add x14, x2, x2"]

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

                # determine if forwarding is needed by checking previous 2 instructions
                # initialize to 00, will get rewritten if forwarding is needed
                cycle_data["FwdA"] = cycle_data["FwdB"] = "00"

                # check 1 instruction prior
                if instruction_data["Rs1"] == program_data[cycle_num-3]["Rd"]:
                    cycle_data["FwdA"] = "10"
                if instruction_data["Rs2"] == program_data[cycle_num-3]["Rd"]:
                    cycle_data["FwdB"] = "10"

                # check 2 instructions prior
                if cycle_num > 8:
                    if instruction_data["Rs1"] == program_data[cycle_num-8]["Rd"]:
                        cycle_data["FwdA"] = "01"
                    if instruction_data["Rs2"] == program_data[cycle_num-8]["Rd"]:
                        cycle_data["FwdB"] = "01"

                # if contain hazards, set appropriate forward signals
            elif stage_num == 3:
                cycle_data["Stage"] = stage_name
                instruction_data, cycle_data = myPipeline.Execute(instruction_data, cycle_data)
            elif stage_num == 4:
                cycle_data["Stage"] = stage_name
                instruction_data, cycle_data = myPipeline.Memory(instruction_data, cycle_data)
            elif stage_num == 5:
                cycle_data["Stage"] = stage_name
                instruction_data, cycle_data = myPipeline.WriteBack(instruction_data, cycle_data)

            # update only if value is empty (avoids overwriting issue)
            for key in instruction_data:
                if instruction_data[key] not in ["", None]:
                    cycle_data[key] = instruction_data[key]

            # append row (representing instruction data)
            program_data.append(cycle_data)


    # set up csv file 
    with open('Hazards/CSVResults/hazards_sim.csv', 'w', newline='') as csvfile:
        fieldnames = ['Stage', 'Cycle', 'Instr', 'Op', 'Fct3', 'Fct7', 'Rd', 'Rs1', 'Rs2', 'Imm', 'RegWrite', 'ALUSrc', 'FwdA', 'FwdB',
        'MemRd', 'MemWr', 'WBSel', 'bne']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(program_data)

    '''
    SECTION 1.5 DYNAMIC SCHEDULING 
    '''
    print("\n########## SECTION 1.5 DYNAMIC SCHEDULING ##########\n")

    # read from text file
    file_name = "Hazards/Input/dynamic_scheduling.txt"
    print("Reading from file " + file_name + "...\n")
    with open(file_name, 'r') as file:
        instructions = file.read().splitlines()

    # encode instructions
    file_name = "Hazards/BinaryResults/dynamic_scheduling.bin"
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
                instruction_data, cycle_data = myPipeline.Memory(instruction_data, cycle_data)
            elif stage_num == 5:
                cycle_data["Stage"] = stage_name
                instruction_data, cycle_data = myPipeline.WriteBack(instruction_data, cycle_data)

            # update only if value is empty (avoids overwriting issue)
            for key in instruction_data:
                if instruction_data[key] not in ["", None]:
                    cycle_data[key] = instruction_data[key]

            # append row (representing instruction data)
            program_data.append(cycle_data)

    # set up csv file 
    with open('Hazards/CSVResults/dynamic_scheduling.csv', 'w', newline='') as csvfile:
        fieldnames = ['Stage', 'Cycle', 'Instr', 'Op', 'Fct3', 'Fct7', 'Rd', 'Rs1', 'Rs2', 'Imm', 'RegWrite', 'ALUSrc', 'FwdA', 'FwdB',
        'MemRd', 'MemWr', 'WBSel', 'bne']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(program_data)

    return 0

if __name__ == "__main__":
    main()
