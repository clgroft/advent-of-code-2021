"""An attempt at day 24.  It is far too slow."""


import re
import sympy as sp


INDEXES = {'w': 0, 'x': 1, 'y': 2, 'z': 3}
INPUT_CTR = 0
INPUT_VARS = {
    0: 2,
    1: 7,
    2: 1,
    3: 4,
    4: 1,
    5: 1,
    6: 9,
    7: 1,
    8: 2,
    9: 1,
    10: 3,
    11: 9,
    12: 1,
    13: 1,
}

EQL_CTR = 0
EQL_VARS = {
    # After getting symbolic expressions for some of the equality expressions,
    # it becomes clear that many of them have specific values that sympy cannot
    # calculate.  Those values are stored here.
    0: 0,
    1: 1,
    2: 0,
    3: 1,
    4: 0,
    5: 1,
    8: 0,
    9: 1,
    10: 0,
    11: 1,
    12: 0,
    13: 1,
    18: 0,
    19: 1,

    # Vary these as part of narrowing down number
    # 6: 1,
    7: 0,
    # 14: 1,
    15: 0,
    # 16: 1,
    17: 0,
    # 20: 1,
    21: 0,
    # 22: 0,
    23: 0,
    # 24: 0,
    25: 0,
    # 26: 1,
    27: 0, # this HAS to be true for any solution
}


class ParseException(Exception): pass


class Instruction:
    def apply(self, state): pass


class InputInstruction(Instruction):
    def __init__(self, var):
        super().__init__()
        self._var = INDEXES[var]

    def apply(self, state):
        global INPUT_CTR, INPUT_VARS
        fixed_input = INPUT_VARS.get(INPUT_CTR)
        if fixed_input is not None:
            state[self._var] = fixed_input
        else:
            new_symbol = sp.Symbol(f'i_{INPUT_CTR}', integer=True)
            state[self._var] = new_symbol
            print(f'{new_symbol} ranges from 1 to 9')
        INPUT_CTR += 1


class ConstantInstruction(Instruction):
    def __init__(self, var, const):
        super().__init__()
        self._var, self._const = INDEXES[var], const


class VariableInstruction(Instruction):
    def __init__(self, var1, var2):
        super().__init__()
        self._var1, self._var2 = INDEXES[var1], INDEXES[var2]


class AddConstantInstruction(ConstantInstruction):
    def apply(self, state):
        state[self._var] += self._const
        # state[self._var] = sp.simplify(state[self._var])


class AddVariableInstruction(VariableInstruction):
    def apply(self, state):
        state[self._var1] += state[self._var2]
        # state[self._var1] = sp.simplify(state[self._var1])


class MulConstantInstruction(ConstantInstruction):
    def apply(self, state):
        state[self._var] *= self._const
        # state[self._var] = sp.simplify(state[self._var])


class MulVariableInstruction(VariableInstruction):
    def apply(self, state):
        state[self._var1] *= state[self._var2]
        # state[self._var1] = sp.simplify(state[self._var1])


class DivConstantInstruction(ConstantInstruction):
    def apply(self, state):
        state[self._var] //= self._const
        # state[self._var] = sp.simplify(state[self._var])


class DivVariableInstruction(VariableInstruction):
    def apply(self, state):
        state[self._var1] //= state[self._var2]
        # state[self._var1] = sp.simplify(state[self._var1])


class ModConstantInstruction(ConstantInstruction):
    def apply(self, state):
        state[self._var] %= self._const
        # state[self._var] = sp.simplify(state[self._var])


class ModVariableInstruction(VariableInstruction):
    def apply(self, state):
        state[self._var1] %= state[self._var2]
        # state[self._var1] = sp.simplify(state[self._var1])


class EqlConstantInstruction(ConstantInstruction):
    def apply(self, state):
        global EQL_CTR, EQL_VARS
        fixed_result = EQL_VARS.get(EQL_CTR)
        if fixed_result is not None:
            state[self._var] = fixed_result
        else:
            new_symbol = sp.Symbol(f'v_{EQL_CTR}', integer=True)
            print(f'{new_symbol} is 1 if {state[self._var]} = {self._const}, o.w. 0')
            state[self._var] = new_symbol
        EQL_CTR += 1


class EqlVariableInstruction(VariableInstruction):
    def apply(self, state):
        global EQL_CTR, EQL_VARS
        fixed_result = EQL_VARS.get(EQL_CTR)
        if fixed_result is not None:
            state[self._var1] = fixed_result
        else:
            new_symbol = sp.Symbol(f'v_{EQL_CTR}', integer=True)
            print(f'{new_symbol} is 1 if {state[self._var1]} = {state[self._var2]}, o.w. 0')
            state[self._var1] = new_symbol
        EQL_CTR += 1


INPUT_RE = re.compile('^inp (.)$')
OTHER_INSTRUCTION_RE = re.compile('^(.*?) (.*?) (.*)$')

def parseInstruction(line):
    m = INPUT_RE.match(line)
    if m:
        return InputInstruction(m.group(1))
    m = OTHER_INSTRUCTION_RE.match(line)
    if not m:
        raise ParseException()
    instruction, var, arg = m.group(1), m.group(2), m.group(3)
    varArg = arg in INDEXES.keys()
    if not varArg:
        arg = int(arg)
    if instruction == 'add':
        return (AddVariableInstruction(var, arg) if varArg
                else AddConstantInstruction(var, arg))
    if instruction == 'mul':
        return (MulVariableInstruction(var, arg) if varArg
                else MulConstantInstruction(var, arg))
    if instruction == 'div':
        return (DivVariableInstruction(var, arg) if varArg
                else DivConstantInstruction(var, arg))
    if instruction == 'mod':
        return (ModVariableInstruction(var, arg) if varArg
                else ModConstantInstruction(var, arg))
    if instruction == 'eql':
        return (EqlVariableInstruction(var, arg) if varArg
                else EqlConstantInstruction(var, arg))
    raise ParseException()


def solution(day, lines):
    instructions = list(map(parseInstruction, lines))
    state = [0,0,0,0]
    for instr in instructions:
        instr.apply(state)
    print(f'Want {state[INDEXES["z"]]} = 0')
