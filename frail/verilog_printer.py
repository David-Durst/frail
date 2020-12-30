from frail.ast import *
from typing import Set, Dict, List

@dataclass(eq=True, frozen=True)
class ModulePort:
    name: str
    width: int
    requires_clock: bool
    input_dir: bool

tab_str = "    "
recurrence_seq_str = "scan_output_"
io_ports: Dict[int, List[ModulePort]] = {}
io_strs: Dict[int, str] = {}
# parameters that are fixed every run
param_strs: Dict[int, str] = {}
# variables (logic type) used in the combinational block
var_strs: Dict[int, str] = {}
# combinational block
comb_strs: Dict[int, str] = {}
# sequential block (where the scan state is updated each clock)
seq_strs: Dict[int, str] = {}
printed_ops: Set[int] = set()
cur_scan_idx: int = -1
cur_scan_lambda_var: Var = None
VarTable: Dict[str, str] = {}
def verilog_header(index: int, name: str="scan"):
    return f"module {name}{index} ("
verilog_footer = "endmodule\n"

def get_var_val(key):
    if key in VarTable.keys():
        return VarTable[key]
    return key


def print_verilog(e: AST, root: bool = True, lake_state: LakeDSLState = default_lake_state):
    global io_ports, io_strs, param_strs, var_strs, comb_strs, seq_strs, printed_ops, cur_scan_idx, cur_scan_lambda_var, VarTable
    if root:
        io_ports = {}
        io_strs = {}
        param_strs = {}
        var_strs ={}
        comb_strs = {}
        seq_strs = {}
        printed_ops = set()
        cur_scan_idx = -1

    if e.index in printed_ops:
        return

    printed_ops.add(e.index)
    e_type = type(e)
    # start with empty string if printing expression not in a scan
    if not io_ports:
        io_ports[-1] = []

    if not io_strs:
        io_strs[-1] = ""

    if not param_strs:
        param_strs[-1] = ""

    if not var_strs:
        var_strs[-1] = ""

    if not comb_strs:
        comb_strs[-1] = ""

    if not seq_strs:
        seq_strs[-1] = ""

    if e_type == Var:
        # don't redefine the scan's lambda variable
        if e == cur_scan_lambda_var:
            io_ports[cur_scan_idx].append(ModulePort(e.name, e.width, True, False))
        else:
            VarTable[f"x{e.index}"] = str(e.name)
            param_strs[cur_scan_idx] += tab_str + f"input logic [{e.width - 1}:0] {e.name}, \n"
    elif e_type == Int:
        VarTable[f"x{e.index}"] = str(e.width) + "'d" + str(e.val)
    elif e_type == Bool:
        VarTable[f"x{e.index}"] = "1'b1" if e.val else "1'b0"
    elif e_type == RecurrenceSeq:
        VarTable[f"x{e.index}"] = recurrence_seq_str + str(e.producing_recurrence)
        width = get_width(e.index, lake_state)
        io_ports[cur_scan_idx].append(ModulePort(recurrence_seq_str + str(e.producing_recurrence), width, False, True))
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
        cur_scan_idx = e.index
        io_ports[cur_scan_idx] = []
        io_strs[cur_scan_idx] = ""
        param_strs[cur_scan_idx] = ""
        var_strs[cur_scan_idx] = ""
        comb_strs[cur_scan_idx] = tab_str + "always_comb begin \n"
        seq_strs[cur_scan_idx] = ""
        cur_scan_lambda_var = var_f("scan_var_" + str(cur_scan_idx))
        f_res = e.f(cur_scan_lambda_var)
        print_verilog(f_res, False, lake_state)
        comb_strs[cur_scan_idx] += tab_str + "end \n"
        # if read from output port, write to it in a sequential block. otherwise, just forward to next block
        read_from_output_port = False
        for port in io_ports[cur_scan_idx]:
            if port.input_dir:
                io_strs[cur_scan_idx] += tab_str + f"input logic [{port.width - 1}:0] {port.name}\n"
            else:
                io_strs[cur_scan_idx] = tab_str + "input logic clk, \n" + \
                                        tab_str + f"output logic [{port.width - 1}:0] {port.name}\n" + io_strs[cur_scan_idx]
                seq_strs[cur_scan_idx] = tab_str + "always_ff @(posedge clk) begin\n" + \
                                         tab_str + tab_str + f"{cur_scan_lambda_var.name} <= x{f_res.index};\n" + \
                                         tab_str + "end\n"
                read_from_output_port = True
        # if don't read from output ports, need to add it here to list of output ports
        if not read_from_output_port:
            width = get_width(f_res.index, lake_state)
            io_strs[cur_scan_idx] = tab_str + f"output logic [{width - 1}:0] x{f_res.index}, \n" + io_strs[cur_scan_idx]
            io_ports[cur_scan_idx].append(ModulePort("x" + str(f_res.index), width, False, False))
    else:
        assert False, str(e) + "is not a valid frail operator"

    if root:
        keys = sorted(param_strs.keys())

        module_inst_strs = []
        top_module_io = []
        inter_logics = []
        inter_assigns = []
        for k in keys:
            if k == -1:
                continue
            module_inst_str = f"scan{k}inst scan{k} (\n"
            for port in io_ports[k]:
                if "output" in port.name or "var" in port.name:
                    if port.input_dir:
                        inter_str = port.name.replace("output", "inter")
                    else:
                        inter_str = port.name.replace("var", "inter")
                        if inter_str not in inter_logics:
                            inter_logics.append(f"logic [{port.width - 1}:0] {inter_str};")
                            inter_assigns.append(f"assign {inter_str} = {port.name};")
                else:
                    io = "input" if port.input_dir else "output"
                    io_str = f"{io} logic [{port.width - 1}:0] {port.name},"
                    if io_str not in top_module_io:
                        top_module_io.append(tab_str + io_str)
                    inter_str = port.name
                module_inst_str += tab_str + f".{port.name}({inter_str}),\n"

            module_inst_str = module_inst_str[0:-2] + "\n);\n"
            module_inst_strs.append(module_inst_str)

        print(verilog_header(0, "top") + "\n")
        for i in range(len(top_module_io)):
            if i == len(top_module_io) - 1:
                print(top_module_io[i][:-2] + "\n);\n")
            else:
                print(top_module_io[i])

        for logic in inter_logics:
            print(logic)
        print()
        for assign in inter_assigns:
            print(assign)
        print()
        for mod in module_inst_strs:
            print(mod)
            
        for k in keys:
            if k == -1:
                continue

            print(verilog_header(k))
            # get rid of comma after last io signal and end io
            io_port_str = io_strs[k] + param_strs[k]
            print(io_port_str[0:-3] + "\n);")
            print(var_strs[k])
            print(comb_strs[k], end='')

            # add a line between combinational and sequential logic blocks
            if comb_strs[k] != "" and seq_strs[k] != "":
                print()

            print(seq_strs[k], end='')
            print(verilog_footer)


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
    comb_strs[cur_scan_idx] += tab_str + tab_str + f"x{arg.index} = "

# def print_top_module(io_ports: Dict[int, List[ModulePort]]):

