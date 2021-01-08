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
from pysmt.shortcuts import Symbol, And, Equals, BVAdd, BVMul, Bool, Ite, BV, BVURem, BVExtract, ForAll, Exists, Portfolio, Solver
from pysmt.typing import BVType 
from pysmt.logics import BV as logicBV
from frail import IteExtend, BVAddExtend, BVSubExtend, BVMulExtend, BVEqualsExtend
import time
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
        scan_strs[cur_scan_idx] = scan_strs[cur_scan_idx] + indent_str + "if " + str(e.index) + " not in " + \
                                  name + "_free_vars:\n"
        scan_strs[cur_scan_idx] = scan_strs[cur_scan_idx] + indent_str + indent_str + name + "_free_vars[" + \
                                  str(e.index) + "] = Symbol(\"" + str(e.name) + "_" + name + "\", BVType(" + str(e.width) + "))\n"
        print_let(e)
        scan_strs[cur_scan_idx] = scan_strs[cur_scan_idx] +  name + "_free_vars[" + str(e.index) + \
                                  "]" + "\n"
    elif e_type == Int:
        print_let(e)
        scan_strs[cur_scan_idx] = scan_strs[cur_scan_idx] + "BV(" + str(e.val) + "," + str(e.width) + ")" + "\n"
    elif e_type == Bool:
        print_let(e)
        scan_strs[cur_scan_idx] = scan_strs[cur_scan_idx] + "Bool(" + str(e.val) + ")\n"
    elif e_type == RecurrenceSeq:
        print_let(e)
        scan_strs[cur_scan_idx] = scan_strs[cur_scan_idx] + recurrence_seq_str + str(e.producing_recurrence) + "\n"
        old_printed_ops = printed_ops
        printed_ops = set()
        old_scan_idx = cur_scan_idx
        old_scan_lambda_var = cur_scan_lambda_var
        frail_to_smt(lake_state.program_map[e.producing_recurrence], False, lake_state, name)
        cur_scan_idx = old_scan_idx
        cur_scan_lambda_var = old_scan_lambda_var
        printed_ops = old_printed_ops
    elif e_type == AddOp:
        arg0_str = print_arg(e.arg0_index, lake_state, name)
        arg1_str = print_arg(e.arg1_index, lake_state, name)
        print_let(e)
        scan_strs[cur_scan_idx] = scan_strs[cur_scan_idx] + "BVAddExtend(" + arg0_str + ", " + arg1_str + ")\n"
    elif e_type == SubOp:
        arg0_str = print_arg(e.arg0_index, lake_state, name)
        arg1_str = print_arg(e.arg1_index, lake_state, name)
        print_let(e)
        scan_strs[cur_scan_idx] = scan_strs[cur_scan_idx] + "BVSubExtend(" + arg0_str + ", " + arg1_str + ")\n"
    elif e_type == MulOp:
        arg0_str = print_arg(e.arg0_index, lake_state, name)
        arg1_str = print_arg(e.arg1_index, lake_state, name)
        print_let(e)
        scan_strs[cur_scan_idx] = scan_strs[cur_scan_idx] + "BVMulExtend(" + arg0_str + ", " + arg1_str + ")\n"
    elif e_type == ModOp:
        arg0_str = print_arg(e.arg0_index, lake_state, name)
        arg1_str = print_arg(e.arg1_index, lake_state, name)
        print_let(e)
        scan_strs[cur_scan_idx] = scan_strs[cur_scan_idx] + "BVURem(" + arg0_str + ", " + arg1_str + ")\n"
    elif e_type == SelectBitsOp:
        arg0_str = print_arg(e.arg0_index, lake_state, name)
        print_let(e)
        scan_strs[cur_scan_idx] = scan_strs[cur_scan_idx] + "BVExtract(" + arg0_str + ", 0, " + str(e.bits) + " - 1)\n"
    elif e_type == IfOp:
        b_str = print_arg(e.b_index, lake_state, name)
        arg0_str = print_arg(e.arg0_index, lake_state, name)
        arg1_str = print_arg(e.arg1_index, lake_state, name)
        print_let(e)
        scan_strs[cur_scan_idx] = scan_strs[cur_scan_idx] + "IteExtend(" + b_str + ", " + arg0_str + ", " + arg1_str + ")\n"
    elif e_type == EqOp:
        arg0_str = print_arg(e.arg0_index, lake_state, name)
        arg1_str = print_arg(e.arg1_index, lake_state, name)
        print_let(e)
        scan_strs[cur_scan_idx] = scan_strs[cur_scan_idx] + "BVEqualsExtend(" + arg0_str + ", " + arg1_str + ")\n"
    elif e_type == ScanConstOp:
        cur_scan_idx = e.index
        cur_scan_lambda_var = var_f("scan_var_" + str(cur_scan_idx))
        scan_func_name = recurrence_seq_str + str(e.index) + "_f"
        scan_strs[cur_scan_idx] = "def " + scan_func_name + "(" + cur_scan_lambda_var.name
        scan_strs[cur_scan_idx] = scan_strs[cur_scan_idx] + "): \n"
        f_res = e.f(cur_scan_lambda_var)
        frail_to_smt(f_res, False, lake_state, name)
        scan_strs[cur_scan_idx] = scan_strs[cur_scan_idx] + indent_str + "return x" + str(f_res.index)
        scan_strs[cur_scan_idx] = scan_strs[cur_scan_idx] + "\n"
        scan_strs[cur_scan_idx] = scan_strs[cur_scan_idx] + name + "_scans.append(" + scan_func_name + ")\n"
        scan_strs[cur_scan_idx] = scan_strs[cur_scan_idx] + name + "_scans_results.append(\"" + recurrence_seq_str + \
                                  str(e.index) + "\")\n"
        scan_strs[cur_scan_idx] = scan_strs[cur_scan_idx] + recurrence_seq_str + str(e.index) + " = BV(0, " + \
                                  str(e.width) + ")\n"
    else:
        assert False, str(e) + "is not a valid frail operator"

    if root:
        print(smt_prologue)
        print(name + "_free_vars = {}")
        print(name + "_scans = []")
        print(name + "_scans_results = []")
        #print(name + "_scan_vars = []")
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

