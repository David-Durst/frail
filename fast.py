from dataclasses import dataclass
from typing import Callable

@dataclass(eq=True)
class LakeDSLState():
    cur_index: int = 0
    def incr(self):
        old = self.cur_index
        self.cur_index = old + 1
        return old

default_lake_state = LakeDSLState()

@dataclass(eq=True, frozen=True)
class AST():
    index: int

@dataclass(eq=True, frozen=True)
class Var(AST):
    name: str

def varL(name: str, lake_state: LakeDSLState = default_lake_state):
    return Var(lake_state.incr(), name)

@dataclass(eq=True, frozen=True)
class Int(AST):
    val: int
    producing_seq: int = None

def intL(val: int, lake_state: LakeDSLState = default_lake_state):
    return Int(lake_state.incr(), val)

@dataclass(eq=True, frozen=True)
class Bool(AST):
    val: bool
    producing_seq: int = None

def boolL(val: bool, lake_state: LakeDSLState = default_lake_state):
    return Int(lake_state.incr(), val)

@dataclass(eq=True, frozen=True)
class RecurrenceSeq(AST):
    producing_recurrence: int

    def get_ith_element(self, lake_state: LakeDSLState = default_lake_state):
        return Int(lake_state.incr(), None, self.index)


def recurrence_seqL(producing_recurrence: int, lake_state: LakeDSLState = default_lake_state):
    return Int(lake_state.incr(), producing_recurrence)

@dataclass(eq=True, frozen=True)
class BinOp(AST):
    arg0: AST
    arg1: AST

@dataclass(frozen=True)
class AddOp(BinOp):
    pass

def addL(arg0: AST, arg1: AST, lake_state: LakeDSLState = default_lake_state) -> AST:
    return AddOp(lake_state.incr(), arg0, arg1)

@dataclass(frozen=True)
class ModOp(BinOp):
    pass

def modL(arg0: AST, arg1: AST, lake_state: LakeDSLState = default_lake_state) -> AST:
    return ModOp(lake_state.incr(), arg0, arg1)

@dataclass(frozen=True)
class SelectBitsOp(BinOp):
    pass

def select_bitsL(arg0: AST, arg1: AST, lake_state: LakeDSLState = default_lake_state) -> AST:
    return SelectBitsOp(lake_state.incr(), arg0, arg1)

@dataclass(frozen=True)
class IfOp(BinOp):
    b: AST

def ifL(b: Bool, arg0: AST, arg1: AST, lake_state: LakeDSLState = default_lake_state):
    return IfOp(lake_state.incr(), arg0, arg1, b)

@dataclass(frozen=True)
class EqOp(BinOp):
    pass

def eqL(arg0: AST, arg1: AST, lake_state: LakeDSLState = default_lake_state):
    return EqOp(lake_state.incr(), arg0, arg1)

@dataclass(frozen=True)
class ScanConstOp(BinOp):
    f: Callable[[Var], Int]

    def get_seq(self, lake_state: LakeDSLState = default_lake_state):
        return RecurrenceSeq(lake_state.incr(), self.index)

def scan_constL(f: Callable[[Var], Int], lake_state: LakeDSLState = default_lake_state):
    return ScanConstOp(lake_state.incr(), f)
"""
@dataclass(frozen=True)
class Affine_Seq():
    a: AST
    y: AST
    num: int
    incr: int
    bit_width: int

@dataclass(frozen=True)
class Const(AST):
    val: int
    width: int

@dataclass(frozen=True)
class MulOp(AST):
    left: AST
    right: AST

@dataclass(frozen=True)
class AddOp(AST):
    left: AST
    right: AST


@dataclass(frozen=True)
class Counter(AST):
    a: int
@dataclass(frozen=True)
class Numeric_Expr():
    var: str
    const: int
    has_var: bool
    
    def __str__(self):
        if self.has_var and self.const != 0:
            return "{}+"
            result 

@dataclass(frozen=True)
class Affine_Seq():
    a: int
    y: int
    num: int
    incr: int
    bit_width: int

    def eq_str(self):
        return "{}*x + y for 0 to {} by {} width {}".format(str(self.a), str(self.y),
                                                            str(self.num*self.incr), self.incr, self.bit_width)

@dataclass(frozen=True)
class Nested_Affine_Seq():
    a: [int]
    y: [int]
    num: int
    incr: [int]
    bit_width: [int]

    def eq_str(self):
        widths = sum(self.bit_width)

        return "{}*x + y for 0 to {} by {} width {}".format(str(self.a), str(self.y),
                                                            str(self.num*self.incr), self.incr, self.bit_width)
"""
