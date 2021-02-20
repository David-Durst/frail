from frail.ast import *
from typing import Set, Dict, List


cur_scan_idx: int = -1
cur_scan_lambda_var: Var = None
output_scan_index: int = -1
printed_ops: Set[int] = set()
mul_list = {}

def strength_reduction_rewrite(e: AST,
                               root: bool = True,
                               lake_state: LakeDSLState = default_lake_state,
                               top_name: str = "top",
                               add_step: bool = True,
                               get_verilog: bool = True):
    global cur_scan_idx, output_scan_index, cur_scan_lambda_var
    global printed_ops, mul_list

    if root:
        cur_scan_idx = -1
        output_scan_index = -1
        printed_ops = set()
        mul_list = {}

    e_type = type(e)
    # print("INFO", cur_scan_idx, e_type)

    if e.index in printed_ops:
        return

    printed_ops.add(e.index)

    replace_counter = None
    if e_type == RecurrenceSeq:
        old_scan_idx = cur_scan_idx
        old_scan_lambda_var = cur_scan_lambda_var
        e_after = strength_reduction_rewrite(lake_state.program_map[e.producing_recurrence], False, lake_state)
        cur_scan_idx = old_scan_idx
        cur_scan_lambda_var = old_scan_lambda_var
    elif e_type == CounterSeq:
        old_scan_idx = cur_scan_idx
        old_scan_lambda_var = cur_scan_lambda_var
        e_after = strength_reduction_rewrite(lake_state.program_map[e.producing_counter], False, lake_state)
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
            lake_state.program_map[e.index] = \
                counter_f(og_counter_op.prev_level_input, og_counter_op.at_max(), incr_amount_op)
            prev_mul_index = e.index
            e = counter_f(og_counter_op.prev_level_input, og_counter_op.at_max(), incr_amount_op)
            # need to search for where this is used and replace it
            mul_list[prev_mul_index] = e.index #e.val()
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
        