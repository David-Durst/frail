from frail.ast import *
from typing import Set, Dict
"""
def replace_counters(e: AST, lake_state: LakeDSLState = default_lake_state):
    for e_index in sorted(lake_state.program_map.keys()):
        # start with earliest to avoid dependency issues
        e = lake_state.program_map[e]
        e_type = type(e)
        if e_type == CounterOp:

            cur_scan_idx = e.index
            scan_strs[cur_scan_idx] = ""
            cur_scan_lambda_var = var_f("counter_var_" + str(cur_scan_idx))
            if e.prev_level_input is not None:
                prev_level_input_str = get_var_val(print_arg(e.prev_level_input, lake_state))
            else:
                prev_level_input_str = "None"
            if e.is_max_wire:
                max_val_str = get_var_val(print_arg(e.max_val, lake_state))
            else:
                max_val_str = str(e.max_val)
            scan_strs[cur_scan_idx] = scan_strs[cur_scan_idx] + recurrence_seq_str + str(e.index) + \
                                      "(counter(" + prev_level_input_str + "," + \
                                      max_val_str + "," + str(e.incr_amount) + "))\n"
"""
