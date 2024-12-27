import os
from dataclasses import dataclass
from typing import List
from collections import deque, defaultdict
from operator import and_, or_, xor


@dataclass
class Gate:
    wire_in_a: str
    wire_in_b: str
    wire_out: str
    operation: str
    is_processed = False


def parse(path: str):
    with open(path, 'r') as f:
        lines = list(map(lambda line: line.strip(), f.readlines()))
        break_point = lines.index("")
        first_half, second_half = lines[:break_point], lines[break_point + 1:]

        def parse_initial_value(line: str):
            wire, value = line.split(": ")
            return (wire, int(value))
        initial_values = list(map(parse_initial_value, first_half))

        def parse_gate(line: str):
            wire_in_a, operation, wire_in_b, _, wire_out = line.split(' ')
            return Gate(wire_in_a, wire_in_b, wire_out, operation)
        gates = list(map(parse_gate, second_half))

        return (initial_values, gates)


def solve(input: tuple[List[tuple[str, int]], List[Gate]]):

    initial_values, gates = input
    values = defaultdict()
    for wire, value in initial_values:
        values[wire] = value
    while True:
        gates_processed = 0
        for gate in gates:
            if gate.is_processed:
                continue
            if gate.wire_in_a in values and gate.wire_in_b in values:
                result = operate(values[gate.wire_in_a],
                                 values[gate.wire_in_b],
                                 gate.operation)
                values[gate.wire_out] = result
                gate.is_processed = True
                gates_processed += 1
        if gates_processed == 0:
            break
    z_wire_value_pairs = list(reversed(sorted((wire, value)
                                              for wire, value in values.items() if wire[0] == 'z')))
    binary_string = ''.join(str(value) for _, value in z_wire_value_pairs)
    return int(binary_string, 2)


def operate(value_a: int, value_b: int, operation: str):
    if operation == "AND":
        return value_a & value_b
    if operation == "OR":
        return value_a | value_b
    if operation == "XOR":
        return value_a ^ value_b
    raise Exception(f"Unrecognized operation {operation}")


input_path = os.path.join(os.path.dirname(
    os.path.realpath(__file__)), 'input')
solution = solve(parse(input_path))
print(solution)
