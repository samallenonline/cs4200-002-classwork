from enum import Enum
import os

import cocotb

from cocotb.clock import Clock
from cocotb.runner import get_runner
from cocotb.triggers import RisingEdge

alu_sim_dir = os.path.abspath(os.path.join('.', 'alu_sim_dir'))

class Funct3(Enum):
    ADD = 0
    SLL = 1
    SLT = 2
    SLTU = 3
    XOR = 4
    SRL = 5
    SRA = 5
    OR = 6
    AND = 7

### PUZZLES ###

async def perform_not(dut) -> None:
    """
    ~

    :param dut: DUT object from cocotb
    :return: None
    """
    # set up inputs 
    # dut.s1.value = user_input # store user input in dut.a 
    dut.s2.value = 0xFFFFFFFF # all 1's
    dut.funct3.value = Funct3.XOR.value # use xor to flip all bits 
    dut.funct7.value = 0

    # tick the clock
    print("clock (perform_not_1) = ", dut.clk.value)
    await RisingEdge(dut.clk)

    print("perform_not:")
    print("s1 value = ", dut.s1.value)
    print("s2 value = ", dut.s2.value)
    print("d value = ", dut.d.value)

    # result stored in dut.d


async def perform_negate(dut) -> None:
    """
    Perform the two's complement.

    :param dut: DUT object from cocotb
    :return: None
    """
    # step 1. flip all bits using perform_not
    # set up inputs 
    # dut.s1.value = user_input
   
    await perform_not(dut) 

    print("clock (perform_negate_1) = ", dut.clk.value)
    await RisingEdge(dut.clk) 

    # step 2. add 1 to the result
    dut.s1.value = dut.d.value
    dut.s2.value = 0x1  # 0x00000001
    dut.funct3.value = Funct3.ADD.value # use add to add 1 

    # tick the clock
    print("clock (perform_negate_2) = ", dut.clk.value)
    await RisingEdge(dut.clk)

    print("perform_negate:")
    print("s1 value = ", dut.s1.value)
    print("s2 value = ", dut.s2.value)
    print("d value = ", dut.d.value)
    
    # result stored in dut.d

async def perform_sub(dut) -> None:
    """
    sub rd, rs1, rs2

    :param dut: Dut object from cocotb
    :param s1: First value as described in R sub
    :param s2: Second value as described in R sub
    :return: None
    """
    # setup inputs 
    # step 1. negate s2

    # print("s1 check = ", dut.s1.value)
    # print("s2 check = ", dut.s2.value)
    temporary = dut.s1.value
    dut.s1.value = dut.s2.value
    dut.s2.value = 0

    await perform_negate(dut)

    # tick the clock 
    print("clock (perform_sub_1) = ", dut.clk.value)
    await RisingEdge(dut.clk) 

    # step 2. add r1 to r2
    dut.s2.value = dut.d.value
    dut.s1.value = temporary
    # dut.s2.value = user_input
    dut.funct3.value = Funct3.ADD.value # use add to add 1 

    # tick the clock
    print("clock (perform_sub_2) = ", dut.clk.value)
    await RisingEdge(dut.clk)

    print("perform_sub:")
    print("s1 value = ", dut.s1.value)
    print("s2 value = ", dut.s2.value)
    print("temp value = ", temporary)
    print("d value = ", dut.d.value)

    # result stored in dut.d


async def set_gt(dut):
    """
    In the same format as slt, rd, rs1, rs2 perform the operation to set the output LSB bit to rs1 > rs2.

    :param dut:
    :return:
    """

    # step 1. switch registers
    # setup inputs 
    temp = dut.s1.value
    dut.s1.value = dut.s2.value
    dut.s2.value = temp

    # step 2. determine if less than
    dut.funct3.value = Funct3.SLT.value # SLT = 2

    # tick the clock
    print("clock (set_gt_5) = ", dut.clk.value)
    await RisingEdge(dut.clk) 

    print("set_gt:")
    print("s1 value = ", dut.s1.value)
    print("s2 value = ", dut.s2.value)
    print("d value = ", dut.d.value)

    # result stored in dut.d


async def set_gte(dut):
    """
    In the same format as slt rd, rs1, rs2 perform the operation to set the output LSB bit to rs1 >= rs2.

    :param dut: DUT object from cocotb
    :return:
    """

    # step 1. check if s1 is greater than s2
    # setup inputs 
    # s1 = user_input1
    # s2 = user_input2
    input1 = dut.s1.value
    input2 = dut.s2.value

    await set_gt(dut)

    # tick the clock 
    print("clock (set_gte_1) = ", dut.clk.value)
    await RisingEdge(dut.clk) 

    # result stored in dut.d
    result1 = dut.d.value
    print("greater than result = ", result1)

    # step 2. check if s1 is equal to s2
    # refresh inputs
    dut.s1.value = input1
    dut.s2.value = input2

    # step 2.1 subtract s1 and s2
    await perform_sub(dut)

    # tick the clock 
    print("clock (set_gte_2) = ", dut.clk.value)
    await RisingEdge(dut.clk) 

    print("set_gt_1:")
    print("s1 value = ", dut.s1.value)
    print("s2 value = ", dut.s2.value)
    print("d value = ", dut.d.value)

    # step 2.2 check if d = 0
    result2 = dut.zero.value & 0xFFFFFFFF
    print("is 0 result = ", result2)

    # step 3. OR both results
    dut.s1.value = result1
    dut.s2.value = result2
    dut.funct3.value = Funct3.OR.value # SLT = 6

    # tick the clock 
    print("clock (set_gte_3) = ", dut.clk.value)
    await RisingEdge(dut.clk)

    print("set_gt_2:")
    print("s1 value = ", dut.s1.value)
    print("s2 value = ", dut.s2.value)
    print("d value = ", dut.d.value)

    # result stored in dut.d


### COMPARISONS ###

