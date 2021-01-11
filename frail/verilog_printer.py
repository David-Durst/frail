from frail.ast import *
from typing import Set, Dict, List

@dataclass(eq=True, frozen=True)
class ModulePort:
    name: str
    width: int
    requires_clock: bool
    input_dir: bool
    input_from_other_scan: bool

tab_str = "    "
def get_tab_strs(num):
    final_tab_str = ""
    for i in range(num):
        final_tab_str += tab_str
    return final_tab_str

recurrence_seq_str = "scan_output_"
step_if_begin = get_tab_strs(2) + "if (step) begin\n"
step_if_end = get_tab_strs(2) + "end \n"
io_ports: Dict[int, List[ModulePort]] = {}
io_strs: Dict[int, str] = {}
# variables (logic type) used in the combinational block
var_strs: Dict[int, str] = {}
# combinational block
comb_strs: Dict[int, str] = {}
# sequential block (where the scan state is updated each clock)
seq_strs: Dict[int, str] = {}
printed_ops: Set[int] = set()
cur_scan_idx: int = -1
cur_scan_lambda_var: Var = None
output_scan_index: int = -1
VarTable: Dict[str, str] = {}
config_regs: List[AST] = []

def verilog_header(index: int, name: str="scan"):
    if name == "scan":
        return f"module {name}{index} ("
    else:
        return f"module {name} ("
verilog_footer = "endmodule\n"

def get_var_val(key):
    if key in VarTable.keys():
        return VarTable[key]
    return key


