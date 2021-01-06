from pysmt.shortcuts import BVZExt, BVAdd, BVSub, BVMul, Equals, Ite

def IteExtend(b, t0,t1):
  orig_width_t0 = t0.get_type().width
  orig_width_t1 = t1.get_type().width
  orig_width = max(orig_width_t0,orig_width_t1)
  t0e = BVZExt(t0, max(orig_width-orig_width_t0, 0))
  t1e = BVZExt(t1, max(orig_width-orig_width_t1, 0))
  return Ite(b, t0e, t1e)

def BVAddExtend(t0,t1):
  orig_width_t0 = t0.get_type().width
  orig_width_t1 = t1.get_type().width
  orig_width = max(orig_width_t0,orig_width_t1)
  t0e = BVZExt(t0, max(orig_width-orig_width_t0, 0))
  t1e = BVZExt(t1, max(orig_width-orig_width_t1, 0))
  return BVAdd(t0e, t1e)

def BVSubExtend(t0,t1):
  orig_width_t0 = t0.get_type().width
  orig_width_t1 = t1.get_type().width
  orig_width = max(orig_width_t0,orig_width_t1)
  t0e = BVZExt(t0, max(orig_width-orig_width_t0, 0))
  t1e = BVZExt(t1, max(orig_width-orig_width_t1, 0))
  return BVSub(t0e, t1e)

def BVMulExtend(t0,t1):
  orig_width_t0 = t0.get_type().width
  orig_width_t1 = t1.get_type().width
  orig_width = max(orig_width_t0,orig_width_t1)
  t0e = BVZExt(t0, max(orig_width-orig_width_t0, 0))
  t1e = BVZExt(t1, max(orig_width-orig_width_t1, 0))
  return BVMul(t0e, t1e)

def BVEqualsExtend(t0,t1):
  orig_width_t0 = t0.get_type().width
  orig_width_t1 = t1.get_type().width
  orig_width = max(orig_width_t0,orig_width_t1)
  t0e = BVZExt(t0, max(orig_width-orig_width_t0, 0))
  t1e = BVZExt(t1, max(orig_width-orig_width_t1, 0))
  return Equals(t0e, t1e)
