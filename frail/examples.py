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

def create_og_design_dim(dim, width=16):

    # configuration registers
    ranges = {}
    strides = {}
    for i in range(dim):
        ranges[i] = var_f(f"range_{i}", width)
        strides[i] = var_f(f"stride_{i}", width)
    offset = var_f("offset", width)

    unit_counters = {}
    unit_counters[0] = scan_const_f(lambda z: if_f(eq_f(z, sub_f(ranges[0], int_f(1))), int_f(0), add_f(z, int_f(1))))
    for k in range(1, dim):
        uc = (unit_counters[k - 1]).get_seq()
        r = ranges[k - 1]
        unit_counters[k] = scan_const_f(lambda z: if_f(eq_f(uc, sub_f(r, int_f(1))), add_f(z, int_f(1)), z))
    
    counters = [scan_const_f(lambda z: if_f(eq_f(unit_counters[0].get_seq(), sub_f(ranges[0], int_f(1))), int_f(0), add_f(z, strides[0])))]
    for j in range(1, dim):
        uc = unit_counters[j - 1].get_seq()
        r = ranges[j - 1]
        s = strides[j]
        counters.append(scan_const_f(lambda z: if_f(eq_f(uc, sub_f(r, int_f(1))), add_f(z, s), z)))


    add_counters = offset
    for i in range(dim):
        add_counters = add_f(counters[i].get_seq(), add_counters)
    return unit_counters[1] #scan_const_f(lambda z: add_counters)

og_design_dim = create_og_design_dim(6)

""" def create_og_design():
    dim = 6

    # configuration registers
    ranges = [var_f(f"range_{i}") for i in range(dim)]
    strides = [var_f(f"stride_{i}") for i in range(dim)]
    offset = var_f("offset")

    unit_counters = [scan_const_f(lambda z: if_f(eq_f(z, sub_f(ranges[0], int_f(1))), int_f(0), add_f(z, int_f(1))))]
    for i in range(1, dim):
        unit_counters.append(scan_const_f(lambda z: if_f(eq_f(unit_counters[i - 1].get_seq(), sub_f(ranges[i - 1], int_f(1))), add_f(z, int_f(1)), z)))
    
    counters = [scan_const_f(lambda z: if_f(eq_f(unit_counters[0].get_seq(), sub_f(ranges[0], int_f(1))), int_f(0), add_f(z, strides[0])))]
    for i in range(1, dim):
        counters.append(scan_const_f(lambda z: if_f(eq_f(unit_counters[i - 1].get_seq(), sub_f(ranges[i - 1], int_f(1))), add_f(z, strides[i]), z)))

    add_counters = offset
    for i in range(dim):
        add_counters = add_f(counters[i].get_seq(), add_counters)
    return scan_const_f(lambda z: add_counters)

og_design = create_og_design()

ranges = [var_f(f"range_{i}", width) for i in range(dim)]
    strides = [var_f(f"stride_{i}", width) for i in range(dim)]
    offset = var_f("offset", width)

    unit_counters = [scan_const_f(lambda z: if_f(eq_f(z, sub_f(ranges[0], int_f(1))), int_f(0), add_f(z, int_f(1))))]
    for k in range(1, dim):
        uc = (unit_counters[k - 1]).get_seq()
        r = ranges[k - 1]
        unit_counters.append(scan_const_f(lambda z: if_f(eq_f(uc, sub_f(r, int_f(1))), add_f(z, int_f(1)), z)))
    
    counters = [scan_const_f(lambda z: if_f(eq_f(unit_counters[0].get_seq(), sub_f(ranges[0], int_f(1))), int_f(0), add_f(z, strides[0])))]
    for j in range(1, dim):
        uc = unit_counters[j - 1].get_seq()
        r = ranges[j - 1]
        s = strides[j - 1]
        counters.append(scan_const_f(lambda z: if_f(eq_f(uc, sub_f(r, int_f(1))), add_f(z, s), z)))


    add_counters = offset
    for i in range(dim):
        add_counters = add_f(counters[i].get_seq(), add_counters)
    return unit_counters[1] #scan_const_f(lambda z: add_counters)

og_design6 = create_og_design_dim(6) """

