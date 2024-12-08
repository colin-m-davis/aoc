import os
import itertools
import functools
import operator


def parse(path):
    with open(path, 'r') as f:
        def parse_one(line):
            first_half, second_half = line.strip().split(': ')
            test_value = int(first_half)
            remaining_values = [int(word)
                                for word in second_half.strip().split(' ')]
            return (test_value, remaining_values)
        return [parse_one(line) for line in f.readlines()]


def solve(data):
    return sum(test_value for test_value, remaining_values in data if is_good(test_value, remaining_values))


def concatenate(a, b):
    return int(str(a) + str(b))


operators = [operator.add, operator.mul, concatenate]


def is_good(test_value, remaining_values):
    num_operators = len(remaining_values) - 1
    operator_sequences = itertools.product(operators, repeat=num_operators)
    return any(apply(remaining_values, sequence) == test_value for sequence in operator_sequences)


def apply(values, operators):
    assert (len(values) == len(operators) + 1)

    def accumulate(accum, item):
        x, op = item
        return op(accum, x)
    return functools.reduce(accumulate, zip(values[1:], operators), values[0])


input_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'input')
solution = solve(parse(input_path))
print(solution)
