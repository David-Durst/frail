import magma as m
import fault
import time
import tempfile
import shutil
import os
import pathlib
import pytest
import random

from lake.models.addr_gen_model import AddrGenModel
from lake.utils.util import transform_strides_and_ranges


@pytest.mark.parametrize("test_rand", [False, True])
@pytest.mark.parametrize("design", ["design_a", "design_b"])
def test_addr_design(
        test_rand,
        design,
        starting_addr=0,
        strides_0=1,
        strides_1=2,
        ranges_0=3,
        ranges_1=4):

    if test_rand:
        starting_addr = random.randint(0, 2**16 - 1)
        strides_0 = random.randint(0, 2**16 - 1)
        strides_1 = random.randint(0, 2**16 - 1)
        ranges_0 = random.randint(0, 2**16 - 1)
        ranges_1 = random.randint(0, 2**16 - 1)

    # print(starting_addr, strides_0, strides_1, ranges_0, ranges_1)

    # set up addressor model
    model_ag = AddrGenModel(2, 16)

    config = {}
    config["starting_addr"] = starting_addr
    config["dimensionality"] = 2
    config["strides_0"] = strides_0
    config["strides_1"] = strides_1
    config["ranges_0"] = ranges_0
    config["ranges_1"] = ranges_1

    model_ag.set_config(config)

    # set up frail design with Verilog
    frail_dir = pathlib.Path(__file__).parent.parent.absolute()

    # get Magma circuit from Verilog
    dut = m.define_from_verilog_file(
        f"{frail_dir}/verilog/{design}.v",
        target_modules=[design],
        type_map={
            "clk": m.In(
                m.Clock)})[0]
    print(f"Imported as magma circuit: {dut}")

    tester = fault.Tester(dut, dut.clk)

    # no need to rst_n or clk_en yet

    # config regs
    if design == "design_b":
        tranges, tstrides = transform_strides_and_ranges(
            [ranges_0, ranges_1],
            [strides_0, strides_1],
            2)
        tester.circuit.x_max = tranges[0]
        tester.circuit.x_stride = tstrides[0]
        tester.circuit.y_max = tranges[1]
        tester.circuit.y_stride = tstrides[1]
        tester.circuit.offset = starting_addr
    else:
        tester.circuit.x_max = ranges_0
        tester.circuit.x_stride = strides_0
        tester.circuit.y_max = ranges_1
        tester.circuit.y_stride = strides_1
        tester.circuit.offset = starting_addr

    for i in range(100):

        tester.eval()
        tester.step(2)
        #tester.circuit.addr.expect(model_ag.get_address())
        print(model_ag.get_address())
        model_ag.step()

    with tempfile.TemporaryDirectory() as tempdir:
        tempdir = design
        shutil.copy(f"{frail_dir}/verilog/{design}.v", tempdir)
        tester.compile_and_run(target="verilator",
                               directory=tempdir,
                               skip_compile=True,
                               flags=["-Wno-fatal", "--trace"])


if __name__ == "__main__":
    test_addr_design(False, "design_b", 0, 15, 20, 12, 13)