def create_og_design6():

    # configuration registers
    r0, r1, r2, r3, r4, r5 = var_f("ranges_0"), var_f("ranges_1"), var_f("ranges_2"), var_f("ranges_3"), var_f("ranges_4"), var_f("ranges_5")
    s0, s1, s2, s3, s4, s5 = var_f("strides_0"), var_f("strides_1"), var_f("strides_2"), var_f("strides_3"), var_f("strides_4"), var_f("strides_5")
    dim = var_f("dimensionality")
    offset = var_f("starting_addr")

    uc0 = scan_const_f(lambda z: if_f(eq_f(z, sub_f(r0, int_f(1))), int_f(0), add_f(z, int_f(1))))
    #uc0 = scan_const_f(lambda z: if_f(eq_f(dim, int_f(0)), int_f(0), uc0.get_seq()))
    uc1 = scan_const_f(lambda z: if_f(eq_f(uc0.get_seq(), sub_f(r0, int_f(1))), add_f(z, int_f(1)), z))
    #uc1 = scan_const_f(lambda z: if_f(eq_f(dim, int_f(1)), int_f(0), uc1.get_seq()))
    uc2 = scan_const_f(lambda z: if_f(eq_f(uc1.get_seq(), sub_f(r1, int_f(1))), add_f(z, int_f(1)), z))
    #uc2 = scan_const_f(lambda z: if_f(eq_f(dim, int_f(2)), int_f(0), uc2.get_seq()))
    uc3 = scan_const_f(lambda z: if_f(eq_f(uc2.get_seq(), sub_f(r2, int_f(1))), add_f(z, int_f(1)), z))
    #uc3 = scan_const_f(lambda z: if_f(eq_f(dim, int_f(3)), int_f(0), uc3.get_seq()))
    uc4 = scan_const_f(lambda z: if_f(eq_f(uc3.get_seq(), sub_f(r3, int_f(1))), add_f(z, int_f(1)), z))
    #uc4 = scan_const_f(lambda z: if_f(eq_f(dim, int_f(4)), int_f(0), uc4.get_seq()))
    uc5 = scan_const_f(lambda z: if_f(eq_f(uc4.get_seq(), sub_f(r4, int_f(1))), add_f(z, int_f(1)), z))
    #uc5 = scan_const_f(lambda z: if_f(eq_f(dim, int_f(5)), int_f(0), uc5.get_seq()))

    c0 = scan_const_f(lambda z: if_f(eq_f(uc0.get_seq(), sub_f(r0, int_f(1))), int_f(0), add_f(z, s0)))
    c1 = scan_const_f(lambda z: if_f(eq_f(uc0.get_seq(), sub_f(r0, int_f(1))), add_f(z, s1), z))
    c2 = scan_const_f(lambda z: if_f(eq_f(uc1.get_seq(), sub_f(r1, int_f(1))), add_f(z, s2), z))
    c3 = scan_const_f(lambda z: if_f(eq_f(uc2.get_seq(), sub_f(r2, int_f(1))), add_f(z, s3), z))
    c4 = scan_const_f(lambda z: if_f(eq_f(uc3.get_seq(), sub_f(r3, int_f(1))), add_f(z, s4), z))
    c5 = scan_const_f(lambda z: if_f(eq_f(uc4.get_seq(), sub_f(r4, int_f(1))), add_f(z, s5), z))

    return scan_const_f(lambda z: add_f(offset, add_f(c0.get_seq(), add_f(c1.get_seq(), add_f(c2.get_seq(), add_f(c3.get_seq(), add_f(c4.get_seq(), c5.get_seq())))))))

og_design6 = create_og_design6()

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