def print_verilog(e: AST,
                  root: bool = True,
                  lake_state: LakeDSLState = default_lake_state,
                  top_name: str = "top",
                  add_step: bool = True,
                  get_verilog: bool = True):
    global io_ports, io_strs, var_strs, comb_strs, seq_strs, printed_ops
    global cur_scan_idx, output_scan_index, cur_scan_lambda_var, VarTable, config_regs
    if root:
        io_ports = {}
        io_strs = {}
        var_strs ={}
        comb_strs = {}
        seq_strs = {}
        printed_ops = set()
        cur_scan_idx = -1
        output_scan_index = -1
        config_regs = []

    e_type = type(e)

    if e.index in printed_ops:
        # still need to add op to io_ports for this next module
        # for signals that are inputs to multiple submodules
        # so that this signal is printed in Verilog
        add_port = None
        if e_type == Var:
            if e == cur_scan_lambda_var:
                add_port = ModulePort(e.name, e.width, True, False, False)
            else:
                add_port = ModulePort(e.name, e.width, False, True, False)
        elif e_type == RecurrenceSeq:
            width = get_width(e.index, lake_state)
            add_port = ModulePort(recurrence_seq_str + str(e.producing_recurrence), width, False, True, True)

        if add_port is not None and add_port not in io_ports[cur_scan_idx]:
            io_ports[cur_scan_idx].append(add_port)
            
        return

    printed_ops.add(e.index)

    # start with empty string if printing expression not in a scan
    if not io_ports:
        io_ports[-1] = []

    if not io_strs:
        io_strs[-1] = ""

    if not var_strs:
        var_strs[-1] = ""

    if not comb_strs:
        comb_strs[-1] = ""

    if not seq_strs:
        seq_strs[-1] = ""

    if e_type == Var:
        # don't redefine the scan's lambda variable
        if e == cur_scan_lambda_var:
            add_port = ModulePort(e.name, e.width, True, False, False)
        else:
            config_regs.append(e)
            VarTable[f"x{e.index}"] = str(e.name)
            add_port = ModulePort(e.name, e.width, False, True, False)
        if add_port not in io_ports[cur_scan_idx]:
            io_ports[cur_scan_idx].append(add_port)
    elif e_type == Int:
        VarTable[f"x{e.index}"] = str(e.width) + "'d" + str(e.val)
    elif e_type == Bool:
        VarTable[f"x{e.index}"] = "1'b1" if e.val else "1'b0"
    elif e_type == RecurrenceSeq:
        VarTable[f"x{e.index}"] = recurrence_seq_str + str(e.producing_recurrence)
        width = get_width(e.index, lake_state)
        io_ports[cur_scan_idx].append(ModulePort(recurrence_seq_str + str(e.producing_recurrence), width, False, True, True))
        old_scan_idx = cur_scan_idx
        old_scan_lambda_var = cur_scan_lambda_var
        print_verilog(lake_state.program_map[e.producing_recurrence], False, lake_state)
        cur_scan_idx = old_scan_idx
        cur_scan_lambda_var = old_scan_lambda_var
    elif e_type == AddOp:
        arg0_str = get_var_val(print_arg(e.arg0_index, lake_state))
        arg1_str = get_var_val(print_arg(e.arg1_index, lake_state))
        print_define_and_assign(e, lake_state)
        comb_strs[cur_scan_idx] += f"{arg0_str} + {arg1_str}; \n"
    elif e_type == SubOp:
        arg0_str = get_var_val(print_arg(e.arg0_index, lake_state))
        arg1_str = get_var_val(print_arg(e.arg1_index, lake_state))
        print_define_and_assign(e, lake_state)
        comb_strs[cur_scan_idx] += f"{arg0_str} - {arg1_str}; \n"
    elif e_type == MulOp:
        arg0_str = get_var_val(print_arg(e.arg0_index, lake_state))
        arg1_str = get_var_val(print_arg(e.arg1_index, lake_state))
        print_define_and_assign(e, lake_state)
        comb_strs[cur_scan_idx] += f"{arg0_str} * {arg1_str}; \n"
    elif e_type == ModOp:
        arg0_str = get_var_val(print_arg(e.arg0_index, lake_state))
        arg1_str = get_var_val(print_arg(e.arg1_index, lake_state))
        print_define_and_assign(e, lake_state)
        comb_strs[cur_scan_idx] += f"{arg0_str} % {arg1_str}; \n"
    elif e_type == SelectBitsOp:
        arg0_str = get_var_val(print_arg(e.arg0_index, lake_state))
        print_define_and_assign(e, lake_state)
        comb_strs[cur_scan_idx] += f"{arg0_str}[{e.bits - 1} : 0]; \n"
    elif e_type == IfOp:
        b_str = get_var_val(print_arg(e.b_index, lake_state))
        arg0_str = get_var_val(print_arg(e.arg0_index, lake_state))
        arg1_str = get_var_val(print_arg(e.arg1_index, lake_state))
        print_define_and_assign(e, lake_state)
        comb_strs[cur_scan_idx] += f"{b_str} ? {arg0_str} : {arg1_str}; \n"
    elif e_type == EqOp:
        arg0_str = get_var_val(print_arg(e.arg0_index, lake_state))
        arg1_str = get_var_val(print_arg(e.arg1_index, lake_state))
        print_define_and_assign(e, lake_state)
        comb_strs[cur_scan_idx] += f"{arg0_str} == {arg1_str}; \n"
    elif e_type == ScanConstOp:
        if output_scan_index == -1:
            output_scan_index = e.index
        cur_scan_idx = e.index
        io_ports[cur_scan_idx] = []
        io_strs[cur_scan_idx] = ""
        var_strs[cur_scan_idx] = ""
        comb_strs[cur_scan_idx] = tab_str + "always_comb begin \n"
        if add_step:
            comb_strs[cur_scan_idx] += step_if_begin
        seq_strs[cur_scan_idx] = ""
        cur_scan_lambda_var = var_f("scan_var_" + str(cur_scan_idx), e.width)
        f_res = e.f(cur_scan_lambda_var)
        print_verilog(f_res, False, lake_state)
        # if read from output port, write to it in a sequential block. otherwise, just forward to next block
        read_from_output_port = False
        for port in io_ports[cur_scan_idx]:
            if port.input_dir:
                io_strs[cur_scan_idx] += tab_str + f"input logic [{port.width - 1}:0] {port.name},\n"
            else:
                add_io_str = tab_str + f"input logic clk, \n" + \
                                        tab_str + f"output logic [{port.width - 1}:0] {port.name},\n"
                io_strs[cur_scan_idx] = add_io_str + io_strs[cur_scan_idx]
                step_begin = step_if_begin if add_step else ""
                step_end = step_if_end if add_step else ""
                seq_strs[cur_scan_idx] = tab_str + f"always_ff @(posedge clk) begin\n" + \
                                         step_begin + \
                                         get_tab_strs(3) + f"{cur_scan_lambda_var.name} <= x{f_res.index};\n" + \
                                         step_end + \
                                         tab_str + "end\n"
                read_from_output_port = True
        # if don't read from output ports, need to add it here to list of output ports
        if not read_from_output_port:
            width = get_width(f_res.index, lake_state)
            io_strs[cur_scan_idx] = tab_str + f"output logic [{width - 1}:0] {cur_scan_lambda_var.name}, \n" + io_strs[cur_scan_idx]
            comb_strs[cur_scan_idx] += get_tab_strs(3) + f"{cur_scan_lambda_var.name} = x{f_res.index}; \n"
            io_ports[cur_scan_idx].append(ModulePort(cur_scan_lambda_var.name, width, False, False, False))
        # end step if
        if add_step:
            comb_strs[cur_scan_idx] += step_if_end
        # end always_comb block
        comb_strs[cur_scan_idx] += tab_str + "end \n"
    else:
        assert False, str(e) + "is not a valid frail operator"

    if root:
        keys = sorted(comb_strs.keys())

        # IO for top wrapper module
        top_module_io = []
        # intermediate signal declarations for sources
        # and sinks between module instances
        inter_logics = []
        # strings instantiating modules and wiring up
        # module IO
        module_inst_strs = []
        # signals that are inputs to modules that need
        # to be later checked to determine if source
        # comes from another module instantiation or
        # needs to come from top level IO
        inter_to_check = {}

        if get_verilog:
            for k in keys:
                if k == -1:
                    continue

                mod_str_from_ports(io_ports,
                                top_module_io,
                                inter_logics,
                                module_inst_strs,
                                inter_to_check,
                                k,
                                add_step)

            print_top_level_module(top_module_io,
                                inter_logics,
                                module_inst_strs,
                                inter_to_check,
                                lake_state,
                                top_name,
                                add_step)

            for k in keys:
                if k == -1:
                    continue

                print(verilog_header(k))
                if add_step:
                    print(tab_str +"input logic step,")
                # get rid of comma after last io signal and end io
                print(io_strs[k][:-2] + "\n);")
                print(var_strs[k])
                print(comb_strs[k], end='')

                # add a line between combinational and sequential logic blocks
                if comb_strs[k] != "" and seq_strs[k] != "":
                    print()

                print(seq_strs[k], end='')
                print(verilog_footer)

        else:
            get_kratos_wrapper(config_regs)