async def f_set_e(dut):
    """
    In the same format as feq.s rd, rs1, rs2 perform a floating point equal comparison.

    :param dut:
    :return:
    """

    # print values 
    print("f_set_e:")
    print("s1 value = ", dut.s1.value)
    print("s2 value = ", dut.s2.value)
    print("d value = ", dut.d.value)

    # set inputs 
    # r1 = user_input1
    # r2 = user_input2
    dut.funct3.value = Funct3.XOR.value # 0 0 = 0, 1 1 = 0
    dut.funct7.value = 0

    # tick the clock
    print("clock (f_set_e_1) = ", dut.clk.value)
    await RisingEdge(dut.clk)

    print("clock (f_set_e_1) = ", dut.clk.value)
    await RisingEdge(dut.clk)

    # result stored in dut.d
    # get dut.zero value stored in d (using add, wouldn't work otherwise idk why)
    is_equal = dut.zero.value & 0xFFFFFFFF
    dut.s1.value = is_equal
    dut.s2.value = 0x00000000
    dut.funct3.value = Funct3.ADD.value

    print("dut.zero = ", dut.zero.value)

    # tick the clock
    print("clock (f_set_e_1) = ", dut.clk.value)
    await RisingEdge(dut.clk)

    # print values 
    print("f_set_e:")
    print("s1 value = ", dut.s1.value)
    print("s2 value = ", dut.s2.value)
    print("d value = ", dut.d.value)


async def f_set_lt(dut):
    """
    In the same format as flt.s rd, rs1, rs2 perform a floating point less than comparison.

    :param dut:
    :return:
    """

    # set inputs 
    # s1 = user_input1
    # s2 = user_input2

    # print values 
    print("f_set_lt:")
    print("s1 value = ", dut.s1.value)
    print("s2 value = ", dut.s2.value)
    print("d value = ", dut.d.value)

    # COMPARE EXPONENTS (LESS THAN?)
    print("COMPARE EXPONENTS (LESS THAN?)")
    # save value of inputs for later
    s1 = dut.s1.value
    s2 = dut.s2.value

    # extract exponents
    mask = 0x7F800000
    s1_exp = mask & s1
    s2_exp = mask & s2

    # setup inputs to SLT
    dut.s1.value = s1_exp
    dut.s2.value = s2_exp

    # tick the clock
    print("clock (f_set_lt_1) = ", dut.clk.value)
    await RisingEdge(dut.clk) 

    # tick the clock
    print("clock (f_set_lt_1) = ", dut.clk.value)
    await RisingEdge(dut.clk) 

    # print values 
    print("f_set_lt:")
    print("s1 value = ", dut.s1.value)
    print("s2 value = ", dut.s2.value)
    print("d value = ", dut.d.value)

    dut.funct3.value = Funct3.SLT.value # a < b = 1 (a less than b), else 0

    # tick the clock
    print("clock (f_set_lt_1) = ", dut.clk.value)
    await RisingEdge(dut.clk) 

    print("clock (f_set_lt_1) = ", dut.clk.value)
    await RisingEdge(dut.clk) 

    # result saved in dut.d
    result1 = dut.d.value & 0xFFFFFFFF
    print("result1 = ", result1)

    # COMPARE EXPONENTS (EQUAL TO?)
    print("COMPARE EXPONENTS (EQUAL TO?)")
    # step 1. perform subtraction for comparison
    # inputs should be the same
    dut.s1.value = s1_exp
    dut.s2.value = s2_exp
    await perform_sub(dut)

    # tick the clock
    print("clock (f_set_lt_2) = ", dut.clk.value)
    await RisingEdge(dut.clk) 

    print("dut.d = ", dut.d.value)
    # result saved to dut.d

    sub_result = dut.d.value
    dut.s1.value = sub_result
    dut.s2.value = 0x00000000
    dut.funct3.value = Funct3.ADD.value

    # tick the clock
    print("clock (f_set_lt_1) = ", dut.clk.value)
    await RisingEdge(dut.clk) 

    # result saved to dut.d

    result2 = dut.zero.value & 0xFFFFFFFF
    print("result2 = ", result2)

    # tick the clock
    print("clock (f_set_lt_1) = ", dut.clk.value)
    await RisingEdge(dut.clk) 

    # COMPARE MANTISSA (LESS THAN?)
    print("COMPARE MANTISSA (LESS THAN?)")
    # extract mantissas
    mask = 0x007FFFFF
    s1_man = mask & s1
    s2_man = mask & s2

    # compare mantissa SLT
    dut.s1.value = s1_man
    dut.s2.value = s2_man

    # tick the clock
    print("clock (f_set_lt_1) = ", dut.clk.value)
    await RisingEdge(dut.clk) 

    # tick the clock
    print("clock (f_set_lt_1) = ", dut.clk.value)
    await RisingEdge(dut.clk) 

   # print values 
    print("f_set_lt:")
    print("s1 value = ", dut.s1.value)
    print("s2 value = ", dut.s2.value)
    print("d value = ", dut.d.value)

    dut.funct3.value = Funct3.SLT.value # a < b = 1 (a less than b), else 0

    # tick the clock
    print("clock (f_set_lt_1) = ", dut.clk.value)
    await RisingEdge(dut.clk) 

    # tick the clock
    print("clock (f_set_lt_1) = ", dut.clk.value)
    await RisingEdge(dut.clk) 

    # result stored in dut.d
    result3 = dut.d.value & 0xFFFFFFFF

    # tick the clock
    print("clock (f_set_lt_1) = ", dut.clk.value)
    await RisingEdge(dut.clk) 

    # tick the clock
    print("clock (f_set_lt_1) = ", dut.clk.value)
    await RisingEdge(dut.clk) 

    print("f_set_lt:")
    print("s1 value = ", dut.s1.value)
    print("s2 value = ", dut.s2.value)
    print("d value = ", dut.d.value)

    # print results of all comparisons
    print("result1 = ", result1)
    print("result2 = ", result2)
    print("result3 = ", result3)

    # ALL TESTS COMPLETED 
    # result 2 AND result 3
    dut.s1.value = result2
    dut.s2.value = result3
    dut.funct3.value = Funct3.AND.value

    # tick the clock
    print("clock (f_set_lt_1) = ", dut.clk.value)
    await RisingEdge(dut.clk) 

    result_and = dut.d.value

    # tick the clock
    print("clock (f_set_lt_1) = ", dut.clk.value)
    await RisingEdge(dut.clk) 

    print("result_and", result_and)

    # result 1 OR (result 2 AND result 3)
    dut.s1.value = result1
    dut.s2.value = result_and
    dut.funct3.value = Funct3.OR.value

    # tick the clock
    print("clock (f_set_lt_1) = ", dut.clk.value)
    await RisingEdge(dut.clk) 

    final_result = dut.d.value

    # tick the clock
    print("clock (f_set_lt_1) = ", dut.clk.value)
    await RisingEdge(dut.clk) 

    print("final result = ", final_result)
    

