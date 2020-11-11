
from pysmt.shortcuts import Symbol, And, Equals, BVAdd, BVMul, Bool, Ite, BV, BVURem, BVExtract, ForAll, Exists, Portfolio, Solver, is_sat, write_smtlib
from pysmt.typing import BVType 
from pysmt.logics import BV as logicBV
from frail import BVAddExtend, BVMulExtend, BVEqualsExtend
import time

design_a_free_vars = {}
design_a_scans = []
design_a_scans_results = []

def scan_const3_f(scan_var_3): 
  x38 = BV(1,32)
  x39 = BVAddExtend(scan_var_3, x38)
  if 1 not in design_a_free_vars:
    design_a_free_vars[1] = Symbol("x_max", BVType(32))
  x1 = design_a_free_vars[1]
  x40 = BVURem(x39, x1)
  return x40
design_a_scans.append(scan_const3_f)
design_a_scans_results.append("scan_const3")
scan_const3 = BV(0, 32)

def scan_const4_f(scan_var_4): 
  x30 = scan_const3
  if 1 not in design_a_free_vars:
    design_a_free_vars[1] = Symbol("x_max", BVType(32))
  x1 = design_a_free_vars[1]
  x31 = BVEqualsExtend(x30, x1)
  x32 = BV(1,32)
  x33 = BV(0,32)
  x34 = Ite(x31, x32, x33)
  x35 = BVAddExtend(scan_var_4, x34)
  if 2 not in design_a_free_vars:
    design_a_free_vars[2] = Symbol("y_max", BVType(32))
  x2 = design_a_free_vars[2]
  x36 = BVURem(x35, x2)
  return x36
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


from pysmt.shortcuts import Symbol, And, Equals, BVAdd, BVMul, Bool, Ite, BV, BVURem, BVExtract, ForAll, Exists, Portfolio, Solver, is_sat, write_smtlib
from pysmt.typing import BVType 
from pysmt.logics import BV as logicBV
from frail import BVAddExtend, BVMulExtend, BVEqualsExtend
import time

design_b_free_vars = {}
design_b_scans = []
design_b_scans_results = []

def scan_const0_f(scan_var_0): 
  if 42 not in design_b_free_vars:
    design_b_free_vars[42] = Symbol("x_delta", BVType(12))
  x42 = design_b_free_vars[42]
  x43 = BVAddExtend(scan_var_0, x42)
  x44 = BVExtract(x43, 0, 12 - 1)
  x45 = BV(0,32)
  x46 = BVEqualsExtend(x44, x45)
  if 47 not in design_b_free_vars:
    design_b_free_vars[47] = Symbol("y_delta", BVType(32))
  x47 = design_b_free_vars[47]
  x48 = BV(0,32)
  x49 = Ite(x46, x47, x48)
  x50 = BVAddExtend(x43, x49)
  return x50
design_b_scans.append(scan_const0_f)
design_b_scans_results.append("scan_const0")
scan_const0 = BV(0, 32)


res = Bool(True)
with Solver("cvc4",
       logic=logicBV,
       incremental=True) as s:
    for step in range(30):
        print("handling step " + str(step))
        start = time.time()
        for i in range(len(design_a_scans)):
            globals()[design_a_scans_results[i]] = design_a_scans[i](globals()[design_a_scans_results[i]])
        for i in range(len(design_b_scans)):
            globals()[design_b_scans_results[i]] = design_b_scans[i](globals()[design_b_scans_results[i]])
        res = And(res, ForAll(design_a_free_vars.values(), Exists(design_b_free_vars.values(), Equals(globals()[design_a_scans_results[i]], globals()[design_b_scans_results[i]]))))
        end = time.time()
        print("time: " + str(round(end - start,2)) + "s")
write_smtlib(res, "res.smtlib")
    
