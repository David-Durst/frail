from frail.ast import *
from frail.debug_printer import *
from frail.verilog_printer import *


# configuration registers
x_max = var_f("x_max")
y_max = var_f("y_max")
x_stride = var_f("x_stride")
y_stride = var_f("y_stride")
offset = var_f("offset")

# original addressor design
def create_og_design():
    x_unit_counter = scan_const_f(lambda z: if_f(eq_f(z, sub_f(x_max, int_f(1))), int_f(0), add_f(z, int_f(1))))
    y_unit_counter = scan_const_f(lambda z: if_f(eq_f(x_unit_counter.get_seq(), sub_f(x_max, int_f(1))), add_f(z, int_f(1)), z))
    x_counter = scan_const_f(lambda z: if_f(eq_f(x_unit_counter.get_seq(), sub_f(x_max, int_f(1))), int_f(0), add_f(z, x_stride)))
    y_counter = scan_const_f(lambda z: if_f(eq_f(x_unit_counter.get_seq(), sub_f(x_max, int_f(1))), add_f(z, y_stride), z))
    og_design = scan_const_f(lambda z: add_f(add_f(x_counter.get_seq(), y_counter.get_seq()), offset))
    return og_design

og_design = create_og_design()


# optimized addressor design
def create_op_design():
    x_unit_counter = scan_const_f(lambda z: if_f(eq_f(z, sub_f(x_max, int_f(1))), int_f(0), add_f(z, int_f(1))))
    y_unit_counter = scan_const_f(lambda z: if_f(eq_f(x_unit_counter.get_seq(), sub_f(x_max, int_f(1))), add_f(z, int_f(1)), z))
    x_count = x_unit_counter.get_seq()
    y_count = y_unit_counter.get_seq()
    yadd = scan_const_f(lambda z: 
              add_f(z,
                  if_f(eq_f(x_count, sub_f(x_max, int_f(1))),
                      y_stride,
                      x_stride
                  )
              )
           )
    return scan_const_f(lambda z: add_f(yadd.get_seq(), offset))

op_design = create_op_design()


x_width = 16
x_max = var_f("x_max")
y_max = var_f("y_max")
x_stride = var_f("x_stride", x_width)
y_stride = var_f("y_stride")
x_counter = scan_const_f(lambda z: if_f(eq_f(z, sub_f(x_max, int_f(1))), int_f(0), add_f(z, int_f(1))))
y_counter = scan_const_f(lambda z: if_f(eq_f(x_counter.get_seq(), sub_f(x_max, int_f(1))), add_f(z, int_f(1)), z))
def design_b_func(z: Var):
    x_count = x_counter.get_seq()
    y_count = y_counter.get_seq()
    # xadd = add_f(z, x_stride)
    yadd = add_f(z,
              if_f(eq_f(x_count, sub_f(x_max, int_f(1))),
                   y_stride,
                   x_stride
                )
              )
    return if_f(eq_f(y_count, y_max), int_f(0), yadd)


design_b_before_offset = scan_const_f(design_b_func)
design_b = scan_const_f(lambda z: add_f(design_b_before_offset.get_seq(), var_f("offset")))
# print_frail(design_b)
# print_verilog(design_b)

design_a_x = scan_const_f(lambda z: mod_f(add_f(z, int_f(1)), x_max))
# print_frail(design_a_x)

def design_a_y_func(z: Var):
    x_val = design_a_x.get_seq()
    add_val = if_f(eq_f(x_val, x_max), int_f(1), int_f(0))
    return mod_f(add_f(z, add_val), y_max)


design_a_y = scan_const_f(design_a_y_func)
design_a_x_strided = scan_const_f(lambda z: mul_f(design_a_x.get_seq(), var_f("x_stride")))
design_a_y_strided = scan_const_f(lambda z: mul_f(design_a_y.get_seq(), var_f("y_stride")))
design_a_merged = scan_const_f(lambda z: add_f(design_a_x_strided.get_seq(), design_a_y_strided.get_seq()))
# print_frail(design_a_merged)
design_a = scan_const_f(lambda z: add_f(design_a_merged.get_seq(), var_f("offset")))
