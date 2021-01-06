
from pysmt.shortcuts import Symbol, And, Equals, BVAdd, BVMul, Bool, Ite, BV, BVURem, BVExtract, ForAll, Exists, Portfolio, Solver
from pysmt.typing import BVType 
from pysmt.logics import BV as logicBV
from frail import BVAddExtend, BVSubExtend, BVMulExtend, BVEqualsExtend
import time

design_a_free_vars = {}
design_a_scans = []
design_a_scans_results = []

def scan_const3_f(scan_var_3): 
  x40 = BV(1,32)
  x41 = BVAddExtend(scan_var_3, x40)
  if 0 not in design_a_free_vars:
    design_a_free_vars[0] = Symbol("x_max", BVType(32))
  x0 = design_a_free_vars[0]
  x42 = BVURem(x41, x0)
  return x42
design_a_scans.append(scan_const3_f)
design_a_scans_results.append("scan_const3")
scan_const3 = BV(0, 32)

def scan_const4_f(scan_var_4): 
  x30 = scan_const3
  if 0 not in design_a_free_vars:
    design_a_free_vars[0] = Symbol("x_max", BVType(32))
  x0 = design_a_free_vars[0]
  x31 = BV(1,32)
  x32 = BVSubExtend(x0, x31)
  x33 = BVEqualsExtend(x30, x32)
  x34 = BV(1,32)
  x35 = BV(0,32)
  x36 = Ite(x33, x34, x35)
  x37 = BVAddExtend(scan_var_4, x36)
  if 1 not in design_a_free_vars:
    design_a_free_vars[1] = Symbol("y_max", BVType(32))
  x1 = design_a_free_vars[1]
  x38 = BVURem(x37, x1)
  return x38
design_a_scans.append(scan_const4_f)
design_a_scans_results.append("scan_const4")
scan_const4 = BV(0, 32)

def scan_const5_f(scan_var_5): 
  x18 = scan_const3
  if 19 not in design_a_free_vars:
    design_a_free_vars[19] = Symbol("x_stride", BVType(32))
  x19 = design_a_free_vars[19]
  x20 = BVMulExtend(x18, x19)
  return x20
design_a_scans.append(scan_const5_f)
design_a_scans_results.append("scan_const5")
scan_const5 = BV(0, 32)

def scan_const6_f(scan_var_6): 
  x26 = scan_const4
  if 27 not in design_a_free_vars:
    design_a_free_vars[27] = Symbol("y_stride", BVType(32))
  x27 = design_a_free_vars[27]
  x28 = BVMulExtend(x26, x27)
  return x28
design_a_scans.append(scan_const6_f)
design_a_scans_results.append("scan_const6")
scan_const6 = BV(0, 32)

def scan_const7_f(scan_var_7): 
  x14 = scan_const5
  x15 = scan_const6
  x16 = BVAddExtend(x14, x15)
  return x16
design_a_scans.append(scan_const7_f)
design_a_scans_results.append("scan_const7")
scan_const7 = BV(0, 32)

def scan_const8_f(scan_var_8): 
  x10 = scan_const7
  if 11 not in design_a_free_vars:
    design_a_free_vars[11] = Symbol("offset", BVType(32))
  x11 = design_a_free_vars[11]
  x12 = BVAddExtend(x10, x11)
  return x12
design_a_scans.append(scan_const8_f)
design_a_scans_results.append("scan_const8")
scan_const8 = BV(0, 32)


from pysmt.shortcuts import Symbol, And, Equals, BVAdd, BVMul, Bool, Ite, BV, BVURem, BVExtract, ForAll, Exists, Portfolio, Solver
from pysmt.typing import BVType 
from pysmt.logics import BV as logicBV
from frail import BVAddExtend, BVSubExtend, BVMulExtend, BVEqualsExtend
import time

design_b_free_vars = {}
design_b_scans = []
design_b_scans_results = []

def scan_const2_f(scan_var_2): 
  if 44 not in design_b_free_vars:
    design_b_free_vars[44] = Symbol("x_delta", BVType(12))
  x44 = design_b_free_vars[44]
  x45 = BVAddExtend(scan_var_2, x44)
  x46 = BVExtract(x45, 0, 12 - 1)
  if 0 not in design_b_free_vars:
    design_b_free_vars[0] = Symbol("x_max", BVType(32))
  x0 = design_b_free_vars[0]
  x47 = BVEqualsExtend(x46, x0)
  if 48 not in design_b_free_vars:
    design_b_free_vars[48] = Symbol("y_delta", BVType(32))
  x48 = design_b_free_vars[48]
  if 49 not in design_b_free_vars:
    design_b_free_vars[49] = Symbol("x_delta", BVType(12))
  x49 = design_b_free_vars[49]
  x50 = Ite(x47, x48, x49)
  x51 = BVAddExtend(scan_var_2, x50)
  if 1 not in design_b_free_vars:
    design_b_free_vars[1] = Symbol("y_max", BVType(32))
  x1 = design_b_free_vars[1]
  x52 = BVEqualsExtend(x51, x1)
  x53 = BV(0,32)
  x54 = Ite(x52, x53, x51)
  return x54
design_b_scans.append(scan_const2_f)
design_b_scans_results.append("scan_const2")
scan_const2 = BV(0, 32)


with Solver("cvc4",
       logic=logicBV,
       incremental=True) as s:
    per_step_constraints = []
    for step in range(1000):
        print("handling step " + str(step))
        for i in range(len(design_a_scans)):
            globals()[design_a_scans_results[i]] = design_a_scans[i](globals()[design_a_scans_results[i]])
        for i in range(len(design_b_scans)):
            globals()[design_b_scans_results[i]] = design_b_scans[i](globals()[design_b_scans_results[i]])
        per_step_constraints.append(Equals(globals()[design_a_scans_results[len(design_a_scans_results)-1]], globals()[design_b_scans_results[len(design_b_scans_results)-1]]))
    final_constraint = per_step_constraints[0]
    for c in per_step_constraints[1:]:
        final_constraint = And(final_constraint, c) 
    s.add_assertion(ForAll(design_a_free_vars.values(), Exists(design_b_free_vars.values(), final_constraint)))
    start = time.time()
    res = s.solve()
    assert res
    end = time.time()
    print("time: " + str(end - start))
    
