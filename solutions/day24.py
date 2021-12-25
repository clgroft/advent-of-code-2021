"""An attempt at day 24.  It is far too slow."""


import re
from typing import Dict, List, Set, Tuple


INDEXES = {'w': 0, 'x': 1, 'y': 2, 'z': 3}


class ParseException(Exception): pass


class Instruction:
    def apply(self, state): pass


class InputInstruction(Instruction):
    def __init__(self, var):
        super().__init__()
        self._var = INDEXES[var]

    def apply(self, states):
        new_states = []
        for state, model_no in states:
            for i in range(9, 0, -1):
                s = list(state)
                s[self._var] = i
                new_states.append((tuple(s), model_no + str(i)))
        return new_states


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
        s = list(state)
        s[self._var] += self._const
        return tuple(s)


class AddVariableInstruction(VariableInstruction):
    def apply(self, state):
        s = list(state)
        s[self._var1] += state[self._var2]
        return tuple(s)


class MulConstantInstruction(ConstantInstruction):
    def apply(self, state):
        s = list(state)
        s[self._var] *= self._const
        return tuple(s)


class MulVariableInstruction(VariableInstruction):
    def apply(self, state):
        s = list(state)
        s[self._var1] *= state[self._var2]
        return tuple(s)


class DivConstantInstruction(ConstantInstruction):
    def apply(self, state):
        s = list(state)
        s[self._var] //= self._const
        return tuple(s)


class DivVariableInstruction(VariableInstruction):
    def apply(self, state):
        s = list(state)
        s[self._var1] //= state[self._var2]
        return tuple(s)


class ModConstantInstruction(ConstantInstruction):
    def apply(self, state):
        s = list(state)
        s[self._var] %= self._const
        return tuple(s)


class ModVariableInstruction(VariableInstruction):
    def apply(self, state):
        s = list(state)
        s[self._var1] %= state[self._var2]
        return tuple(s)


class EqlConstantInstruction(ConstantInstruction):
    def apply(self, state):
        s = list(state)
        s[self._var] = 1 if state[self._var] == self._const else 0
        return tuple(s)


class EqlVariableInstruction(VariableInstruction):
    def apply(self, state):
        s = list(state)
        s[self._var1] = 1 if state[self._var1] == state[self._var2] else 0
        return tuple(s)


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


def applyInstructionsToModelNumbers(
        instructions: List[Instruction],
        states: List[Tuple[Tuple[int, int, int, int], str]]):
    for instr in instructions:
        if isinstance(instr, InputInstruction):
            states = instr.apply(states)
            print(f'Expanded to {len(states)} states')
        else:
            states = [(instr.apply(s), model_no) for s, model_no in states]
            # Now collapse identical states together
            collapsed_states : List[Tuple[Tuple[int, int, int, int], str]] = []
            existing_states : Set[Tuple[int, int, int, int]] = set()
            for state, model_no in states:
                if state not in existing_states:
                    existing_states.add(state)
                    collapsed_states.append((state, model_no))
            # if len(collapsed_states) < len(states):
            print(f'Collapsed {len(states)} to {len(collapsed_states)}')
            states = collapsed_states
    return max(model_no for state, model_no in states if state[3] == 0)


def solution(day, lines):
    instructions = list(map(parseInstruction, lines))
    model_no = applyInstructionsToModelNumbers(instructions, [((0,0,0,0), '')])
    if model_no:
        print(f'Model number: {result}')
    else:
        print(f'No model number found')
