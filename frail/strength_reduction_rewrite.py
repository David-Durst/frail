from frail.ast import *
from typing import Set, Dict, List


cur_scan_idx: int = -1
cur_scan_lambda_var: Var = None
output_scan_index: int = -1
printed_ops: Set[int] = set()
mul_list = {}


def get_index(index: int, lake_state: LakeDSLState):
    e, ls = strength_reduction_rewrite(lake_state.program_map[index], False, lake_state)
    if index in mul_list:
        counter_op = mul_list[index]
        return e.index
    return index


def strength_reduction_rewrite(e: AST,
                               root: bool = True,
                               lake_state: LakeDSLState = default_lake_state):
    global cur_scan_idx, output_scan_index, cur_scan_lambda_var
    global printed_ops, mul_list

    if root:
        cur_scan_idx = -1
        output_scan_index = -1
        printed_ops = set()
        mul_list = {}

    e_type = type(e)
    if e.index in printed_ops:
        return

    printed_ops.add(e.index)

    if e_type == RecurrenceSeq:
        old_scan_idx = cur_scan_idx
        old_scan_lambda_var = cur_scan_lambda_var
        e_after, ls = strength_reduction_rewrite(lake_state.program_map[e.producing_recurrence], False, lake_state)
        cur_scan_idx = old_scan_idx
        cur_scan_lambda_var = old_scan_lambda_var

    elif e_type == CounterSeq:
        old_scan_idx = cur_scan_idx
        old_scan_lambda_var = cur_scan_lambda_var
        e_after, ls = strength_reduction_rewrite(lake_state.program_map[e.producing_counter], False, lake_state)
        cur_scan_idx = old_scan_idx
        cur_scan_lambda_var = old_scan_lambda_var

    elif e_type in (AddOp, SubOp, ModOp, EqOp, LTOp, GTOp):
        e.arg0_index = get_index(e.arg0_index, lake_state)
        e.arg1_index = get_index(e.arg1_index, lake_state)
        lake_state.program_map[e.index] = e
    elif e_type == SelectBitsOp:
        e.arg0_index = get_index(e.arg0_index, lake_state)
    elif e_type == IfOp:
        e.arg0_index = get_index(e.arg0_index, lake_state)
        e.arg1_index = get_index(e.arg1_index, lake_state)
        e.b_index = get_index(e.b_index, lake_state)
    elif e_type == MulOp:
        replace_counter = None
        if isinstance(lake_state.program_map[e.arg0_index], CounterSeq):
            replace_counter = e.arg0_index
            replace_arg = 0
        elif isinstance(lake_state.program_map[e.arg1_index], CounterSeq):
            replace_counter = e.arg1_index
            replace_arg = 1
        # print("MUL 0", lake_state.program_map[e.arg0_index])
        # print("MUL 1", lake_state.program_map[e.arg1_index])
        if replace_counter is not None:
            og_counter_op = lake_state.program_map[lake_state.program_map[replace_counter].producing_counter]
            incr_amount_index = e.arg0_index if replace_arg == 1 else e.arg1_index
            incr_amount_op = lake_state.program_map[incr_amount_index]
            prev_level = None if og_counter_op.prev_level_input is None else lake_state.program_map[og_counter_op.prev_level_input]
            lake_state.program_map[e.index] = \
                counter_f(prev_level, og_counter_op.at_max(), incr_amount_op).val()
            prev_mul_index = e.index
            e = counter_f(prev_level, og_counter_op.at_max(), incr_amount_op).val()
            mul_list[prev_mul_index] = e.index
    elif e_type == CounterOp:
        if output_scan_index == -1:
            output_scan_index = e.index
        cur_scan_idx = e.index

        if e.prev_level_input is not None:
            strength_reduction_rewrite(lake_state.program_map[e.prev_level_input], False, lake_state)
        if e.is_max_wire:
            strength_reduction_rewrite(lake_state.program_map[e.max_val], False, lake_state)
        if isinstance(e.incr_amount, AST):
            strength_reduction_rewrite(e.incr_amount, False, lake_state)

    elif e_type == ScanConstOp:
        if output_scan_index == -1:
            output_scan_index = e.index
        cur_scan_idx = e.index
        cur_scan_lambda_var = var_f("scan_var_" + str(cur_scan_idx), e.width)
        f_res = e.f(cur_scan_lambda_var)
        e_ret, ls = strength_reduction_rewrite(f_res, False, lake_state)
        if isinstance(e_ret, CounterOp):
            e = e_ret
        else:
            e = scan_const_f(lambda z: e_ret)

    return e, lake_state
        