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
        break
    print_verilog(e=e,
                  lake_state=lake_state,
                  top_name="nested")
    return e


def get_index(index: int, lake_state: LakeDSLState):
    sharing_nested_counters_rewrite(lake_state.program_map[index],
                                    False,
                                    lake_state)
    index_ast = lake_state.program_map[index]
    if index in replace:
        return replace[index].index
    return index


def get_merged_counter(lake_state):
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
        new_config_name = f"config_{merge[0]}_{merge[1]}_op"
        if isinstance(pvc.incr_amount, Var):
            new_config_name = f"{pvc.incr_amount.name}_op"
        max_val = lake_state.program_map[lake_state.program_map[pvc.max_val].producing_counter].at_max()
        merged_counter = counter_f(mvc.prev_level_input,
                                   max_val,
                                   if_f(lake_state.program_map[pvc.prev_level_input],
                                        var_f(new_config_name),
                                        mvc.incr_amount))
        return merged_counter
    return None


def add_potential_counter(e, lake_state, index, prev):
    curr = prev_vals if prev else max_vals
    other = max_vals if prev else prev_vals
    if isinstance(lake_state.program_map[index], CounterSeq):
        prod_counter = lake_state.program_map[index].producing_counter
        can_merge = True
        for m in other:
            if e.index in other[m]:
                can_merge = False
        if can_merge:
            if prod_counter in curr:
                curr[prod_counter].append(e.index)
            else:
                curr[prod_counter] = [e.index]
    sharing_nested_counters_rewrite(
        lake_state.program_map[index], False, lake_state)


def sharing_nested_counters_rewrite(
        e: AST,
        root: bool = True,
        lake_state: LakeDSLState = default_lake_state):
    global cur_scan_idx, output_scan_index, cur_scan_lambda_var
    global printed_ops, have_merged_counters, prev_vals, max_vals
    global replace

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
        counter_op = lake_state.program_map[e.producing_counter]
        old_scan_idx = cur_scan_idx
        old_scan_lambda_var = cur_scan_lambda_var
        sharing_nested_counters_rewrite(counter_op, False, lake_state)
        cur_scan_idx = old_scan_idx
        cur_scan_lambda_var = old_scan_lambda_var

    elif e_type == CounterOp:
        if output_scan_index == -1:
            output_scan_index = e.index
        cur_scan_idx = e.index

        if e.prev_level_input is not None:
            add_potential_counter(e, lake_state, e.prev_level_input, True)

        if e.is_max_wire:
            add_potential_counter(e, lake_state, e.max_val, False)

        if isinstance(e.incr_amount, AST):
            sharing_nested_counters_rewrite(e.incr_amount, False, lake_state)

    elif e_type == ScanConstOp:
        if output_scan_index == -1:
            output_scan_index = e.index
        cur_scan_idx = e.index
        cur_scan_lambda_var = var_f("scan_var_" + str(cur_scan_idx), e.width)
        f_res = e.f(cur_scan_lambda_var)
        e_ret = sharing_nested_counters_rewrite(f_res, False, lake_state)
        e = scan_const_f(lambda z: e_ret)

    elif e_type == AddOp:
        e.arg0_index = get_index(e.arg0_index, lake_state)
        e.arg1_index = get_index(e.arg1_index, lake_state)
        lake_state.program_map[e.index] = e
        merged = get_merged_counter(lake_state)
        if merged is not None:
            merged = merged.val()
            lake_state.program_map[e.index] = merged
            replace[e.index] = merged

    elif e_type in (SubOp, ModOp, EqOp, LTOp, GTOp, MulOp):
        e.arg0_index = get_index(e.arg0_index, lake_state)
        e.arg1_index = get_index(e.arg1_index, lake_state)
        lake_state.program_map[e.index] = e

    elif e_type == SelectBitsOp:
        e.arg0_index = get_index(e.arg0_index, lake_state)
        lake_state.program_map[e.index] = e

    elif e_type == IfOp:
        e.arg0_index = get_index(e.arg0_index, lake_state)
        e.arg1_index = get_index(e.arg1_index, lake_state)
        e.b_index = get_index(e.b_index, lake_state)
        lake_state.program_map[e.index] = e

    return e