async def f_set_lte(dut):
    """
    In the same format as fle.s rd, rs1, rs2 perform a floating point less than or equal comparison.

    :param dut:
    :return:
    """

    # check if s1 is less than s2
    # set inputs 
    s1 = dut.s1.value
    s2 = dut.s2.value
    await f_set_lt(dut) # less than

    # tick the clock
    print("clock (f_set_lte_1) = ", dut.clk.value)
    await RisingEdge(dut.clk)

    # result stored in dut.d
    result_lt = dut.d.value
    print("result_lt = ", result_lt)

    # tick the clock
    print("clock (f_set_lte_1) = ", dut.clk.value)
    await RisingEdge(dut.clk)

    # check if s1 is equal to s2 
    dut.s1.value = s1
    dut.s2.value = s2
    await f_set_e(dut)  # equal to

    # tick the clock
    print("clock (f_set_lte_1) = ", dut.clk.value)
    await RisingEdge(dut.clk)

    # result stored in dut.d
    result_eq = dut.d.value
    print("result_eq = ", result_eq)

    # tick the clock
    print("clock (f_set_lte_1) = ", dut.clk.value)
    await RisingEdge(dut.clk)

    # AND both results
    dut.s1.value = result_lt
    dut.s2.value = result_eq
    dut.funct3.value = Funct3.ADD.value

    # tick the clock
    print("clock (f_set_lte_1) = ", dut.clk.value)
    await RisingEdge(dut.clk)

    # result stored in dut.d
    print("final_result = ", dut.d.value)

    print("f_set_lte:")
    print("s1 value = ", dut.s1.value)
    print("s2 value = ", dut.s2.value)
    print("d value = ", dut.d.value)

   # tick the clock
    print("clock (f_set_lte_1) = ", dut.clk.value)
    await RisingEdge(dut.clk)


### MULTIPLICATION ###

async def perform_multiplication(dut):
    """
    In the same format as mul rd, rs1, rs2 perform multiplication.

    :param dut:
    :return:
    """
    # setup inputs 
    # dut.s1.value = user_input1
    # dut.s2.value = user_input2
    multiplicand = dut.s1.value
    multiplier = dut.s2.value
    product = 0x00000000    # register to hold product

    # tick the clock 
    print("clock (perform_multiplication) = ", dut.clk.value)
    await RisingEdge(dut.clk)

    print("perform_multiplication:")
    print("s1 value = ", dut.s1.value)
    print("s2 value = ", dut.s2.value)
    print("d value = ", dut.d.value)

    # tick the clock 
    print("clock (perform_multiplication) = ", dut.clk.value)
    await RisingEdge(dut.clk)

    # LOOP START for i in range(32)
    for i in range(32):
        # obtain lsb of multiplier
        dut.s1.value = multiplier
        dut.s2.value = 0x00000001
        dut.funct3.value = Funct3.AND.value

        # tick the clock 
        print("clock (perform_multiplication) = ", dut.clk.value)
        await RisingEdge(dut.clk)

        # tick the clock 
        print("clock (perform_multiplication) = ", dut.clk.value)
        await RisingEdge(dut.clk)

        print("perform_multiplication:")
        print("s1 value = ", dut.s1.value)
        print("s2 value = ", dut.s2.value)
        print("d value = ", dut.d.value)

        # result stored in dut.d
        lsb = dut.d.value

        # tick the clock 
        print("clock (perform_multiplication) = ", dut.clk.value)
        await RisingEdge(dut.clk)

        print("multiplier lsb =", lsb)

        # create mask 
        dut.s1.value = 0x00000000
        dut.s2.value = lsb

        # tick the clock 
        print("clock (perform_multiplication) = ", dut.clk.value)
        await RisingEdge(dut.clk)

    # tick the clock 
        print("clock (perform_multiplication) = ", dut.clk.value)
        await RisingEdge(dut.clk)

        # subtract values (if lsb = 0, 0 - lsb = 0x00000000. if lsb = 1, 0 - lsb = 0xFFFFFFFF)
        await perform_sub(dut)

        # tick the clock 
        print("clock (perform_multiplication) = ", dut.clk.value)
        await RisingEdge(dut.clk)

        print("perform_multiplication:")
        print("s1 value = ", dut.s1.value)
        print("s2 value = ", dut.s2.value)
        print("d value = ", dut.d.value)

        # result will be in dut.d 
        mask = dut.d.value
        print("mask = ", mask)

        # tick the clock 
        print("clock (perform_multiplication) = ", dut.clk.value)
        await RisingEdge(dut.clk)

    # tick the clock 
        print("clock (perform_multiplication) = ", dut.clk.value)
        await RisingEdge(dut.clk)

        # determine value to be added (if lsb = 0, add_value = 0. if lsb = 1, add_value = multiplicand)
        dut.s1.value = multiplicand 
        dut.s2.value = mask
        dut.funct3.value = Funct3.AND.value

        # tick the clock 
        print("clock (perform_multiplication) = ", dut.clk.value)
        await RisingEdge(dut.clk)

    # tick the clock 
        print("clock (perform_multiplication) = ", dut.clk.value)
        await RisingEdge(dut.clk)

        # result stored in dut.d
        add_value = dut.d.value
        print("value added to product = ", add_value)

    # tick the clock 
        print("clock (perform_multiplication) = ", dut.clk.value)
        await RisingEdge(dut.clk)

        # tick the clock 
        print("clock (perform_multiplication) = ", dut.clk.value)
        await RisingEdge(dut.clk)

        # sum product and add_value (only adds multiplicand to product if lsb of multiplier = 1)
        dut.s1.value = add_value
        dut.s2.value = product 
        dut.funct3.value = Funct3.ADD.value

    # tick the clock 
        print("clock (perform_multiplication) = ", dut.clk.value)
        await RisingEdge(dut.clk)

        # tick the lock 
        print("clock (perform_multiplication) = ", dut.clk.value)
        await RisingEdge(dut.clk)

        # result stored in dut.d
        product = dut.d.value
        print("product = ", product)

        # tick the clock 
        print("clock (perform_multiplication) = ", dut.clk.value)
        await RisingEdge(dut.clk)

        # shift the multiplicand register left 1 bit 
        print("multiplicand before left shift = ", multiplicand)
        dut.s1.value = multiplicand
        dut.s2.value = 0x00000001

        # tick the clock 
        print("clock (perform_multiplication) = ", dut.clk.value)
        await RisingEdge(dut.clk)

        print("perform_multiplication (BEFORE LEFT SHIFT):")
        print("s1 value = ", dut.s1.value)
        print("s2 value = ", dut.s2.value)
        dut.funct3.value = Funct3.SLL.value

    # tick the clock 
        print("clock (perform_multiplication) = ", dut.clk.value)
        await RisingEdge(dut.clk)

    # tick the clock 
        print("clock (perform_multiplication) = ", dut.clk.value)
        await RisingEdge(dut.clk)

        # result stored in dut.d
        multiplicand = dut.d.value
        print("multiplicand after left shift = ", multiplicand)

        # tick the clock 
        print("clock (perform_multiplication) = ", dut.clk.value)
        await RisingEdge(dut.clk)

        # shift the multiplier register right 1 bit 
        print("multiplier before right shift = ", multiplier)
        dut.s1.value = multiplier 
        dut.s2.value = 0x00000001

        # tick the clock 
        print("clock (perform_multiplication) = ", dut.clk.value)
        await RisingEdge(dut.clk)

        print("perform_multiplication - BEFORE RIGHT SHIFT:")
        print("s1 value = ", dut.s1.value)
        print("s2 value = ", dut.s2.value)
        dut.funct3.value = Funct3.SRL.value

    # tick the clock 
        print("clock (perform_multiplication) = ", dut.clk.value)
        await RisingEdge(dut.clk)

        # tick the clock 
        print("clock (perform_multiplication) = ", dut.clk.value)
        await RisingEdge(dut.clk)

        # result stored in dut.d
        multiplier = dut.d.value
        print("multiplier after right shift = ", multiplier)

    # tick the clock 
        print("clock (perform_multiplication) = ", dut.clk.value)
        await RisingEdge(dut.clk)

        # END OF LOOP
        # store result in rd
        dut.s1.value = product 
        dut.s2.value = 0x00000000
        dut.funct3.value = Funct3.ADD.value

        # tick the clock 
        print("clock (perform_multiplication) = ", dut.clk.value)
        await RisingEdge(dut.clk)

        # result stored in rd

        print("perform_multiplication:")
        print("s1 value = ", dut.s1.value)
        print("s2 value = ", dut.s2.value)
        print("d value = ", dut.d.value)
        print("multiplicand = ", multiplicand)
        print("multiplier = ", multiplier )


