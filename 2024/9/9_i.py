import os
from collections import defaultdict
import functools
import itertools


def parse(path):
    with open(path, 'r') as f:
        return [int(digit) for digit in f.readline().strip()]


def solve(lengths):
    final_disk_state = move_file_blocks(decompress_into_disk_format(lengths))
    assert (all(x != None for x in final_disk_state))
    return sum(index * file_id_number for index, file_id_number in enumerate(final_disk_state))


def decompress_into_disk_format(lengths):
    file_id_number = -1
    result = []
    pen = None
    for i, length in enumerate(lengths):
        if i % 2 == 0:
            # File block
            file_id_number += 1
            pen = file_id_number
        else:
            pen = None
        for _ in range(length):
            result.append(pen)
    return result


def move_file_blocks(d):
    disk = d[::]
    left_free_space_index = 0
    right_file_block_index = len(disk) - 1
    while left_free_space_index < right_file_block_index:
        while left_free_space_index in range(len(disk)) and disk[left_free_space_index] != None:
            left_free_space_index += 1
        while right_file_block_index in range(len(disk)) and disk[right_file_block_index] == None:
            right_file_block_index -= 1
        if left_free_space_index >= right_file_block_index:
            break
        disk[left_free_space_index] = disk[right_file_block_index]
        disk[right_file_block_index] = None
    return disk[:left_free_space_index]


input_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'input')
solution = solve(parse(input_path))
print(solution)