def check_circuit(e_a: AST, name_a: str, e_b: AST, name_b: str, num_iterations: int,
                  lake_state: LakeDSLState = default_lake_state):
    frail_to_smt(e_a, True, lake_state, name_a)
    frail_to_smt(e_b, True, lake_state, name_b)
    free_vars_name_a = name_a + "_free_vars"
    scans_a = name_a + "_scans"
    scans_results_a = name_a + "_scans_results"
    free_vars_name_b = name_b + "_free_vars"
    scans_b = name_b + "_scans"
    scans_results_b = name_b + "_scans_results"
    print(f"""
with Solver("cvc4",
       logic=logicBV,
       incremental=True) as s:
    per_step_constraints = []
    for step in range({num_iterations}):
        print("handling step " + str(step))
        for i in range(len({scans_a})):
            globals()[{scans_results_a}[i]] = {scans_a}[i](globals()[{scans_results_a}[i]])
        for i in range(len({scans_b})):
            globals()[{scans_results_b}[i]] = {scans_b}[i](globals()[{scans_results_b}[i]])
        per_step_constraints.append(Equals(globals()[{scans_results_a}[len({scans_results_a})-1]], globals()[{scans_results_b}[len({scans_results_b})-1]]))
    final_constraint = per_step_constraints[0]
    for c in per_step_constraints[1:]:
        final_constraint = And(final_constraint, c) 
    s.add_assertion(ForAll({free_vars_name_a}.values(), Exists({free_vars_name_b}.values(), final_constraint)))
    start = time.time()
    res = s.solve()
    assert res
    end = time.time()
    print("time: " + str(end - start))
    """)


def print_ex_smt():
    check_circuit(design_a, "design_a", design_b, "design_b", 1000)

def print_ex_opog():
    check_circuit(op_design, "op_design", og_design, "og_design", 2)

def print_frail_smt():
    frail_to_smt(design_b, name="design_b")
    frail_to_smt(design_a, name="design_a")