### DIVISION ###

async def perform_division(dut):
    """
    In the same format as mul rd, rs1, rs2 perform multiplication.

    :param dut:
    :return:
    """
    # setup inputs 
    # dut.s1.value = user_input1
    # dut.s2.value = user_input2
    quotient = 0x0000   # 16-bit 
    divisor = dut.s2.value  # 32-bit
    remainder = dut.s1.value    # 32-bit

    print("perform_division INITIAL:")
    print("quotient = ", quotient)
    print("remainder = ", remainder)
    print("divisor = ", divisor)
    print("fct3 = ", dut.funct3.value)

    # shift divisor left 16 bits so it fills left half of divisor register 
    dut.s1.value = divisor
    dut.s2.value = 16
    dut.funct3.value = Funct3.SLL.value

    # tick the clock 
    print("clock (perform_division) = ", dut.clk.value)
    await RisingEdge(dut.clk)

    # tick the clock 
    print("clock (perform_division) = ", dut.clk.value)
    await RisingEdge(dut.clk)

   # result stored in dut.d
    divisor = dut.d.value
    
    print("perform_division:")
    print("s1 = ", dut.s1.value)
    print("s2 = ", dut.s2.value)

    # tick the clock 
    print("clock (perform_division) = ", dut.clk.value)
    await RisingEdge(dut.clk)

    print("perform_division:")
    print("quotient = ", quotient)
    print("remainder = ", remainder)
    print("divisor = ", divisor)

    # tick the clock 
    print("clock (perform_division) = ", dut.clk.value)
    await RisingEdge(dut.clk)

    # LOOP START for i in range(65)
    for i in range(17):
        # subtract divisor from remainder and place result in remainder
        dut.s1.value = remainder
        dut.s2.value = divisor

        # tick the clock 
        print("clock (perform_division) = ", dut.clk.value)
        await RisingEdge(dut.clk)

        await perform_sub(dut)

        # tick the clock 
        print("clock (perform_division) = ", dut.clk.value)
        await RisingEdge(dut.clk)

        print("perform_division:")
        print("quotient = ", quotient)
        print("remainder = ", remainder)
        print("divisor = ", divisor)

        # result stored in dut.d
        remainder = dut.d.value

        # tick the clock 
        print("clock (perform_division) = ", dut.clk.value)
        await RisingEdge(dut.clk)

        print("**************************")
        print("remainder = ", remainder)

        # ^ ABOVE THIS IS GOOD ^

        # tick the clock 
        print("clock (perform_division) = ", dut.clk.value)
        await RisingEdge(dut.clk)

        print("perform_division:")
        print("quotient = ", quotient)
        print("remainder = ", remainder)
        print("divisor = ", divisor)

        # test the remainder (remainder < 0, 1 if yes, 0 if no)
        dut.s1.value = remainder 
        dut.s2.value = 0x00000000

        # tick the clock 
        print("clock (perform_division) = ", dut.clk.value)
        await RisingEdge(dut.clk)

        dut.funct3.value = Funct3.SLT.value

        # tick the clock 
        print("clock (perform_division) = ", dut.clk.value)
        await RisingEdge(dut.clk)

        # tick the clock 
        print("clock (perform_division) = ", dut.clk.value)
        await RisingEdge(dut.clk)

        # result stored in dut.d
        remainder_test = dut.d.value & 0xFFFFFFFF
        print("remainder_test = ", remainder_test)

        # tick the clock 
        print("clock (perform_division) = ", dut.clk.value)
        await RisingEdge(dut.clk)

        # create a mask 
        dut.s1.value = 0x00000000
        dut.s2.value = remainder_test

        # tick the clock 
        print("clock (perform_division) = ", dut.clk.value)
        await RisingEdge(dut.clk)

        await perform_sub(dut)

        # tick the clock 
        print("clock (perform_division) = ", dut.clk.value)
        await RisingEdge(dut.clk)

        print("**************************")
        # ^ ABOVE THIS IS GOOD ^
        # result stored in dut.d
        mask = dut.d.value
        print("mask = ", mask)

        # tick the clock 
        print("clock (perform_division) = ", dut.clk.value)
        await RisingEdge(dut.clk)
        
        # determine value to be added 
        dut.s1.value = divisor
        dut.s2.value = mask

        # tick the clock 
        print("clock (perform_division) = ", dut.clk.value)
        await RisingEdge(dut.clk)

        print("perform_division:")
        print("s1 = ", dut.s1.value)
        print("s2 = ", dut.s2.value)

        dut.funct3.value = Funct3.AND.value

        # tick the clock 
        print("clock (perform_division) = ", dut.clk.value)
        await RisingEdge(dut.clk)

        # tick the clock 
        print("clock (perform_division) = ", dut.clk.value)
        await RisingEdge(dut.clk)

        # result stored in dut.d
        add_value = dut.d.value

        # tick the clock 
        print("clock (perform_division) = ", dut.clk.value)
        await RisingEdge(dut.clk)

        print("add_value = ", add_value)

        print("perform_division:")
        print("quotient = ", quotient)
        print("remainder = ", remainder)
        print("divisor = ", divisor)

        # add the value 
        dut.s1.value = add_value
        dut.s2.value = remainder

        # tick the clock 
        print("clock (perform_division) = ", dut.clk.value)
        await RisingEdge(dut.clk)

        print("perform_division:")
        print("s1 = ", dut.s1.value)
        print("s2 = ", dut.s2.value)
        
        dut.funct3.value = Funct3.ADD.value

        # tick the clock 
        print("clock (perform_division) = ", dut.clk.value)
        await RisingEdge(dut.clk)

        # tick the clock 
        print("clock (perform_division) = ", dut.clk.value)
        await RisingEdge(dut.clk)

        # result stored in dut.d
        remainder = dut.d.value

        # tick the clock 
        print("clock (perform_division) = ", dut.clk.value)
        await RisingEdge(dut.clk)

        print("perform_division:")
        print("quotient = ", quotient)
        print("remainder = ", remainder)
        print("divisor = ", divisor)

        print("**************************")
        # ^ ABOVE THIS IS GOOD ^

        # shift quotient register to the left 
        dut.s1.value = quotient
        dut.s2.value = 0x00000001

        # tick the clock 
        print("clock (perform_division) = ", dut.clk.value)
        await RisingEdge(dut.clk)

        dut.funct3.value = Funct3.SLL.value

        # tick the clock 
        print("clock (perform_division) = ", dut.clk.value)
        await RisingEdge(dut.clk)

        # tick the clock 
        print("clock (perform_division) = ", dut.clk.value)
        await RisingEdge(dut.clk)

        # result stored in dut.d
        quotient = dut.d.value

        # tick the clock 
        print("clock (perform_division) = ", dut.clk.value)
        await RisingEdge(dut.clk)

        print("perform_division:")
        print("quotient = ", quotient)
        print("remainder = ", remainder)
        print("divisor = ", divisor)

        # set LSB accordingly (LSB = 1 if remainder >= 0, and LSB = 0 if remainder < 0)
        # get opposite of remainder_test 
        dut.s1.value = remainder_test
        dut.s2.value = 0x00000001

        # tick the clock 
        print("clock (perform_division) = ", dut.clk.value)
        await RisingEdge(dut.clk)

        dut.funct3.value = Funct3.XOR.value

        # tick the clock 
        print("clock (perform_division) = ", dut.clk.value)
        await RisingEdge(dut.clk)

        # tick the clock
        print("clock (perform_division) = ", dut.clk.value)
        await RisingEdge(dut.clk)

        # result stored in dut.d
        lsb = dut.d.value & 0xFFFFFFFF

        # tick the clock
        print("clock (perform_division) = ", dut.clk.value)
        await RisingEdge(dut.clk)

        print("lsb = ", lsb)

        # add lsb to quotient 
        dut.s1.value = quotient 
        dut.s2.value = lsb

        # tick the clock 
        print("clock (perform_division) = ", dut.clk.value)
        await RisingEdge(dut.clk)

        dut.funct3.value = Funct3.OR.value

        # tick the clock 
        print("clock (perform_division) = ", dut.clk.value)
        await RisingEdge(dut.clk)

        # tick the clock
        print("clock (perform_division) = ", dut.clk.value)
        await RisingEdge(dut.clk)

        # result stored in dut.d
        quotient = dut.d.value

        # tick the clock
        print("clock (perform_division) = ", dut.clk.value)
        await RisingEdge(dut.clk)

        print("perform_division:")
        print("quotient = ", quotient)
        print("remainder = ", remainder)
        print("divisor = ", divisor)

        # shift divisor register right 1 bit 
        dut.s1.value = divisor 
        dut.s2.value = 0x00000001

        # tick the clock 
        print("clock (perform_division) = ", dut.clk.value)
        await RisingEdge(dut.clk)

        dut.funct3.value = Funct3.SRL.value

        # tick the clock
        print("clock (perform_division) = ", dut.clk.value)
        await RisingEdge(dut.clk)

        # tick the clock 
        print("clock (perform_division) = ", dut.clk.value)
        await RisingEdge(dut.clk)

        # result stored in dut.d
        divisor = dut.d.value

        # tick the clock
        print("clock (perform_division) = ", dut.clk.value)
        await RisingEdge(dut.clk)

        print("perform_division:")
        print("quotient = ", quotient)
        print("remainder = ", remainder)
        print("divisor = ", divisor)

    # END OF LOOP
    
    # return quotient 
    dut.s1.value = quotient
    dut.s2.value = 0x00000000

    # tick the clock 
    print("clock (perform_division) = ", dut.clk.value)
    await RisingEdge(dut.clk)

    dut.funct3.value = Funct3.ADD.value

    # tick the clock 
    print("clock (perform_division) = ", dut.clk.value)
    await RisingEdge(dut.clk)

    # tick the clock 
    print("clock (perform_division) = ", dut.clk.value)
    await RisingEdge(dut.clk)

    # result stored in dut.d
    


    