def print_arg(arg_index: int, lake_state: LakeDSLState):
    print_verilog(lake_state.program_map[arg_index], False, lake_state)
    if arg_index == cur_scan_lambda_var.index:
        return cur_scan_lambda_var.name
    else:
        return "x" + str(arg_index)

def get_width(arg_index: int, lake_state: LakeDSLState):
    ast_obj = lake_state.program_map[arg_index]
    if hasattr(ast_obj, "width"):
        return ast_obj.width
    elif hasattr(ast_obj, "bits"):
        return ast_obj.bits
    elif isinstance(ast_obj, BinOp):
        return max(get_width(ast_obj.arg0_index, lake_state), get_width(ast_obj.arg1_index, lake_state))
    elif isinstance(ast_obj, ScanConstOp):
        return ast_obj.width
    elif isinstance(ast_obj, RecurrenceSeq):
        return get_width(ast_obj.producing_recurrence, lake_state)
    elif isinstance(ast_obj, EqOp):
        return ast_obj
    else:
        raise ValueError("unrecognized object: " + str(ast_obj))

def print_define_and_assign(arg: AST, lake_state: LakeDSLState):
    print_logic(arg, lake_state)
    print_assign(arg)

def print_logic(arg: AST, lake_state: LakeDSLState):
    width = get_width(arg.index, lake_state)
    if width == 1:
        var_strs[cur_scan_idx] += tab_str + f"logic x{arg.index}; \n"
    else:
        var_strs[cur_scan_idx] += tab_str + f"logic [{width - 1}:0] x{arg.index}; \n"

def print_assign(arg: AST):
    comb_strs[cur_scan_idx] += get_tab_strs(3) + f"x{arg.index} = "

def mod_str_from_ports(io_ports: Dict[int, List[ModulePort]],
                       top_module_io: list,
                       inter_logics: list,
                       module_inst_strs: list,
                       inter_to_check: Dict[str, str],
                       k: int,
                       add_step: bool):

    module_inst_str = ""
    needs_clock = False
    
    for port in io_ports[k]:
        # check if module requires clock
        if port.requires_clock:
            needs_clock = True

        # signals that may need to be connected between modules
        # output signals need to be stored, as later scans can depend on them
        if not port.input_dir:
            inter_str = port.name.replace("var", "inter")
            # create intermediate signal at top level module to
            #  connect sources and sinks between modules
            # these are output signals, so safe to create these
            #  intermediate signals
            inter_full_str = f"logic [{port.width - 1}:0] {inter_str};"
            inter_logics.append(inter_full_str)
        # input signals that are from other scans will need to be wired up
        elif port.input_from_other_scan and port.input_dir:
            inter_str = port.name.replace("output", "inter")
            inter_to_check[inter_str] = tab_str + f"input logic [{port.width - 1}:0] {inter_str},"
        # signals that go to the top level as inputs that have no source scan
        else:
            io = "input" if port.input_dir else "output"
            io_str = f"{io} logic [{port.width - 1}:0] {port.name},"
            add_to_top = tab_str + io_str
            # multiple modules may have the same port, add to top module IO only once
            if add_to_top not in top_module_io:
                top_module_io.append(add_to_top)
            inter_str = port.name
        module_port_str = get_tab_strs(2) + f".{port.name}({inter_str}),\n"
        module_inst_str += module_port_str

    if add_step:
        module_inst_str = get_tab_strs(2) + ".step(step),\n" + module_inst_str

    # wire clk input to module only if clk is an input
    if needs_clock:
        module_inst_str = get_tab_strs(2) + ".clk(clk),\n" + module_inst_str

    module_inst_str = tab_str + f"scan{k} scan{k} (\n" + module_inst_str

    module_inst_str = module_inst_str[0:-2] + f"\n{tab_str});\n"
    module_inst_strs.append(module_inst_str)


