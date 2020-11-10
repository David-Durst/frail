from pysmt.shortcuts import BVZExt, BVAdd, BVMul

def BVAddExtend(t0,t1):
  orig_width_t0 = t0.get_type().width
  orig_width_t1 = t1.get_sort().width
  orig_width = max(orig_width_t0,orig_width_t1)
  t0e = BVZExt(t0, max(orig_width-orig_width_t0, 0))
  t1e = BVZExt(t0, max(orig_width-orig_width_t1, 0))
  return BVAdd(t0e, t1e)

def BVMulExtend(t0,t1):
  orig_width_t0 = t0.get_type().width
  orig_width_t1 = t1.get_sort().width
  orig_width = max(orig_width_t0,orig_width_t1)
  t0e = BVZExt(t0, max(orig_width-orig_width_t0, 0))
  t1e = BVZExt(t0, max(orig_width-orig_width_t1, 0))
  return BVMul(t0e, t1e)
