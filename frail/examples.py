from frail.ast import *
from frail.debug_printer import *
from frail.verilog_printer import *
from frail.strength_reduction_rewrite import *
from frail.sharing_nested_counters_rewrite import *


x_max = var_f("x_max")
y_max = var_f("y_max")
z_max = var_f("z_max")
x_stride = var_f("x_stride")
y_stride = var_f("y_stride")
z_stride = var_f("z_stride")
offset = var_f("offset")

# AFFINE counter 2 loop levels
def create_affine_counter_design():
    level1 = counter_f(None, x_max, int_f(1))
    level2 = counter_f(level1.at_max(), y_max, int_f(1))
    add_design = scan_const_f(lambda z: add_f(offset, add_f(mul_f(level1.val(), x_stride), mul_f(level2.val(), y_stride))))
    return add_design
    """ level1 = counter_f(None, x_max, int_f(1))
    level2 = counter_f(level1.at_max(), y_max, int_f(1))
    level3 = counter_f(level2.at_max(), z_max, int_f(1))
    add_design = scan_const_f(lambda z: add_f(offset, add_f(mul_f(level1.val(), x_stride), add_f(mul_f(level2.val(), y_stride), mul_f(level3.val(), z_stride)))))
    return add_design """

counter_design = create_affine_counter_design()
# print_verilog(counter_design)

# with strength reduction rewrite rule
rewrite, ls = strength_reduction_rewrite(counter_design)
# print_verilog(e=rewrite, lake_state=ls, top_name="rewrite")
nested_counters_rewrite(rewrite, True, ls)