def print_top_level_module(top_module_io: list,
                           inter_logics: list,
                           module_inst_strs: list,
                           inter_to_check: Dict[str, str],
                           lake_state: LakeDSLState,
                           top_name: str,
                           add_step: bool):
    global output_scan_index

    print(verilog_header(0, top_name) + "\n")
    for check in inter_to_check.keys():
        add = True
        for logic in inter_logics:
            # check if this intermediate signal is has a source
            # from one of the module instances (if not, add
            # to top level i/o)
            if logic[0:-1] in inter_to_check[check]:
                add = False
                break
        if add and inter_to_check[check] not in top_module_io:
            top_module_io.append(inter_to_check[check])

    # sort so that inputs are printed before outputs
    top_module_io = sorted(top_module_io)

    if add_step:
        top_module_io.insert(0, tab_str + "input logic step,")

    # add clk to top level IO as first input
    top_module_io.insert(0, tab_str + "input logic clk,")

    # print top level module io (signal has only one source
    # or sink in instantiated modules)
    top_io_str = ""
    for i in range(len(top_module_io)):
        top_io_str += top_module_io[i] + "\n"
    top_io_str += tab_str + f"output logic [{lake_state.program_map[output_scan_index].width - 1}:0] addr_out\n"
    print(top_io_str + ");\n")

    # print intermediate signals to wire up sources
    # sinks between module instances
    for logic in inter_logics:
        print(tab_str + logic)
    print()

    # print module instances
    for mod in module_inst_strs:
        print(mod)
    print(tab_str + f"always_comb begin\n{get_tab_strs(2)} addr_out = scan_inter_{output_scan_index};\n{tab_str}end")
    print(verilog_footer)

def get_kratos_wrapper(config_regs: list):

    print(f"""from kratos import *
from lake.attributes.config_reg_attr import ConfigRegAttr
from lake.attributes.formal_attr import FormalAttr, FormalSignalConstraint


class Addressor(Generator):

    def __init__(self,
                name):
        super().__init__(name)

        # external module with Verilog generated from frail
        self.external = True

        self.clk = self.clock("clk")

        self.step = self.input("step", width=1)
        self.addr_out = self.output("addr_out", width=16)""")

    if len(config_regs) > 0:
        print()
        print(get_tab_strs(2) + "# configuration registers")

    for config in config_regs:
        print(get_tab_strs(2) + f'self.{config.name} = self.input("{config.name}", width={config.width})')

    print()

    print(f"""class AddressorWrapper(Generator):

    def __init__(self,
                 name):
        wrapper_name = name + "_wrapper"
        super().__init__(wrapper_name)

        self.clk = self.clock("clk")

        self.step = self.input("step", width=1)
        self.addr_out = self.output("addr_out", width=16)""")

    if len(config_regs) > 0:
        print()
        print(get_tab_strs(2) + "# configuration registers")

    for config in config_regs:
        print()
        print(get_tab_strs(2) + f'self.{config.name} = self.input("{config.name}", width={config.width})')
        print(get_tab_strs(2) + f'self.{config.name}.add_attribute(ConfigRegAttr("{config.name}"))')
        print(get_tab_strs(2) + f'self.{config.name}.add_attribute(FormalAttr(self.{config.name}.name, FormalSignalConstraint.SOLVE))')

    print()
    print(get_tab_strs(2) + f'addressor = Addressor(name)')
    print(get_tab_strs(2) + f'self.add_child("addressor", addressor,')

    for signal in ("clk", "step", "addr_out"):
        print(get_tab_strs(3), f"{signal}=self.{signal},")

    for i in range(len(config_regs)):
        config = config_regs[i]
        print_config = get_tab_strs(3) + f"{config.name}=self.{config.name}"
        if i != len(config_regs) - 1:
            print_config += ","
        else:
            print_config += ")"

        print(print_config)
    