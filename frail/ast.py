from dataclasses import dataclass, field
from typing import Callable, Dict, Union


@dataclass(eq=True)
class AST():
    index: int

    def __post_init__(self):
        default_lake_state.program_map[self.index] = self


@dataclass(eq=True)
class LakeDSLState():
    cur_index: int = 0
    program_map: Dict[int, AST] = field(default_factory=dict)

    def incr(self):
        old = self.cur_index
        self.cur_index = old + 1
        return old


default_lake_state = LakeDSLState()


@dataclass(eq=True)
class Var(AST):
    name: str
    width: int


def var_f(name: str, width: int = 16, lake_state: LakeDSLState = default_lake_state) -> Var:
    return Var(lake_state.incr(), name, width)


@dataclass(eq=True)
class Int(AST):
    val: int
    width: int


def int_f(val: int, bit_width: int = 16, lake_state: LakeDSLState = default_lake_state) -> Int:
    return Int(lake_state.incr(), val, bit_width)


@dataclass(eq=True)
class Bool(AST):
    val: bool
    producing_seq: int = None
    width: int = 1


def bool_f(val: bool, lake_state: LakeDSLState = default_lake_state) -> Bool:
    return Int(lake_state.incr(), val)


@dataclass(eq=True)
class RecurrenceSeq(AST):
    producing_recurrence: int


def recurrence_seq_f(producing_recurrence: int, lake_state: LakeDSLState = default_lake_state) -> RecurrenceSeq:
    return RecurrenceSeq(lake_state.incr(), producing_recurrence)


@dataclass(eq=True)
class CounterSeq(AST):
    producing_counter: int
    # true if is_max signal, false if just value signal
    is_max_signal: int


def counter_seq_f(producing_counter: int, is_max_signal: bool, lake_state: LakeDSLState = default_lake_state) -> CounterSeq:
    return CounterSeq(lake_state.incr(), producing_counter, is_max_signal)


@dataclass(eq=True)
class BinOp(AST):
    arg0_index: int
    arg1_index: int


@dataclass()
class AddOp(BinOp):
    pass


def add_f(arg0: AST, arg1: AST, lake_state: LakeDSLState = default_lake_state) -> AddOp:
    return AddOp(lake_state.incr(), arg0.index, arg1.index)


@dataclass()
class SubOp(BinOp):
    pass


def sub_f(arg0: AST, arg1: AST, lake_state: LakeDSLState = default_lake_state) -> SubOp:
    return SubOp(lake_state.incr(), arg0.index, arg1.index)


@dataclass()
class MulOp(BinOp):
    pass


def mul_f(arg0: AST, arg1: AST, lake_state: LakeDSLState = default_lake_state) -> MulOp:
    return MulOp(lake_state.incr(), arg0.index, arg1.index)


@dataclass()
class ModOp(BinOp):
    pass


def mod_f(arg0: AST, arg1: AST, lake_state: LakeDSLState = default_lake_state) -> ModOp:
    return ModOp(lake_state.incr(), arg0.index, arg1.index)


@dataclass()
class SelectBitsOp(AST):
    arg0_index: int
    bits: int
    pass


def select_bits_f(arg0: AST, arg1: int, lake_state: LakeDSLState = default_lake_state) -> SelectBitsOp:
    return SelectBitsOp(lake_state.incr(), arg0.index, arg1)


@dataclass()
class IfOp(BinOp):
    b_index: int


def if_f(b: Bool, arg0: AST, arg1: AST, lake_state: LakeDSLState = default_lake_state) -> IfOp:
    return IfOp(lake_state.incr(), arg0.index, arg1.index, b.index)


@dataclass()
class EqOp(BinOp):
    width: int = 1


def eq_f(arg0: AST, arg1: AST, lake_state: LakeDSLState = default_lake_state) -> EqOp:
    return EqOp(lake_state.incr(), arg0.index, arg1.index)

@dataclass()
class LTOp(BinOp):
    width: int = 1

def lt_f(arg0: AST, arg1: AST, lake_state: LakeDSLState = default_lake_state) -> LTOp:
    return LTOp(lake_state.incr(), arg0.index, arg1.index)

@dataclass()
class GTOp(BinOp):
    width: int = 1
    
def gt_f(arg0: AST, arg1: AST, lake_state: LakeDSLState = default_lake_state) -> GTOp:
    return GTOp(lake_state.incr(), arg0.index, arg1.index)

@dataclass()
class CounterOp(AST):
    prev_level_input: AST
    max_val: int
    is_max_wire: int
    incr_amount: AST
    width: int

    def at_max(self, lake_state: LakeDSLState = default_lake_state):
        return CounterSeq(lake_state.incr(), self.index, True)

    def val(self, lake_state: LakeDSLState = default_lake_state):
        return CounterSeq(lake_state.incr(), self.index, False)


def counter_f(prev_level_input: AST, max_val: Union[AST, int], incr_amount: AST, width: int = 16,
              lake_state: LakeDSLState = default_lake_state) -> CounterOp:
    max_val_storage = max_val.index if isinstance(max_val, AST) else max_val
    prev_level_input_storage = prev_level_input.index if prev_level_input is not None else None
    return CounterOp(lake_state.incr(), prev_level_input_storage, max_val_storage, isinstance(max_val, AST), incr_amount, width)

@dataclass()
class ScanConstOp(AST):
    f: Callable[[Var], AST]
    width: int

    def get_seq(self, lake_state: LakeDSLState = default_lake_state):
        return RecurrenceSeq(lake_state.incr(), self.index)


def scan_const_f(f: Callable[[Var], AST], width: int = 16, lake_state: LakeDSLState = default_lake_state) -> ScanConstOp:
    return ScanConstOp(lake_state.incr(), f, width)


"""
@dataclass()
class Affine_Seq():
    a: AST
    y: AST
    num: int
    incr: int
    bit_width: int

@dataclass()
class Const(AST):
    val: int
    width: int

@dataclass()
class MulOp(AST):
    left: AST
    right: AST

@dataclass()
class AddOp(AST):
    left: AST
    right: AST


@dataclass()
class Counter(AST):
    a: int
@dataclass()
class Numeric_Expr():
    var: str
    const: int
    has_var: bool
    
    def __str__(self):
        if self.has_var and self.const != 0:
            return "{}+"
            result 

@dataclass()
class Affine_Seq():
    a: int
    y: int
    num: int
    incr: int
    bit_width: int

    def eq_str(self):
        return "{}*x + y for 0 to {} by {} width {}".format(str(self.a), str(self.y),
                                                            str(self.num*self.incr), self.incr, self.bit_width)

@dataclass()
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
