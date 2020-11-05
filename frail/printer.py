from frail.ast import *
from typing import Set, Dict

indent_str = "  "
recurrence_seq_str = "scan_const"
scan_strs: Dict[int, str] = {}
printed_ops: Set[int] = set()


def print_frail(e: AST, cur_scan_idx: int = -1, root: bool = True, lake_state: LakeDSLState = default_lake_state):
    global scan_strs, printed_ops
    if root:
        scan_strs = {}
        printed_ops = set()

    e_type = type(e)
    # start with empty string if printing expression not in a scan
    if not scan_strs:
        scan_strs[-1] = ""

    if e_type == Var:
        print_let(e, cur_scan_idx)
        scan_strs[cur_scan_idx] = scan_strs[cur_scan_idx] + "Var(" + str(e.name) + ")"
    elif e_type == Int:
        print_let(e, cur_scan_idx)
        scan_strs[cur_scan_idx] = scan_strs[cur_scan_idx] + str(e.val)
    elif e_type == Bool:
        print_let(e, cur_scan_idx)
        scan_strs[cur_scan_idx] = scan_strs[cur_scan_idx] + str(e.val)
    elif e_type == RecurrenceSeq:
        print_let(e, cur_scan_idx)
        scan_strs[cur_scan_idx] = scan_strs[cur_scan_idx] + recurrence_seq_str + str(e.producing_recurrence)
        print_frail(lake_state.program_map[e.producing_recurrence], cur_scan_idx, False, lake_state)
    elif e_type == AddOp:
        arg0_str = print_arg(e.arg0_index, cur_scan_idx, lake_state)
        arg1_str = print_arg(e.arg1_index, cur_scan_idx, lake_state)
        print_let(e, cur_scan_idx)
        scan_strs[cur_scan_idx] = scan_strs[cur_scan_idx] + arg0_str + " + " + arg1_str
    elif e_type == MulOp:
        arg0_str = print_arg(e.arg0_index, cur_scan_idx, lake_state)
        arg1_str = print_arg(e.arg1_index, cur_scan_idx, lake_state)
        print_let(e, cur_scan_idx)
        scan_strs[cur_scan_idx] = scan_strs[cur_scan_idx] + arg0_str + " * " + arg1_str
    elif e_type == ModOp:
        arg0_str = print_arg(e.arg0_index, cur_scan_idx, lake_state)
        arg1_str = print_arg(e.arg1_index, cur_scan_idx, lake_state)
        print_let(e, cur_scan_idx)
        scan_strs[cur_scan_idx] = scan_strs[cur_scan_idx] + arg0_str + " % " + arg1_str
    elif e_type == SelectBitsOp:
        arg0_str = print_arg(e.arg0_index, cur_scan_idx, lake_state)
        print_let(e, cur_scan_idx)
        scan_strs[cur_scan_idx] = scan_strs[cur_scan_idx] + "select_bits(" + arg0_str + ", " + str(e.bits) + ")"
    elif e_type == IfOp:
        b_str = print_arg(e.b_index, cur_scan_idx, lake_state)
        arg0_str = print_arg(e.arg0_index, cur_scan_idx, lake_state)
        arg1_str = print_arg(e.arg1_index, cur_scan_idx, lake_state)
        print_let(e, cur_scan_idx)
        scan_strs[cur_scan_idx] = scan_strs[cur_scan_idx] + "if(" + b_str + ", " + arg0_str + ", " + arg1_str + ")"
    elif e_type == EqOp:
        arg0_str = print_arg(e.arg0_index, cur_scan_idx, lake_state)
        arg1_str = print_arg(e.arg1_index, cur_scan_idx, lake_state)
        print_let(e, cur_scan_idx)
        scan_strs[cur_scan_idx] = scan_strs[cur_scan_idx] + arg0_str + " == " + arg1_str
    elif e_type == ScanConstOp:
        cur_scan_idx = cur_scan_idx + 1
        scan_strs[cur_scan_idx] = ""
        arg_var = var_f("scan_var_" + str(cur_scan_idx))
        scan_strs[cur_scan_idx] = scan_strs[cur_scan_idx] + recurrence_seq_str + str(
            e.index) + "(lambda " + arg_var.name
        scan_strs[cur_scan_idx] = scan_strs[cur_scan_idx] + "): \n"
        f_res = e.f(arg_var)
        print_frail(f_res, cur_scan_idx, False)
        scan_strs[cur_scan_idx] = scan_strs[cur_scan_idx] + "\n" + indent_str + "return x" + str(f_res.index)
        scan_strs[cur_scan_idx] = scan_strs[cur_scan_idx] + "\n)\n"
    else:
        assert False, str(e) + "is not a valid frail operator"

    if root:
        keys = reversed(sorted(scan_strs.keys()))
        for k in keys:
            print(scan_strs[k])


def print_arg(arg_index: int, cur_scan_idx: int, lake_state: LakeDSLState):
    if arg_index not in printed_ops:
        printed_ops.add(arg_index)
        print_frail(lake_state.program_map[arg_index], cur_scan_idx, False, lake_state)
        scan_strs[cur_scan_idx] = scan_strs[cur_scan_idx] + "\n"
    return "x" + str(arg_index)


def print_let(arg: int, cur_scan_idx: int):
    scan_strs[cur_scan_idx] = scan_strs[cur_scan_idx] + indent_str + "let x" + str(arg.index) + " = "
