from pysmt.shortcuts import Symbol, And, Equals, BVAdd, BVMul, Bool, Ite, BV, BVURem, BVExtract, ForAll, Exists, Portfolio, Solver
from pysmt.typing import BVType 
from pysmt.logics import BV as logicBV
from frail import IteExtend, BVAddExtend, BVSubExtend, BVMulExtend, BVEqualsExtend
import time

op_design_free_vars = {}
op_design_scans = []
op_design_scans_results = []

def scan_const10_f(scan_var_10): 
  if 16 not in op_design_free_vars:
    op_design_free_vars[16] = Symbol("x_max_op_design", BVType(32))
  x16 = op_design_free_vars[16]
  x60 = BV(1,32)
  x61 = BVSubExtend(x16, x60)
  x62 = BVEqualsExtend(scan_var_10, x61)
  x63 = BV(0,32)
  x64 = BV(1,32)
  x65 = BVAddExtend(scan_var_10, x64)
  x66 = IteExtend(x62, x63, x65)
  return x66
op_design_scans.append(scan_const10_f)
op_design_scans_results.append("scan_const10")
scan_const10 = BV(0, 16)

def scan_const11_f(scan_var_11): 
  x38 = scan_const10
  if 16 not in op_design_free_vars:
    op_design_free_vars[16] = Symbol("x_max_op_design", BVType(32))
  x16 = op_design_free_vars[16]
  x39 = BV(1,32)
  x40 = BVSubExtend(x16, x39)
  x41 = BVEqualsExtend(x38, x40)
  x42 = BV(1,32)
  x43 = BVAddExtend(scan_var_11, x42)
  x44 = IteExtend(x41, x43, scan_var_11)
  return x44
op_design_scans.append(scan_const11_f)
op_design_scans_results.append("scan_const11")
scan_const11 = BV(0, 16)

def scan_const14_f(scan_var_14): 
  x12 = scan_const10
  if 16 not in op_design_free_vars:
    op_design_free_vars[16] = Symbol("x_max_op_design", BVType(32))
  x16 = op_design_free_vars[16]
  x54 = BV(1,32)
  x55 = BVSubExtend(x16, x54)
  x56 = BVEqualsExtend(x12, x55)
  if 19 not in op_design_free_vars:
    op_design_free_vars[19] = Symbol("y_stride_op_design", BVType(32))
  x19 = op_design_free_vars[19]
  if 18 not in op_design_free_vars:
    op_design_free_vars[18] = Symbol("x_stride_op_design", BVType(16))
  x18 = op_design_free_vars[18]
  x57 = IteExtend(x56, x19, x18)
  x58 = BVAddExtend(scan_var_14, x57)
  return x58
op_design_scans.append(scan_const14_f)
op_design_scans_results.append("scan_const14")
scan_const14 = BV(0, 16)

def scan_const15_f(scan_var_15): 
  x31 = scan_const11
  if 17 not in op_design_free_vars:
    op_design_free_vars[17] = Symbol("y_max_op_design", BVType(32))
  x17 = op_design_free_vars[17]
  x32 = BVEqualsExtend(x31, x17)
  x33 = BV(0,32)
  x34 = scan_const14
  if 4 not in op_design_free_vars:
    op_design_free_vars[4] = Symbol("offset_op_design", BVType(32))
  x4 = op_design_free_vars[4]
  x35 = BVAddExtend(x34, x4)
  x36 = IteExtend(x32, x33, x35)
  return x36
op_design_scans.append(scan_const15_f)
op_design_scans_results.append("scan_const15")
scan_const15 = BV(0, 16)


from pysmt.shortcuts import Symbol, And, Equals, BVAdd, BVMul, Bool, Ite, BV, BVURem, BVExtract, ForAll, Exists, Portfolio, Solver
from pysmt.typing import BVType 
from pysmt.logics import BV as logicBV
from frail import IteExtend, BVAddExtend, BVSubExtend, BVMulExtend, BVEqualsExtend
import time

og_design_free_vars = {}
og_design_scans = []
og_design_scans_results = []

def scan_const5_f(scan_var_5): 
  if 16 not in og_design_free_vars:
    og_design_free_vars[16] = Symbol("x_max_og_design", BVType(32))
  x16 = og_design_free_vars[16]
  x116 = BV(1,32)
  x117 = BVSubExtend(x16, x116)
  x118 = BVEqualsExtend(scan_var_5, x117)
  x119 = BV(0,32)
  x120 = BV(1,32)
  x121 = BVAddExtend(scan_var_5, x120)
  x122 = IteExtend(x118, x119, x121)
  return x122
og_design_scans.append(scan_const5_f)
og_design_scans_results.append("scan_const5")
scan_const5 = BV(0, 16)

