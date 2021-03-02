from frail.ast import *
from typing import Set, Dict, List
from frail.verilog_printer import *


cur_scan_idx: int = -1
cur_scan_lambda_var: Var = None
output_scan_index: int = -1
printed_ops: Set[int] = set()
have_merged_counters: bool = False
prev_vals = {}
max_vals = {}

def nested_counters_rewrite(e: AST,
                            root: bool = True,
                            lake_state: LakeDSLState = default_lake_state):
    need_merged_counters = True
    sharing_nested_counters_rewrite(e, root, lake_state)
    print(prev_vals)
    print(max_vals)
    """ while need_merged_counters:
      e, lake_state, need_merged_counters = \
        sharing_nested_counters_rewrite(e, root, lake_state) """
      
    """ print_verilog(e=e,
                  lake_state=lake_state, 
                  top_name="nested_counters_rewrite") """

def get_arg(index: int, lake_state: LakeDSLState):
    sharing_nested_counters_rewrite(lake_state.program_map[index],
                                    False,
                                    lake_state)

def sharing_nested_counters_rewrite(e: AST,
                                    root: bool = True,
                                    lake_state: LakeDSLState = default_lake_state):
    global cur_scan_idx, output_scan_index, cur_scan_lambda_var
    global printed_ops, have_merged_counters, prev_vals, max_vals

    print(prev_vals)
    print(max_vals)
    print()
    if root:
        cur_scan_idx = -1
        output_scan_index = -1
        printed_ops = set()
        have_merged_counters = False
        prev_vals = {}
        max_vals = {}

    e_type = type(e)
    if e.index in printed_ops:
        return

    printed_ops.add(e.index)

    if e_type == RecurrenceSeq:
        old_scan_idx = cur_scan_idx
        old_scan_lambda_var = cur_scan_lambda_var
        sharing_nested_counters_rewrite(
            lake_state.program_map[e.producing_recurrence], False, lake_state)
        cur_scan_idx = old_scan_idx
        cur_scan_lambda_var = old_scan_lambda_var

    elif e_type == CounterSeq:
        print("COUNTER SEQ ", e)
        counter_op = lake_state.program_map[e.producing_counter]
        print("MAX ", lake_state.program_map[counter_op.max_val])
        old_scan_idx = cur_scan_idx
        old_scan_lambda_var = cur_scan_lambda_var
        sharing_nested_counters_rewrite(lake_state.program_map[e.producing_counter],
                                   False,
                                   lake_state)
        cur_scan_idx = old_scan_idx
        cur_scan_lambda_var = old_scan_lambda_var

    elif e_type == CounterOp:
        print("COUNTER OP ", e)
        if output_scan_index == -1:
            output_scan_index = e.index
        cur_scan_idx = e.index

        if e.prev_level_input is not None:
            if type(lake_state.program_map[e.prev_level_input]) == CounterSeq:
                prev_prod_counter = lake_state.program_map[e.prev_level_input].producing_counter
                if prev_prod_counter in prev_vals:
                    prev_vals[prev_prod_counter].append(e.index)
                else:
                    prev_vals[prev_prod_counter] = [e.index]
            sharing_nested_counters_rewrite(
                lake_state.program_map[e.prev_level_input], False, lake_state)
        if e.is_max_wire:
            if type(lake_state.program_map[e.max_val]) == CounterSeq:
                max_prod_counter = lake_state.program_map[e.max_val].producing_counter
                if max_prod_counter in max_vals:
                    max_vals[max_prod_counter].append(e.index)
                else:
                    max_vals[max_prod_counter] = [e.index]
            sharing_nested_counters_rewrite(lake_state.program_map[e.max_val],
                                       False,
                                       lake_state)
        if isinstance(e.incr_amount, AST):
            sharing_nested_counters_rewrite(e.incr_amount,
                                       False,
                                       lake_state)

    elif e_type == ScanConstOp:
        if output_scan_index == -1:
            output_scan_index = e.index
        cur_scan_idx = e.index
        cur_scan_lambda_var = var_f("scan_var_" + str(cur_scan_idx), e.width)
        f_res = e.f(cur_scan_lambda_var)
        e_ret, ls, have_merged_counters = sharing_nested_counters_rewrite(f_res, False, lake_state)
        if isinstance(e_ret, CounterOp):
            e = e_ret
        else:
            e = scan_const_f(lambda z: e_ret)

    elif e_type in (AddOp, SubOp, ModOp, EqOp, LTOp, GTOp, MulOp):
        get_arg(e.arg0_index, lake_state)
        get_arg(e.arg1_index, lake_state)
    elif e_type == SelectBitsOp:
        e.arg0_index = get_index(e.arg0_index, lake_state)
    elif e_type == IfOp:
        get_arg(e.arg0_index, lake_state)
        get_arg(e.arg1_index, lake_state)
        get_arg(e.b_index, lake_state)

    return e, lake_state, True
