import magma as m
import fault
import time
import tempfile
import os
design_a_dut = m.define_from_verilog_file("/home/skavya/frail/design_a.v", target_modules=["design_a"], type_map={"clk": m.In(m.Clock)})[0]
print(f"Imported as magma circuit: {design_a_dut}")

tester = fault.Tester(design_a_dut, design_a_dut.clk)

# no need to rst_n or clk_en yet

# config regs
tester.circuit.x_max = 2
tester.circuit.x_stride = 1
tester.circuit.y_max = 3
tester.circuit.y_stride = 2
tester.circuit.offset = 0

for i in range(15):

    tester.step(2)

    tester.eval()

with tempfile.TemporaryDirectory() as tempdir:
    tempdir = "design_a"
    tester.compile_and_run(target="verilator",
                           skip_compile=True,
                           directory=tempdir,
                           flags=["-Wno-fatal", "--trace"])