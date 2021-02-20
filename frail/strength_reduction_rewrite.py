from frail.ast import *
from typing import Set, Dict, List

@dataclass(eq=True, frozen=True)
class ModulePort:
    name: str
    width: int
    requires_clock: bool
    input_dir: bool
    input_from_other_scan: bool
    # true if this is the max signal from a counter, false it's the val, None if this is not from a counter
    counter_max: bool = None

tab_str = "    "
def get_tab_strs(num):
    final_tab_str = ""
    for i in range(num):
        final_tab_str += tab_str
    return final_tab_str

recurrence_seq_str = "scan_output_"
counter_max_output = "counter_at_max_"
counter_val_output = "counter_val_"
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
to_delete: List[int] = []
mul_list = {}

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


def strength_reduction_rewrite(e: AST,
                               root: bool = True,
                               lake_state: LakeDSLState = default_lake_state,
                               top_name: str = "top",
                               add_step: bool = True,
                               get_verilog: bool = True):
    global io_ports, io_strs, var_strs, comb_strs, seq_strs, printed_ops
    global cur_scan_idx, output_scan_index, cur_scan_lambda_var, VarTable, config_regs
    global to_delete, mul_list

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
        to_delete = []

    e_type = type(e)
    print("INFO", cur_scan_idx, e_type)
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

    replace_counter = None
    if e_type == RecurrenceSeq:
        old_scan_idx = cur_scan_idx
        old_scan_lambda_var = cur_scan_lambda_var
        strength_reduction_rewrite(lake_state.program_map[e.producing_recurrence], False, lake_state)
        cur_scan_idx = old_scan_idx
        cur_scan_lambda_var = old_scan_lambda_var
    elif e_type == CounterSeq:
        old_scan_idx = cur_scan_idx
        old_scan_lambda_var = cur_scan_lambda_var
        strength_reduction_rewrite(lake_state.program_map[e.producing_counter], False, lake_state)
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
        # print(type(lake_state.program_map[e.arg0_index]))
        # print(type(lake_state.program_map[e.arg1_index]))
        if isinstance(lake_state.program_map[e.arg0_index], CounterSeq):
            replace_counter = e.arg0_index
            replace_arg = 0
        elif isinstance(lake_state.program_map[e.arg1_index], CounterSeq):
            replace_counter = e.arg1_index
            replace_arg = 1
        if replace_counter is not None:
            og_counter_op = lake_state.program_map[lake_state.program_map[replace_counter].producing_counter]
            incr_amount_index = e.arg0_index if replace_arg == 1 else e.arg1_index
            incr_amount_op = lake_state.program_map[incr_amount_index]
            new_index = lake_state.incr()
            lake_state.program_map[e.index] = \
                counter_f(og_counter_op.prev_level_input, og_counter_op.at_max(), incr_amount_op)
            """ CounterOp(index=new_index,
                        prev_level_input=og_counter_op.prev_level_input,
                        max_val=og_counter_op.at_max(),
                        is_max_wire=True,
                        incr_amount=incr_amount_op,
                        width=og_counter_op.width) """
            # to_delete.append(e.index)
            mul_list[e.index] = new_index
        else:
            arg0_str = get_var_val(print_arg(e.arg0_index, lake_state))
            arg1_str = get_var_val(print_arg(e.arg1_index, lake_state))
            print_define_and_assign(e, lake_state)
            VarTable[f"x_{e.index}"] = f"{arg0_str} * {arg1_str}; \n"
            comb_strs[cur_scan_idx] += VarTable[f"x_{e.index}"]
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
    elif e_type == LTOp:
        arg0_str = get_var_val(print_arg(e.arg0_index, lake_state))
        arg1_str = get_var_val(print_arg(e.arg1_index, lake_state))
        print_define_and_assign(e, lake_state)
        comb_strs[cur_scan_idx] += f"{arg0_str} < {arg1_str}; \n"
    elif e_type == GTOp:
        arg0_str = get_var_val(print_arg(e.arg0_index, lake_state))
        arg1_str = get_var_val(print_arg(e.arg1_index, lake_state))
        print_define_and_assign(e, lake_state)
        comb_strs[cur_scan_idx] += f"{arg0_str} > {arg1_str}; \n"
    elif e_type == CounterOp:
        if output_scan_index == -1:
            output_scan_index = e.index
        cur_scan_idx = e.index

        io_ports[cur_scan_idx] = []
        # add output port
        io_ports[cur_scan_idx].append(ModulePort(counter_val_output + str(e.index), e.width, True, False, False, False))
        io_ports[cur_scan_idx].append(ModulePort(counter_max_output + str(e.index), e.width, True, False, False, True))
        io_strs[cur_scan_idx] = ""
        var_strs[cur_scan_idx] = ""
        comb_strs[cur_scan_idx] = tab_str + "always_comb begin \n"
        seq_strs[cur_scan_idx] = ""
        cur_scan_lambda_var = var_f("scan_var_" + str(cur_scan_idx), e.width)
        if e.prev_level_input is not None:
            strength_reduction_rewrite(lake_state.program_map[e.prev_level_input], False, lake_state)
            enable_signal = io_ports[cur_scan_idx][-1].name
        else:
            enable_signal = "1'b1"
        if e.is_max_wire:
            strength_reduction_rewrite(lake_state.program_map[e.max_val], False, lake_state)
            max_signal = io_ports[cur_scan_idx][-1].name
        else:
            max_signal = f"{e.width}'d{e.max_val}"

        # logic of checking max output, then incrementing if prev_level_input says so and not at max
        comb_strs[cur_scan_idx] += get_tab_strs(3) + f"{counter_max_output}{e.index} = {counter_val_output}{e.index} == {max_signal} - {e.width}'b1;\n"
        # what are step?
        step_begin = step_if_begin if add_step else ""
        step_end = step_if_end if add_step else ""
        
        seq_strs[cur_scan_idx] = tab_str + f"always_ff @(posedge clk) begin\n" + \
                                 step_begin + \
                                 get_tab_strs(3) + \
                                    f"{counter_val_output}{e.index} <= {enable_signal} ? " +\
                                    f"({counter_max_output}{e.index} " + \
                                    f"? {e.width}'b0 : {counter_val_output}{e.index} + {e.width}'d{e.incr_amount})" + \
                                    f": {counter_val_output}{e.index}; \n" + \
                                 step_end + \
                                 tab_str + "end\n"

        # if read from output port, write to it in a sequential block. otherwise, just forward to next block
        # manually added all output fports in this block
        for port in io_ports[cur_scan_idx]:
            if port.input_dir:
                io_strs[cur_scan_idx] += tab_str + f"input logic [{port.width - 1}:0] {port.name},\n"
            else:
                io_strs[cur_scan_idx] = tab_str + f"output logic [{port.width - 1}:0] {port.name},\n" + io_strs[cur_scan_idx]
        # add clk
        io_strs[cur_scan_idx] += tab_str + f"input logic clk \n"
        # end always_comb block
        comb_strs[cur_scan_idx] += tab_str + "end \n"
    elif e_type == ScanConstOp:
        if output_scan_index == -1:
            output_scan_index = e.index
        cur_scan_idx = e.index
        cur_scan_lambda_var = var_f("scan_var_" + str(cur_scan_idx), e.width)
        f_res = e.f(cur_scan_lambda_var)
        
        strength_reduction_rewrite(f_res, False, lake_state)
        # lake_state.program_map[cur_scan_idx] = scan_const_f(lambda z: res)

    if root:
        return e, lake_state
        """ for d in to_delete:
            del lake_state.program_map[d]
        # for k in lake_state.program_map.keys():
            # print(lake_state.program_map[k])

    if replace_counter is not None:
        return lake_state.program_map[new_index], lake_state
    return e, lake_state """


def print_arg(arg_index: int, lake_state: LakeDSLState):
    strength_reduction_rewrite(lake_state.program_map[arg_index], False, lake_state)
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
    elif isinstance(ast_obj, CounterSeq):
        return get_width(ast_obj.producing_counter, lake_state)
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
    if isinstance(lake_state.program_map[output_scan_index], CounterOp):
        print(tab_str + f"always_comb begin\n{get_tab_strs(2)} addr_out = counter_val_{output_scan_index};\n{tab_str}end")
    else:
        print(tab_str + f"always_comb begin\n{get_tab_strs(2)} addr_out = scan_inter_{output_scan_index};\n{tab_str}end")
    print(verilog_footer)