@cocotb.test()
async def run_alu_sim(dut):
    clock = Clock(dut.clk, period=10, units='ns') # This assigns the clock into the ALU
    cocotb.start_soon(clock.start(start_high=False))


@cocotb.test()
async def test_perform_not(dut):
    '''
    tests the perform_not wrapper 
    '''
    print("TESTING: perform_not(dut)")
    clock = Clock(dut.clk, period=10, units='ns')
    cocotb.start_soon(clock.start(start_high=False))

    dut.s1.value = 0x12340000   # setup input
    await perform_not(dut)      # setup operation

    print("clock (test_perform_not1) = ", dut.clk.value)
    await RisingEdge(dut.clk)

    # print values 
    print("test_perform_not:")
    print("s1 value = ", dut.s1.value)
    print("s2 value = ", dut.s2.value)
    print("d value = ", dut.d.value)

    result = dut.d.value & 0xFFFFFFFF
    expected = (~0x12340000) & 0xFFFFFFFF

    print("clock (test_perform_not_2) = ", dut.clk.value)
    await RisingEdge(dut.clk)

    assert result == expected, f"NOT failed: got 0x{result:08X}, expected 0x{expected:08X}"
    print(f"NOT(0x12340000) = 0x{result:08X}")

    print("clock (test_perform_not_3) = ", dut.clk.value)
    await RisingEdge(dut.clk)

