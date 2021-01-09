
from pysmt.shortcuts import Symbol, And, Equals, BVAdd, BVMul, Bool, Ite, BV, BVURem, BVExtract, ForAll, Exists, Portfolio, Solver, TRUE
from pysmt.typing import BVType 
from pysmt.logics import BV as logicBV
from frail import IteExtend, BVAddExtend, BVSubExtend, BVMulExtend, BVEqualsExtend
import time

op_design_free_vars = {}
op_design_scans = []
op_design_scans_results = []

def scan_const10_f(scan_var_10): 
  if 16 not in op_design_free_vars:
    op_design_free_vars[16] = Symbol("x_max_op_design", BVType(16))
  x16 = op_design_free_vars[16]
  x40 = BV(1,16)
  x41 = BVSubExtend(x16, x40)
  x42 = BVEqualsExtend(scan_var_10, x41)
  x43 = BV(0,16)
  x44 = BV(1,16)
  x45 = BVAddExtend(scan_var_10, x44)
  x46 = IteExtend(x42, x43, x45)
  return x46
op_design_scans.append(scan_const10_f)
op_design_scans_results.append("scan_const10")
scan_const10 = BV(0, 16)

def scan_const14_f(scan_var_14): 
  x12 = scan_const10
  if 16 not in op_design_free_vars:
    op_design_free_vars[16] = Symbol("x_max_op_design", BVType(16))
  x16 = op_design_free_vars[16]
  x34 = BV(1,16)
  x35 = BVSubExtend(x16, x34)
  x36 = BVEqualsExtend(x12, x35)
  if 19 not in op_design_free_vars:
    op_design_free_vars[19] = Symbol("y_stride_op_design", BVType(16))
  x19 = op_design_free_vars[19]
  if 18 not in op_design_free_vars:
    op_design_free_vars[18] = Symbol("x_stride_op_design", BVType(16))
  x18 = op_design_free_vars[18]
  x37 = IteExtend(x36, x19, x18)
  x38 = BVAddExtend(scan_var_14, x37)
  return x38
op_design_scans.append(scan_const14_f)
op_design_scans_results.append("scan_const14")
scan_const14 = BV(0, 16)

def scan_const15_f(scan_var_15): 
  x31 = scan_const14
  if 4 not in op_design_free_vars:
    op_design_free_vars[4] = Symbol("offset_op_design", BVType(16))
  x4 = op_design_free_vars[4]
  x32 = BVAddExtend(x31, x4)
  return x32
op_design_scans.append(scan_const15_f)
op_design_scans_results.append("scan_const15")
scan_const15 = BV(0, 16)


from pysmt.shortcuts import Symbol, And, Equals, BVAdd, BVMul, Bool, Ite, BV, BVURem, BVExtract, ForAll, Exists, Portfolio, Solver, TRUE
from pysmt.typing import BVType 
from pysmt.logics import BV as logicBV
from frail import IteExtend, BVAddExtend, BVSubExtend, BVMulExtend, BVEqualsExtend
import time

og_design_free_vars = {}
og_design_scans = []
og_design_scans_results = []

def scan_const5_f(scan_var_5): 
  if 16 not in og_design_free_vars:
    og_design_free_vars[16] = Symbol("x_max_og_design", BVType(16))
  x16 = og_design_free_vars[16]
  x76 = BV(1,16)
  x77 = BVSubExtend(x16, x76)
  x78 = BVEqualsExtend(scan_var_5, x77)
  x79 = BV(0,16)
  x80 = BV(1,16)
  x81 = BVAddExtend(scan_var_5, x80)
  x82 = IteExtend(x78, x79, x81)
  return x82
og_design_scans.append(scan_const5_f)
og_design_scans_results.append("scan_const5")
scan_const5 = BV(0, 16)

def scan_const7_f(scan_var_7): 
  x53 = scan_const5
  if 16 not in og_design_free_vars:
    og_design_free_vars[16] = Symbol("x_max_og_design", BVType(16))
  x16 = og_design_free_vars[16]
  x54 = BV(1,16)
  x55 = BVSubExtend(x16, x54)
  x56 = BVEqualsExtend(x53, x55)
  x57 = BV(0,16)
  if 18 not in og_design_free_vars:
    og_design_free_vars[18] = Symbol("x_stride_og_design", BVType(16))
  x18 = og_design_free_vars[18]
  x58 = BVAddExtend(scan_var_7, x18)
  x59 = IteExtend(x56, x57, x58)
  return x59
og_design_scans.append(scan_const7_f)
og_design_scans_results.append("scan_const7")
scan_const7 = BV(0, 16)

def scan_const8_f(scan_var_8): 
  x69 = scan_const5
  if 16 not in og_design_free_vars:
    og_design_free_vars[16] = Symbol("x_max_og_design", BVType(16))
  x16 = og_design_free_vars[16]
  x70 = BV(1,16)
  x71 = BVSubExtend(x16, x70)
  x72 = BVEqualsExtend(x69, x71)
  if 19 not in og_design_free_vars:
    og_design_free_vars[19] = Symbol("y_stride_og_design", BVType(16))
  x19 = og_design_free_vars[19]
  x73 = BVAddExtend(scan_var_8, x19)
  x74 = IteExtend(x72, x73, scan_var_8)
  return x74
og_design_scans.append(scan_const8_f)
og_design_scans_results.append("scan_const8")
scan_const8 = BV(0, 16)

def scan_const9_f(scan_var_9): 
  x48 = scan_const7
  x49 = scan_const8
  x50 = BVAddExtend(x48, x49)
  if 4 not in og_design_free_vars:
    og_design_free_vars[4] = Symbol("offset_og_design", BVType(16))
  x4 = og_design_free_vars[4]
  x51 = BVAddExtend(x50, x4)
  return x51
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
    final_constraint = Or(Not(Equals(op_design_free_vars[17], og_design_free_vars[17])), Or(Not(Equals(op_design_free_vars[16], og_design_free_vars[16])), TRUE()))
    for c in per_step_constraints:
        final_constraint = And(final_constraint, c) 
    s.add_assertion(ForAll(op_design_free_vars.values(), Exists(og_design_free_vars.values(), final_constraint)))
    start = time.time()
    res = s.solve()
    assert res
    end = time.time()
    print("time: " + str(end - start))
    
