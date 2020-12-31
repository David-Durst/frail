import magma as m
import fault
import time
import tempfile
import shutil
import os
import pathlib


def test_addr_design_a():
    frail_dir = pathlib.Path(__file__).parent.parent.absolute()

    design_a_dut = m.define_from_verilog_file(
        f"{frail_dir}/verilog/design_a.v",
        target_modules=["design_a"],
        type_map={
            "clk": m.In(
                m.Clock)})[0]
    print(f"Imported as magma circuit: {design_a_dut}")

    tester = fault.Tester(design_a_dut, design_a_dut.clk)

    # no need to rst_n or clk_en yet

    # config regs
    tester.circuit.x_max = 3
    tester.circuit.x_stride = 1
    tester.circuit.y_max = 4
    tester.circuit.y_stride = 2
    tester.circuit.offset = 0

    for i in range(12):

        tester.step(2)

        tester.eval()

    with tempfile.TemporaryDirectory() as tempdir:
        shutil.copy(f"{frail_dir}/verilog/design_a.v", tempdir)
        tester.compile_and_run(target="verilator",
                               directory=tempdir,
                               skip_compile=True,
                               flags=["-Wno-fatal"])


if __name__ == "__main__":
    test_addr_design_a()
