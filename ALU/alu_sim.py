from enum import Enum
import os

import cocotb

from cocotb.clock import Clock
from cocotb.runner import get_runner
#from cocotb.triggers import RisingEdge
from cocotb.triggers import *

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
    await FallingEdge(dut.clk) 

    # step 2. add 1 to the result

    dut.s1.value = dut.d.value
    dut.s2.value = 0x1  # 0x00000001
    dut.funct3.value = Funct3.ADD.value # use add to add 1 

    # tick the clock
    print("clock (perform_negate_2) = ", dut.clk.value)
    await RisingEdge(dut.clk)
    
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
    # step 1. negate r1

    temporary = dut.s2.value

    await perform_negate(dut)

    # tick the clock 
    print("clock (perform_sub_1) = ", dut.clk.value)
    await FallingEdge(dut.clk) 

    print("perform_sub:")
    print("s1 value = ", dut.s1.value)
    print("s2 value = ", dut.s2.value)
    print("d value = ", dut.d.value)
    
    # step 2. add r1 to r2
    dut.s1.value = dut.d.value
    dut.s2.value = temporary
    # dut.s2.value = user_input
    dut.funct3.value = Funct3.ADD.value # use add to add 1 

    # tick the clock
    print("clock (perform_sub_2) = ", dut.clk.value)
    await RisingEdge(dut.clk)

    # result stored in dut.d


async def set_gt(dut):
    """
    In the same format as slt, rd, rsq, rs2 perform the operation to set the output LSB bit to rs1 > rs2.

    :param dut:
    :return:
    """

    # setup inputs 

    # tick the clock 

    # result stored in dut.d


async def set_gte(dut):
    """
    In the same format as slt rd, rs1, rs2 perform the operation to set the output LSB bit to rs1 >= rs2.

    :param dut: DUT object from cocotb
    :return:
    """

    # setup inputs 

    # tick the clock 

    # result stored in dut.d

### COMPARISONS ###

async def f_set_e(dut):
    """
    In the same format as feq.s rd, rs1, rs2 perform a floating point equal comparison.

    :param dut:
    :return:
    """


async def f_set_lt(dut):
    """
    In the same format as flt.s rd, rs1, rs2 perform a floating point less than comparison.

    :param dut:
    :return:
    """


async def f_set_lte(dut):
    """
    In the same format as fle.s rd, rs1, rs2 perform a floating point less than or equal comparison.

    :param dut:
    :return:
    """

### MULTIPLICATION ###

async def perform_multiplication(dut):
    """
    In the same format as mul rd, rs1, rs2 perform multiplication.

    :param dut:
    :return:
    """

### DIVISION ###

async def perform_division(dut):
    """
    In the same format as mul rd, rs1, rs2 perform multiplication.

    :param dut:
    :return:
    """

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
    await FallingEdge(dut.clk)

    # print values 
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
    await FallingEdge(dut.clk)

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
    await FallingEdge(dut.clk)

    # print values 
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
    await FallingEdge(dut.clk)

@cocotb.test()
async def test_perform_sub(dut):
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
    await perform_sub(dut)      # setup operation

    print("clock (test_perform_sub_1) = ", dut.clk.value)
    await FallingEdge(dut.clk)

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
    await FallingEdge(dut.clk)

@cocotb.test()
async def test_set_gt(dut):
    '''
    Docstring for test_set_gt
    
    :param dut: Description
    '''

@cocotb.test()
async def test_set_gte(dut):
    '''
    Docstring for test_set_gte
    
    :param dut: Description
    '''

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