def scan_const6_f(scan_var_6): 
  x77 = scan_const5
  if 16 not in og_design_free_vars:
    og_design_free_vars[16] = Symbol("x_max_og_design", BVType(32))
  x16 = og_design_free_vars[16]
  x78 = BV(1,32)
  x79 = BVSubExtend(x16, x78)
  x80 = BVEqualsExtend(x77, x79)
  x81 = BV(1,32)
  x82 = BVAddExtend(scan_var_6, x81)
  x83 = IteExtend(x80, x82, scan_var_6)
  return x83
og_design_scans.append(scan_const6_f)
og_design_scans_results.append("scan_const6")
scan_const6 = BV(0, 16)

def scan_const7_f(scan_var_7): 
  x93 = scan_const5
  if 16 not in og_design_free_vars:
    og_design_free_vars[16] = Symbol("x_max_og_design", BVType(32))
  x16 = og_design_free_vars[16]
  x94 = BV(1,32)
  x95 = BVSubExtend(x16, x94)
  x96 = BVEqualsExtend(x93, x95)
  x97 = BV(0,32)
  if 18 not in og_design_free_vars:
    og_design_free_vars[18] = Symbol("x_stride_og_design", BVType(16))
  x18 = og_design_free_vars[18]
  x98 = BVAddExtend(scan_var_7, x18)
  x99 = IteExtend(x96, x97, x98)
  return x99
og_design_scans.append(scan_const7_f)
og_design_scans_results.append("scan_const7")
scan_const7 = BV(0, 16)

def scan_const8_f(scan_var_8): 
  x109 = scan_const5
  if 16 not in og_design_free_vars:
    og_design_free_vars[16] = Symbol("x_max_og_design", BVType(32))
  x16 = og_design_free_vars[16]
  x110 = BV(1,32)
  x111 = BVSubExtend(x16, x110)
  x112 = BVEqualsExtend(x109, x111)
  if 19 not in og_design_free_vars:
    og_design_free_vars[19] = Symbol("y_stride_og_design", BVType(32))
  x19 = og_design_free_vars[19]
  x113 = BVAddExtend(scan_var_8, x19)
  x114 = IteExtend(x112, x113, scan_var_8)
  return x114
og_design_scans.append(scan_const8_f)
og_design_scans_results.append("scan_const8")
scan_const8 = BV(0, 16)

def scan_const9_f(scan_var_9): 
  x68 = scan_const6
  if 17 not in og_design_free_vars:
    og_design_free_vars[17] = Symbol("y_max_og_design", BVType(32))
  x17 = og_design_free_vars[17]
  x69 = BVEqualsExtend(x68, x17)
  x70 = BV(0,32)
  x71 = scan_const7
  x72 = scan_const8
  x73 = BVAddExtend(x71, x72)
  if 4 not in og_design_free_vars:
    og_design_free_vars[4] = Symbol("offset_og_design", BVType(32))
  x4 = og_design_free_vars[4]
  x74 = BVAddExtend(x73, x4)
  x75 = IteExtend(x69, x70, x74)
  return x75
og_design_scans.append(scan_const9_f)
og_design_scans_results.append("scan_const9")
scan_const9 = BV(0, 16)


with Solver("cvc4",
       logic=logicBV,
       incremental=True) as s:
    per_step_constraints = []
    for step in range(2):
        print("handling step " + str(step))
        for i in range(len(op_design_scans)):
            globals()[op_design_scans_results[i]] = op_design_scans[i](globals()[op_design_scans_results[i]])
        for i in range(len(og_design_scans)):
            globals()[og_design_scans_results[i]] = og_design_scans[i](globals()[og_design_scans_results[i]])
        per_step_constraints.append(Equals(globals()[op_design_scans_results[len(op_design_scans_results)-1]], globals()[og_design_scans_results[len(og_design_scans_results)-1]]))
    final_constraint = [per_step_constraints[0]]
    for c in per_step_constraints[1:]:
        final_constraint.append(And(final_constraint[-1], c))
    a = {16: og_design_free_vars[16]}
    b = {17: og_design_free_vars[17]}
    s.add_assertion(ForAll(og_design_free_vars.values(), Exists(op_design_free_vars.values(), final_constraint[BVMul(a[16], b[17])])))

    """ s.add_assertion(Equals(og_design_free_vars[18], op_design_free_vars[18]))
    s.add_assertion(Equals(og_design_free_vars[16], op_design_free_vars[16]))
    s.add_assertion(Equals(og_design_free_vars[4], op_design_free_vars[4]))
    del op_design_free_vars[18]
    del op_design_free_vars[16]
    del op_design_free_vars[4] """

    start = time.time()
    res = s.solve()
    assert res
    end = time.time()
    print("time: " + str(end - start))
    
