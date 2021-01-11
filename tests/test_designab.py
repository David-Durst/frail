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
@pytest.mark.parametrize("design", ["og_design", "op_design"])
def test_addr_design(
        test_rand,
        design,
        starting_addr=0,
        strides_0=15,
        strides_1=13,
        ranges_0=2,
        ranges_1=13):

    if test_rand:
        max_value = 2**5
        starting_addr = random.randint(0, max_value - 1)
        strides_0 = random.randint(0, max_value - 1)
        strides_1 = random.randint(0, max_value - 1)
        ranges_0 = random.randint(0, max_value - 1)
        ranges_1 = random.randint(0, max_value - 1)

    print(starting_addr, strides_0, strides_1, ranges_0, ranges_1)

    # set up frail design with Verilog
    frail_dir = pathlib.Path(__file__).parent.parent.absolute()
    print(frail_dir)
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

    x = [f"ranges_{i}" for i in range(4)]
    y = [f"strides_{i}" for i in range(4)]
    r = [2, 4, 14, 1]
    s = [4, 1, 4, 0]
    tester.circuit.dim = 4
    for i in range(len(x)):
        setattr(tester.circuit, x[i], r[i])
        setattr(tester.circuit, y[i], s[i])

    # set up addressor model
    model_ag = AddrGenModel(4, 16)

    config = {}
    for i in range(len(x)):
        config[x[i]] = r[i]
        config[y[i]] = s[i]
    config["dimensionality"] = 4

    model_ag.set_config(config)

    tester.circuit.step = 1

    for i in range(min(1000, 2*4*14 - 1)):
        # start with first addr on rising clk edge
        tester.circuit.clk = 1
        tester.step(2)
        tester.eval()
        model_ag.step()
        tester.circuit.addr_out.expect(model_ag.get_address())
        # print(model_ag.get_address())

    with tempfile.TemporaryDirectory() as tempdir:
        tempdir = design
        shutil.copy(f"{frail_dir}/verilog/{design}.v", tempdir)
        tester.compile_and_run(target="verilator",
                               directory=tempdir,
                               skip_compile=True,
                               #flags=["-Wno-fatal"])
                               flags=["-Wno-fatal", "--trace"])


if __name__ == "__main__":
    test_addr_design(False, "og_design6")#, 0, 15, 20, 12, 15)
