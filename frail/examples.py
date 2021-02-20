from frail.ast import *
from frail.debug_printer import *
from frail.verilog_printer import *
from frail.strength_reduction_rewrite import *

x_max = var_f("x_max")
y_max = var_f("y_max")
x_stride = var_f("x_stride")
y_stride = var_f("y_stride")
offset = var_f("offset")

def create_affine_counter_design():
    level1 = counter_f(None, x_max, int_f(1))
    level2 = counter_f(level1.at_max(), y_max, int_f(1))
    add_design = scan_const_f(lambda z: add_f(offset, add_f(mul_f(level1.val(), x_stride), mul_f(level2.val(), y_stride))))
    return add_design #scan_const_f(lambda z: mul_f(level2.val(), y_stride)) #add_design

counter_design = create_affine_counter_design()
# rewrite, rewrite_lake_state = strength_reduction_rewrite(counter_design)
rewrite = strength_reduction_rewrite(counter_design)
#print_verilog(e=rewrite, lake_state=rewrite_lake_state)
print_verilog(e=rewrite, top_name="rewrite")
# print_verilog(counter_design)