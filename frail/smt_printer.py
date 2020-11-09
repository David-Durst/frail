from frail.ast import *
from frail.examples import *
from typing import Set, Dict

indent_str = "  "
recurrence_seq_str = "scan_const"
scan_strs: Dict[int, str] = {}
printed_ops: Set[int] = set()
cur_scan_idx: int = -1
cur_scan_lambda_var: Var = None
smt_prologue = """
from pysmt.shortcuts import Symbol, And, Equals, BVAdd, BVMul, Int, Bool, Ite, BV, BVURem, BVExtract
from pysmt.typing import BVType 
"""


def frail_to_smt(e: AST, root: bool = True, lake_state: LakeDSLState = default_lake_state, name: str = "NA"):
    global scan_strs, printed_ops, cur_scan_idx, cur_scan_lambda_var
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
        print_let(e)
        scan_strs[cur_scan_idx] = scan_strs[cur_scan_idx] + "Symbol(\"" + str(e.name) + "\", BVType(" + str(e.width) + "))\n"
        scan_strs[cur_scan_idx] = scan_strs[cur_scan_idx] + indent_str + name + "_free_vars.append(BV(x" + \
                                  str(e.index) + "))" + "\n"
    elif e_type == Int:
        print_let(e)
        scan_strs[cur_scan_idx] = scan_strs[cur_scan_idx] + "BV(" + str(e.val) + "," + str(e.width) + ")" + "\n"
    elif e_type == Bool:
        print_let(e)
        scan_strs[cur_scan_idx] = scan_strs[cur_scan_idx] + "Bool(" + str(e.val) + ")\n"
    elif e_type == RecurrenceSeq:
        print_let(e)
        scan_strs[cur_scan_idx] = scan_strs[cur_scan_idx] + recurrence_seq_str + str(e.producing_recurrence) + "\n"
        old_scan_idx = cur_scan_idx
        old_scan_lambda_var = cur_scan_lambda_var
        frail_to_smt(lake_state.program_map[e.producing_recurrence], False, lake_state, name)
        cur_scan_idx = old_scan_idx
        cur_scan_lambda_var = old_scan_lambda_var
    elif e_type == AddOp:
        arg0_str = print_arg(e.arg0_index, lake_state, name)
        arg1_str = print_arg(e.arg1_index, lake_state, name)
        print_let(e)
        scan_strs[cur_scan_idx] = scan_strs[cur_scan_idx] + "BVAdd(" + arg0_str + ", " + arg1_str + ")\n"
    elif e_type == MulOp:
        arg0_str = print_arg(e.arg0_index, lake_state, name)
        arg1_str = print_arg(e.arg1_index, lake_state, name)
        print_let(e)
        scan_strs[cur_scan_idx] = scan_strs[cur_scan_idx] + "BVMul(" + arg0_str + ", " + arg1_str + ")\n"
    elif e_type == ModOp:
        arg0_str = print_arg(e.arg0_index, lake_state, name)
        arg1_str = print_arg(e.arg1_index, lake_state, name)
        print_let(e)
        scan_strs[cur_scan_idx] = scan_strs[cur_scan_idx] + "BVURem(" + arg0_str + ", " + arg1_str + ")\n"
    elif e_type == SelectBitsOp:
        arg0_str = print_arg(e.arg0_index, lake_state, name)
        print_let(e)
        scan_strs[cur_scan_idx] = scan_strs[cur_scan_idx] + "BVExtact(" + arg0_str + ", 0, " + str(e.bits) + " - 1)\n"
    elif e_type == IfOp:
        b_str = print_arg(e.b_index, lake_state, name)
        arg0_str = print_arg(e.arg0_index, lake_state, name)
        arg1_str = print_arg(e.arg1_index, lake_state, name)
        print_let(e)
        scan_strs[cur_scan_idx] = scan_strs[cur_scan_idx] + "Ite(" + b_str + ", " + arg0_str + ", " + arg1_str + ")\n"
    elif e_type == EqOp:
        arg0_str = print_arg(e.arg0_index, lake_state, name)
        arg1_str = print_arg(e.arg1_index, lake_state, name)
        print_let(e)
        scan_strs[cur_scan_idx] = scan_strs[cur_scan_idx] + "Equals(" + arg0_str + ", " + arg1_str + ")\n"
    elif e_type == ScanConstOp:
        cur_scan_idx = e.index
        cur_scan_lambda_var = var_f("scan_var_" + str(cur_scan_idx))
        scan_func_name = recurrence_seq_str + str(e.index) + "_f"
        scan_strs[cur_scan_idx] = "def " + scan_func_name + "(" + cur_scan_lambda_var.name
        scan_strs[cur_scan_idx] = scan_strs[cur_scan_idx] + "): \n"
        f_res = e.f(cur_scan_lambda_var)
        frail_to_smt(f_res, False, lake_state, name)
        scan_strs[cur_scan_idx] = scan_strs[cur_scan_idx] + indent_str + "return x" + str(f_res.index)
        scan_strs[cur_scan_idx] = scan_strs[cur_scan_idx] + "\n)\n"
        scan_strs[cur_scan_idx] = scan_strs[cur_scan_idx] + name + "_scans.append(" + scan_func_name + ")\n"
        scan_strs[cur_scan_idx] = scan_strs[cur_scan_idx] + name + "_scan_vars.append(Symbol(\"" + \
                                  cur_scan_lambda_var.name + "\", " + str(e.width) + "))\n"
    else:
        assert False, str(e) + "is not a valid frail operator"

    if root:
        print(smt_prologue)
        print(name + "_free_vars = []")
        print(name + "_scans = []")
        print(name + "_scan_vars = []")
        keys = sorted(scan_strs.keys())
        for k in keys:
            print(scan_strs[k])


def print_arg(arg_index: int, lake_state: LakeDSLState, name: str):
    frail_to_smt(lake_state.program_map[arg_index], False, lake_state, name)
    if arg_index == cur_scan_lambda_var.index:
        return cur_scan_lambda_var.name
    else:
        return "x" + str(arg_index)


def print_let(arg: AST):
    scan_strs[cur_scan_idx] = scan_strs[cur_scan_idx] + indent_str + "x" + str(arg.index) + " = "

def print_ex_smt():
    frail_to_smt(design_b, name="design_b")
    frail_to_smt(design_a, name="design_a")
