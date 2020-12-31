from frail.ast import *
from typing import Set, Dict

indent_str = "  "
recurrence_seq_str = "scan_const"
scan_strs: Dict[int, str] = {}
printed_ops: Set[int] = set()
cur_scan_idx: int = -1
cur_scan_lambda_var: Var = None
VarTable: Dict[str, str] = {}


def get_var_val(key):
    if key in VarTable.keys():
        return VarTable[key]
    return key


def print_frail(e: AST, root: bool = True, lake_state: LakeDSLState = default_lake_state):
    global scan_strs, printed_ops, cur_scan_idx, cur_scan_lambda_var, VarTable
    if root:
        scan_strs = {}
        printed_ops = set()
        cur_scan_idx = -1

    if e.index in printed_ops:
        return

    printed_ops.add(e.index)
    e_type = type(e)
    # start with empty string if printing expression not in a scan
    if not scan_strs:
        scan_strs[-1] = ""

    if e_type == Var:
        # don't redefine the scan's lambda variable
        if e == cur_scan_lambda_var:
            return
        VarTable[f"x{e.index}"] = "Var(" + str(e.name) + ")"
    elif e_type == Int:
        VarTable[f"x{e.index}"] = str(e.val)
    elif e_type == Bool:
        VarTable[f"x{e.index}"] = str(e.val)
    elif e_type == RecurrenceSeq:
        VarTable[f"x{e.index}"] = recurrence_seq_str + str(e.producing_recurrence) + "[i]"
        old_scan_idx = cur_scan_idx
        old_scan_lambda_var = cur_scan_lambda_var
        print_frail(lake_state.program_map[e.producing_recurrence], False, lake_state)
        cur_scan_idx = old_scan_idx
        cur_scan_lambda_var = old_scan_lambda_var
    elif e_type == AddOp:
        arg0_str = get_var_val(print_arg(e.arg0_index, lake_state))
        arg1_str = get_var_val(print_arg(e.arg1_index, lake_state))
        print_let(e)
        scan_strs[cur_scan_idx] = scan_strs[cur_scan_idx] + arg0_str + " + " + arg1_str + "\n"
    elif e_type == SubOp:
        arg0_str = get_var_val(print_arg(e.arg0_index, lake_state))
        arg1_str = get_var_val(print_arg(e.arg1_index, lake_state))
        print_let(e)
        scan_strs[cur_scan_idx] = scan_strs[cur_scan_idx] + arg0_str + " - " + arg1_str + "\n"
    elif e_type == MulOp:
        arg0_str = get_var_val(print_arg(e.arg0_index, lake_state))
        arg1_str = get_var_val(print_arg(e.arg1_index, lake_state))
        print_let(e)
        scan_strs[cur_scan_idx] = scan_strs[cur_scan_idx] + arg0_str + " * " + arg1_str + "\n"
    elif e_type == ModOp:
        arg0_str = get_var_val(print_arg(e.arg0_index, lake_state))
        arg1_str = get_var_val(print_arg(e.arg1_index, lake_state))
        print_let(e)
        scan_strs[cur_scan_idx] = scan_strs[cur_scan_idx] + arg0_str + " % " + arg1_str + "\n"
    elif e_type == SelectBitsOp:
        arg0_str = get_var_val(print_arg(e.arg0_index, lake_state))
        print_let(e)
        scan_strs[cur_scan_idx] = scan_strs[cur_scan_idx] + "select_bits(" + arg0_str + ", " + str(e.bits) + ")\n"
    elif e_type == IfOp:
        b_str = get_var_val(print_arg(e.b_index, lake_state))
        arg0_str = get_var_val(print_arg(e.arg0_index, lake_state))
        arg1_str = get_var_val(print_arg(e.arg1_index, lake_state))
        print_let(e)
        scan_strs[cur_scan_idx] = scan_strs[cur_scan_idx] + "if(" + b_str + ", " + arg0_str + ", " + arg1_str + ")\n"
    elif e_type == EqOp:
        arg0_str = get_var_val(print_arg(e.arg0_index, lake_state))
        arg1_str = get_var_val(print_arg(e.arg1_index, lake_state))
        print_let(e)
        scan_strs[cur_scan_idx] = scan_strs[cur_scan_idx] + arg0_str + " == " + arg1_str + "\n"
    elif e_type == ScanConstOp:
        cur_scan_idx = e.index
        scan_strs[cur_scan_idx] = ""
        cur_scan_lambda_var = var_f("scan_var_" + str(cur_scan_idx))
        scan_strs[cur_scan_idx] = scan_strs[cur_scan_idx] + recurrence_seq_str + str(
            e.index) + "(lambda " + cur_scan_lambda_var.name
        scan_strs[cur_scan_idx] = scan_strs[cur_scan_idx] + ": \n"
        f_res = e.f(cur_scan_lambda_var)
        print_frail(f_res, False, lake_state)
        scan_strs[cur_scan_idx] = scan_strs[cur_scan_idx] + indent_str + "return x" + str(f_res.index)
        scan_strs[cur_scan_idx] = scan_strs[cur_scan_idx] + "\n, " + str(e.width) +")\n"
    else:
        assert False, str(e) + "is not a valid frail operator"

    if root:
        keys = sorted(scan_strs.keys())
        for k in keys:
            print(scan_strs[k])


def print_arg(arg_index: int, lake_state: LakeDSLState):
    print_frail(lake_state.program_map[arg_index], False, lake_state)
    if arg_index == cur_scan_lambda_var.index:
        return cur_scan_lambda_var.name
    else:
        return "x" + str(arg_index)


def print_let(arg: AST):
    scan_strs[cur_scan_idx] = scan_strs[cur_scan_idx] + indent_str + "let x" + str(arg.index) + " = "
