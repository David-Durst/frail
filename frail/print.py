from frail.ast import *

indent_str = "  "
recurrence_seq_str = "recur"
def print_frail(e: AST, indentation: int = 1, scan_strs: dict[int, str] = [], cur_scan_idx: int = -1, root: bool = True):
    e_type = type(e)
    # start with empty string if printing expression not in a scan
    if not scan_strs:
        dict[-1] = ""

    if e_type == Var:
        dict[cur_scan_idx] = dict[cur_scan_idx] + str(e.val)
    elif e_type == Int:
        dict[cur_scan_idx] = dict[cur_scan_idx] + str(e.val)
    elif e_type == Bool:
        dict[cur_scan_idx] = dict[cur_scan_idx] + str(e.val)
    elif e_type == RecurrenceSeq:
        dict[cur_scan_idx] = dict[cur_scan_idx] + recurrence_seq_str + str(e.producing_recurrence)
    elif e_type == AddOp:
        print_frail(e.arg0, indentation, scan_strs, cur_scan_idx, False)
        dict[cur_scan_idx] = dict[cur_scan_idx] + " + "
        print_frail(e.arg1, indentation, scan_strs, cur_scan_idx, False)
    elif e_type == MulOp:
        print_frail(e.arg0, indentation, scan_strs, cur_scan_idx, False)
        dict[cur_scan_idx] = dict[cur_scan_idx] + " * "
        print_frail(e.arg1, indentation, scan_strs, cur_scan_idx, False)
    elif e_type == ModOp:
        print_frail(e.arg0, indentation, scan_strs, cur_scan_idx, False)
        dict[cur_scan_idx] = dict[cur_scan_idx] + " % "
        print_frail(e.arg1, indentation, scan_strs, cur_scan_idx, False)
    elif e_type == SelectBitsOp:
        dict[cur_scan_idx] = dict[cur_scan_idx] + "select_bits("
        print_frail(e.arg0, indentation, scan_strs, cur_scan_idx, False)
        dict[cur_scan_idx] = dict[cur_scan_idx] + ", "
        print_frail(e.arg1, indentation, scan_strs, cur_scan_idx, False)
        dict[cur_scan_idx] = dict[cur_scan_idx] + ")"
    elif e_type == IfOp:
        dict[cur_scan_idx] = dict[cur_scan_idx] + "if("
        print_frail(e.b, indentation, scan_strs, cur_scan_idx, False)
        dict[cur_scan_idx] = dict[cur_scan_idx] + ")\n" + (indent_str * indentation)
        print_frail(e.arg0, indentation + 1, scan_strs, cur_scan_idx, False)
        dict[cur_scan_idx] = dict[cur_scan_idx] + "\n" + (indent_str * (indentation - 1)) + "else\n" + \
                             (indent_str * indentation)
        print_frail(e.arg1, indentation + 1, scan_strs, cur_scan_idx, False)
        dict[cur_scan_idx] = dict[cur_scan_idx] + "\n" + (indent_str * (indentation-1))
    elif e_type == EqOp:
        print_frail(e.arg0, indentation, scan_strs, cur_scan_idx, False)
        dict[cur_scan_idx] = dict[cur_scan_idx] + " == "
        print_frail(e.arg1, indentation, scan_strs, cur_scan_idx, False)
    elif e_type == ScanConstOp:
        cur_scan_idx = cur_scan_idx + 1
        arg_var = varL("scan_var_" + str(cur_scan_idx))
        dict[cur_scan_idx] = dict[cur_scan_idx] + "scan_const(lambda "
        print_frail(arg_var, indentation, scan_strs, cur_scan_idx, False)
        dict[cur_scan_idx] = dict[cur_scan_idx] + ": "
        print_frail(e.f(arg_var), indentation, scan_strs, cur_scan_idx, False)
        dict[cur_scan_idx] = dict[cur_scan_idx] + ")"
    else:
        assert False, str(e) + "is not a valid frail operator"


    if root:
        keys = sorted(scan_strs.keys())
        for k in keys:
            print(scan_strs[k])
