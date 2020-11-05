from frail.ast import *


def recur_func(z: Var):
    x_width = 12
    z = add_f(z, var_f("x_delta", x_width))
    z = add_f(z,
              if_f(eq_f(select_bits_f(z, x_width), int_f(0)),
                   var_f("y_delta"),
                   int_f(0)
                   )
              )
    return z


scan_recur = scan_const_f(recur_func)

x_max = var_f("x_max")
y_max = var_f("y_max")
multi_scan_x = scan_const_f(lambda z: mod_f(add_f(z, int_f(1)), x_max))

def multi_scan_y_func(z: Var):
    x_val = multi_scan_x.get_seq()
    add_val = if_f(eq_f(x_val, x_max), int_f(1), int_f(0))
    return mod_f(add_f(z, add_val), y_max)


multi_scan_y = scan_const_f(multi_scan_y_func)