@cocotb.test()
async def test_perform_negate(dut):
    '''
    tests the perform_negate wrapper 
    '''
    print("TESTING: perform_negate(dut)")
    clock = Clock(dut.clk, period=10, units='ns')
    cocotb.start_soon(clock.start(start_high=False))

    dut.s1.value = 0xFFFF0000   # setup input
    await perform_negate(dut)      # setup operation

    print("clock (test_perform_negate_1) = ", dut.clk.value)
    await RisingEdge(dut.clk)

    # print values 
    print("test_perform_negate:")
    print("s1 value = ", dut.s1.value)
    print("s2 value = ", dut.s2.value)
    print("d value = ", dut.d.value)

    result = dut.d.value & 0xFFFFFFFF
    expected = (~0xFFFF0000 + 1) & 0xFFFFFFFF

    print("clock (test_perform_negate_2) = ", dut.clk.value)
    await RisingEdge(dut.clk)

    assert result == expected, f"NEGATE failed: got 0x{result:08X}, expected 0x{expected:08X}"
    print(f"NEGATE(0xFFFF000) = 0x{result:08X}")

    print("clock (test_perform_negate_3) = ", dut.clk.value)
    await RisingEdge(dut.clk)

@cocotb.test()
async def test1_perform_sub(dut):
    '''
    Docstring for test_perform_sub
    
    :param dut: Description
    '''
    print("TESTING: perform_sub(dut)")
    clock = Clock(dut.clk, period=10, units='ns')
    cocotb.start_soon(clock.start(start_high=False))

    # setup inputs
    dut.s1.value = 0x0000FFFF
    dut.s2.value = 0x00005555

    await RisingEdge(dut.clk)
    print("rs2 check = ", dut.s2.value)

    await RisingEdge(dut.clk)
    await perform_sub(dut)      # setup operation

    print("clock (test_perform_sub_1) = ", dut.clk.value)
    await RisingEdge(dut.clk)

    # print values 
    print("test_perform_sub:")
    print("s1 value = ", dut.s1.value)
    print("s2 value = ", dut.s2.value)
    print("d value = ", dut.d.value)

    result = dut.d.value & 0xFFFFFFFF
    expected = (0x0000FFFF - 0x00005555) & 0xFFFFFFFF

    print("clock (test_perform_sub_2) = ", dut.clk.value)
    await RisingEdge(dut.clk)

    assert result == expected, f"SUB failed: got 0x{result:08X}, expected 0x{expected:08X}"
    print(f"SUB(0x007FAA78) = 0x{result:08X}")

    print("clock (test_perform_negate_3) = ", dut.clk.value)
    await RisingEdge(dut.clk)

@cocotb.test()
async def test2_perform_sub(dut):
    '''
    Docstring for test_perform_sub
    
    :param dut: Description
    '''
    print("TESTING: perform_sub(dut)")
    clock = Clock(dut.clk, period=10, units='ns')
    cocotb.start_soon(clock.start(start_high=False))

    # setup inputs
    dut.s1.value = 0x0000F000
    dut.s2.value = 0x00000001

    print("clock (test2_perform_sub_1) = ", dut.clk.value)
    await RisingEdge(dut.clk)

    print("clock (test2_perform_sub_2) = ", dut.clk.value)
    await RisingEdge(dut.clk)
    await perform_sub(dut)      # setup operation

    print("clock (test2_perform_sub_3) = ", dut.clk.value)
    await RisingEdge(dut.clk)

    # print values 
    print("test2_perform_sub:")
    print("s1 value = ", dut.s1.value)
    print("s2 value = ", dut.s2.value)
    print("d value = ", dut.d.value)

    result = dut.d.value & 0xFFFFFFFF
    expected = (0x0000F000 - 0x00000001) & 0xFFFFFFFF

    print("clock (test2_perform_sub_4) = ", dut.clk.value)
    await RisingEdge(dut.clk)

    assert result == expected, f"SUB failed: got 0x{result:08X}, expected 0x{expected:08X}"
    print(f"SUB(0x007FAA78) = 0x{result:08X}")

    print("clock (test2_perform_sub_5) = ", dut.clk.value)
    await RisingEdge(dut.clk)

