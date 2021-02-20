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
        print("e BEFORE", e)
        e_after = strength_reduction_rewrite(lake_state.program_map[e.producing_recurrence], False, lake_state)
        print("e AFTER", e_after)
        cur_scan_idx = old_scan_idx
        cur_scan_lambda_var = old_scan_lambda_var
    elif e_type == CounterSeq:
        old_scan_idx = cur_scan_idx
        old_scan_lambda_var = cur_scan_lambda_var
        print("e BEFORE", e)
        e_after = strength_reduction_rewrite(lake_state.program_map[e.producing_counter], False, lake_state)
        print("e AFTER", e_after)
        cur_scan_idx = old_scan_idx
        cur_scan_lambda_var = old_scan_lambda_var
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
            e = counter_f(og_counter_op.prev_level_input, og_counter_op.at_max(), incr_amount_op)
            """ CounterOp(index=new_index,
                        prev_level_input=og_counter_op.prev_level_input,
                        max_val=og_counter_op.at_max(),
                        is_max_wire=True,
                        incr_amount=incr_amount_op,
                        width=og_counter_op.width) """
            # to_delete.append(e.index)
            mul_list[e.index] = e.val()
    elif e_type == CounterOp:
        if output_scan_index == -1:
            output_scan_index = e.index
        cur_scan_idx = e.index

        cur_scan_lambda_var = var_f("scan_var_" + str(cur_scan_idx), e.width)
        if e.prev_level_input is not None:
            strength_reduction_rewrite(lake_state.program_map[e.prev_level_input], False, lake_state)
        if e.is_max_wire:
            strength_reduction_rewrite(lake_state.program_map[e.max_val], False, lake_state)

    elif e_type == ScanConstOp:
        if output_scan_index == -1:
            output_scan_index = e.index
        cur_scan_idx = e.index
        cur_scan_lambda_var = var_f("scan_var_" + str(cur_scan_idx), e.width)
        f_res = e.f(cur_scan_lambda_var)
        e_ret = strength_reduction_rewrite(f_res, False, lake_state)
        if isinstance(e_ret, CounterOp):
            e = e_ret

    if root:
        return e
    return e
        