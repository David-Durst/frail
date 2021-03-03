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
replace = {}

def nested_counters_rewrite(e: AST,
                            root: bool = True,
                            lake_state: LakeDSLState = default_lake_state):
    need_merged_counters = True
    while (need_merged_counters):
        e = sharing_nested_counters_rewrite(e, root, lake_state)
        
        # merged_counter = get_merged_counter(lake_state)
        # print_verilog(merged_counter, top_name="nested")
        break
    print_verilog(e=e,
                  lake_state=lake_state, 
                  top_name="nested")
    return e
    """ while need_merged_counters:
      e, lake_state, need_merged_counters = \
        sharing_nested_counters_rewrite(e, root, lake_state) """
      
    """ print_verilog(e=e,
                  lake_state=lake_state, 
                  top_name="nested_counters_rewrite") """

def get_merged_counter(lake_state):
    print(prev_vals)
    print(max_vals)
    merge = None
    for m in max_vals:
        if m in prev_vals and len(prev_vals[m]) > 0 and len(max_vals[m]) > 0:
            merge = [max_vals[m][0], prev_vals[m][0]]
            max_vals[m].remove(max_vals[m][0])
            prev_vals[m].remove(prev_vals[m][0])
            break
    if merge is not None:
        mvc = lake_state.program_map[merge[0]]
        pvc = lake_state.program_map[merge[1]]
        merged_counter = counter_f(mvc.prev_level_input, pvc.max_val, if_f(lake_state.program_map[pvc.prev_level_input], var_f(f"config_{merge[0]}_{merge[1]}_op"), mvc.incr_amount))
        print("MERGE", merged_counter)
        return merged_counter
    return None

def get_index(index: int, lake_state: LakeDSLState):
    sharing_nested_counters_rewrite(lake_state.program_map[index],
                                    False,
                                    lake_state)
    if index in replace:
        return replace[index].index
    return index

def sharing_nested_counters_rewrite(e: AST,
                                    root: bool = True,
                                    lake_state: LakeDSLState = default_lake_state):
    global cur_scan_idx, output_scan_index, cur_scan_lambda_var
    global printed_ops, have_merged_counters, prev_vals, max_vals
    global replace

    """ print(prev_vals)
    print(max_vals)
    print() """
    if root:
        cur_scan_idx = -1
        output_scan_index = -1
        printed_ops = set()
        have_merged_counters = False
        prev_vals = {}
        max_vals = {}
        replace = {}

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
                can_merge = True
                for m in max_vals:
                    if e.index in max_vals[m]:
                        can_merge = False
                if can_merge:
                    if prev_prod_counter in prev_vals:
                        prev_vals[prev_prod_counter].append(e.index)
                    else:
                        prev_vals[prev_prod_counter] = [e.index]
                """ if prev_prod_counter in max_vals:
                    return True """
            sharing_nested_counters_rewrite(
                lake_state.program_map[e.prev_level_input], False, lake_state)
        if e.is_max_wire:
            if type(lake_state.program_map[e.max_val]) == CounterSeq:
                max_prod_counter = lake_state.program_map[e.max_val].producing_counter
                can_merge = True
                for p in prev_vals:
                    if e.index in prev_vals[p]:
                        can_merge = False
                if can_merge:
                    if max_prod_counter in max_vals:
                        max_vals[max_prod_counter].append(e.index)
                    else:
                        max_vals[max_prod_counter] = [e.index]
                """ if max_prod_counter in max_vals:
                    return True """
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
        sharing_nested_counters_rewrite(f_res, False, lake_state)

    elif e_type in (AddOp, SubOp, ModOp, EqOp, LTOp, GTOp, MulOp):
        if e_type == AddOp:
            print("INDICES", e.arg0_index, e.arg1_index)
            print(lake_state.program_map[e.arg0_index], lake_state.program_map[e.arg1_index])
        e.arg0_index = get_index(e.arg0_index, lake_state)
        e.arg1_index = get_index(e.arg1_index, lake_state)
        lake_state.program_map[e.index] = e
        merged = get_merged_counter(lake_state)
        if merged is not None:
            lake_state.program_map[e.index] = merged
            replace[e.index] = merged
        print("DONE ADD")
    elif e_type == SelectBitsOp:
        e.arg0_index = get_index(e.arg0_index, lake_state)
        lake_state.program_map[e.index] = e
    elif e_type == IfOp:
        e.arg0_index = get_index(e.arg0_index, lake_state)
        e.arg1_index = get_index(e.arg1_index, lake_state)
        e.b_index = get_index(e.b_index, lake_state)
        lake_state.program_map[e.index] = e

    return e