@cocotb.test()
async def test_set_gt(dut):
    '''
    Docstring for test_set_gt **SIGNED
    
    :param dut: Description
    '''
    print("TESTING: set_gt(dut)")
    clock = Clock(dut.clk, period=10, units='ns')
    cocotb.start_soon(clock.start(start_high=False))

    # setup inputs
    dut.s1.value = 0x1234AAAA
    dut.s2.value = 0x12340000

    print("clock (test_set_gt_1) = ", dut.clk.value)
    await RisingEdge(dut.clk)

    print("clock (test_set_gt_2) = ", dut.clk.value)
    await RisingEdge(dut.clk)

    await set_gt(dut)      # setup operation

    print("clock (test_set_gt_3) = ", dut.clk.value)
    await RisingEdge(dut.clk)

    # print values 
    print("test_set_gt:")
    print("s1 value = ", dut.s1.value)
    print("s2 value = ", dut.s2.value)
    print("d value = ", dut.d.value)

    result = dut.d.value & 0xFFFFFFFF
    expected = (0x1234AAAA > 0x12340000) & 0xFFFFFFFF

    print("clock (test_set_gt_4) = ", dut.clk.value)
    await RisingEdge(dut.clk)

    assert result == expected, f"GT failed: got 0x{result:08X}, expected 0x{expected:08X}"
    print(f"GT({expected}) = {result:08X}")

    print("clock (test_set_gt_5) = ", dut.clk.value)
    await RisingEdge(dut.clk)

@cocotb.test()
async def test_set_gte(dut):
    '''
    Docstring for test_set_gte **SIGNED
    
    :param dut: Description
    '''
    print("TESTING: set_gte(dut)")
    clock = Clock(dut.clk, period=10, units='ns')
    cocotb.start_soon(clock.start(start_high=False))

    # setup inputs
    dut.s1.value = 0x12340000
    dut.s2.value = 0x1234AAAA

    print("clock (test_set_gte_1) = ", dut.clk.value)
    await RisingEdge(dut.clk)

    print("clock (test_set_gte_2) = ", dut.clk.value)
    await RisingEdge(dut.clk)

    await set_gte(dut)      # setup operation

    print("clock (test_set_gte_3) = ", dut.clk.value)
    await RisingEdge(dut.clk)

    # print values 
    print("test_set_gte:")
    print("s1 value = ", dut.s1.value)
    print("s2 value = ", dut.s2.value)
    print("d value = ", dut.d.value)

    result = dut.d.value & 0xFFFFFFFF
    expected = (0x12340000 >= 0x1234AAAA) & 0xFFFFFFFF

    print("clock (test_set_gte_4) = ", dut.clk.value)
    await RisingEdge(dut.clk)

    assert result == expected, f"GTE failed: got 0x{result:08X}, expected 0x{expected:08X}"
    print(f"GTE({expected}) = {result:08X}")

    print("clock (test_set_gte_5) = ", dut.clk.value)
    await RisingEdge(dut.clk)

@cocotb.test()
async def test_f_set_e(dut):
    '''
    Docstring for test_f_set_e
    
    :param dut: Description
    '''
    print("TESTING: f_set_e(dut)")
    clock = Clock(dut.clk, period=10, units='ns')
    cocotb.start_soon(clock.start(start_high=False))

    # setup inputs
    dut.s1.value = 0x4048F5C3   # = 3.14
    dut.s2.value = 0x4048F5C3   # = 3.14

    print("clock (test_f_set_e1) = ", dut.clk.value)
    await RisingEdge(dut.clk)

    print("clock (test_f_set_e2) = ", dut.clk.value)
    await RisingEdge(dut.clk)

    await f_set_e(dut)      # setup operation

    print("clock (test_f_set_e3) = ", dut.clk.value)
    await RisingEdge(dut.clk)

    # print values 
    print("test_f_set_e:")
    print("s1 value = ", dut.s1.value)
    print("s2 value = ", dut.s2.value)
    print("d value = ", dut.d.value)

    result = dut.d.value & 0xFFFFFFFF
    expected = (0x4048F5C3 == 0x4048F5C3) & 0xFFFFFFFF

    print("clock (test_f_set_e4) = ", dut.clk.value)
    await RisingEdge(dut.clk)

    assert result == expected, f"EQUAL failed: got 0x{result:08X}, expected 0x{expected:08X}"
    print(f"EQUAL({expected}) = {result:08X}")

    print("clock (test_f_set_e5) = ", dut.clk.value)
    await RisingEdge(dut.clk)

@cocotb.test()
async def test_f_set_lt(dut):
    '''
    Docstring for test_f_set_lt
    
    :param dut: Description
    '''
    print("TESTING: f_set_lt(dut)")
    clock = Clock(dut.clk, period=10, units='ns')
    cocotb.start_soon(clock.start(start_high=False))

    # setup inputs
    dut.s1.value = 0x3fa66666   # = 1.3
    # dut.s2.value = 0x3f933333   # = 1.15
    # dut.s2.value = 0x40133333   # = 2.3
    dut.s2.value = 0x40200000   # = 2.5

    print("clock (test_f_set_lt_1) = ", dut.clk.value)
    await RisingEdge(dut.clk)

    print("clock (test_f_set_lt_2) = ", dut.clk.value)
    await RisingEdge(dut.clk)

    await f_set_lt(dut)      # setup operation

    print("clock (test_f_set_lt_3) = ", dut.clk.value)
    await RisingEdge(dut.clk)

    result = dut.d.value & 0xFFFFFFFF
    expected = (0x3fa66666 < 0x40200000) & 0xFFFFFFFF

    print("clock (test_f_set_lt_4) = ", dut.clk.value)
    await RisingEdge(dut.clk)

    assert result == expected, f"LESS THAN failed: got 0x{result:08X}, expected 0x{expected:08X}"
    print(f"LESS THAN({expected}) = {result:08X}")

    print("clock (test_f_set_lt_5) = ", dut.clk.value)
    await RisingEdge(dut.clk)

@cocotb.test()
async def test_f_set_lte(dut):
    '''
    Docstring for test_f_set_lte
    
    :param dut: Description
    '''
    print("TESTING: f_set_lte(dut)")
    clock = Clock(dut.clk, period=10, units='ns')
    cocotb.start_soon(clock.start(start_high=False))

    # setup inputs
    # dut.s1.value = 0x3fa66666   # = 1.3
    # dut.s1.value = 0x40200000   # = 2.5
    dut.s1.value = 0x40133333   # = 2.3
    # dut.s1.value = 0x3f933333   # = 1.15
    # dut.s2.value = 0x3fa66666   # = 1.3
    # dut.s2.value = 0x3f933333   # = 1.15
    # dut.s2.value = 0x40133333   # = 2.3
    dut.s2.value = 0x40200000   # = 2.5

    print("clock (test_f_set_lte_1) = ", dut.clk.value)
    await RisingEdge(dut.clk)

    print("clock (test_f_set_lte_2) = ", dut.clk.value)
    await RisingEdge(dut.clk)

    await f_set_lte(dut)      # setup operation

    print("clock (test_f_set_lte_3) = ", dut.clk.value)
    await RisingEdge(dut.clk)

    result = dut.d.value & 0xFFFFFFFF
    expected = (0x40133333 <= 0x40200000) & 0xFFFFFFFF

    print("clock (test_f_set_lte_4) = ", dut.clk.value)
    await RisingEdge(dut.clk)

    assert result == expected, f"LTE failed: got 0x{result:08X}, expected 0x{expected:08X}"
    print(f"LTE ({expected}) = {result:08X}")

    print("clock (test_f_set_lte_5) = ", dut.clk.value)
    await RisingEdge(dut.clk)

@cocotb.test()
async def test_perform_multiplication(dut):
    '''
    Docstring for test_perform_multiplication
    
    :param dut: Description
    '''
    print("TESTING: perform_multiplication(dut)")
    clock = Clock(dut.clk, period=10, units='ns')
    cocotb.start_soon(clock.start(start_high=False))

    # setup inputs
    # dut.s1.value = 0x0000000A # = 10
    # dut.s2.value = 0x00000005 # = 5
    dut.s1.value = 0x00000019 # = 25 = 00000000000000000000000000011001
    dut.s2.value = 0x00000002 # = 2 = 00000000000000000000000000000010

    print("clock (test_perform_multiplication_1) = ", dut.clk.value)
    await RisingEdge(dut.clk)

    print("clock (test_perform_multiplication_2) = ", dut.clk.value)
    await RisingEdge(dut.clk)

    await perform_multiplication(dut)      # setup operation

    print("clock (test_perform_multiplication_3) = ", dut.clk.value)
    await RisingEdge(dut.clk)

    result = dut.d.value & 0xFFFFFFFF
    expected = (0x00000019 * 0x00000002) & 0xFFFFFFFF

    print("clock (test_perform_multiplication_4) = ", dut.clk.value)
    await RisingEdge(dut.clk)

    assert result == expected, f"MULT failed: got 0x{result:08X}, expected 0x{expected:08X}"
    print(f"MULT ({expected}) = {result:08X}")

    print("clock (test_perform_multiplication_5) = ", dut.clk.value)
    await RisingEdge(dut.clk)

@cocotb.test()
async def test_perform_division(dut):
    '''
    Docstring for test_perform_division
    
    :param dut: Description
    '''
    print("TESTING: perform_division(dut)")
    clock = Clock(dut.clk, period=10, units='ns')
    cocotb.start_soon(clock.start(start_high=False))

    # setup inputs
    # dut.s1.value = 0x0000000A # = 10
    #dut.s2.value = 0x00000002 # = 2 = 00000000000000000000000000000010
    # dut.s1.value = 0x00000019 # = 25 = 00000000000000000000000000011001
    # dut.s2.value = 0x00000005 # = 5 = 00000000000000000000000000000101
    dut.s1.value = 0x00000007 # = 7
    dut.s2.value = 0x00000002 # = 2

    print("clock (test_perform_division_1) = ", dut.clk.value)
    await RisingEdge(dut.clk)

    print("clock (test_perform_division_2) = ", dut.clk.value)
    await RisingEdge(dut.clk)

    await perform_division(dut)      # setup operation

    print("clock (test_perform_division_3) = ", dut.clk.value)
    await RisingEdge(dut.clk)

    result = dut.d.value & 0xFFFFFFFF
    expected = (0x00000007 // 0x00000002) & 0xFFFFFFFF

    print("clock (test_perform_division_4) = ", dut.clk.value)
    await RisingEdge(dut.clk)

    assert result == expected, f"DIV failed: got 0x{result:08X}, expected 0x{expected:08X}"
    print(f"DIV ({expected}) = {result:08X}")

    print("clock (test_perform_division_5) = ", dut.clk.value)
    await RisingEdge(dut.clk)

def test_via_cocotb():
    """
    Main entry point for cocotb
    """
    verilog_sources = [os.path.abspath(os.path.join('.', 'alu.v'))]
    runner = get_runner("verilator")
    runner.build(
        verilog_sources=verilog_sources,
        vhdl_sources=[],
        hdl_toplevel="RISCALU",
        build_args=["--threads", "2"],
        build_dir=alu_sim_dir,
    )
    runner.test(hdl_toplevel="RISCALU", test_module="alu_sim")

if __name__ == '__main__':
    test_via_cocotb()
