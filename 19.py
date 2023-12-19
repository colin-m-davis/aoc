# AoC 2023, day 19

from functools import reduce
from copy import deepcopy

start = 'in'
accept = 'A'
reject = 'R'
sep = ':'
lt = '<'
gt = '>'
categories = ['x', 'm', 'a', 's']
lb, ub = 1, 4000

def parse_workflow(line):
    split_index = line.index('{')
    name = line[:split_index]
    chunks = line[split_index+1:-1].split(',')
    def parse_chunk(chunk):
        if sep not in chunk: return chunk
        assert(lt in chunk or gt in chunk)
        comp_index = chunk.index(lt) if lt in chunk else chunk.index(gt)
        dest_index = chunk.index(sep)
        return {
            'category': chunk[:comp_index],
            'operator': chunk[comp_index],
            'comparand': int(chunk[comp_index+1:dest_index]),
            'destination': chunk[dest_index+1:]
        }
    return (name, [parse_chunk(chunk) for chunk in chunks])

def parse_part(line):
    chunks = line[1:-1].split(',')
    def parse_chunk(chunk):
        split_index = chunk.index('=')
        return (chunk[:split_index], int(chunk[split_index+1:]))
    ratings = [parse_chunk(chunk) for chunk in chunks]
    return {rating[0]: rating[1] for rating in ratings}

def parse(path):
    f = open(path)
    lines = [line.strip() for line in f.readlines()]
    split_index = lines.index('')
    unprocessed_workflows = map(parse_workflow, lines[:split_index])
    workflows = reduce(lambda acc, x: {**acc, x[0]: x[1]}, unprocessed_workflows, {})
    parts = [parse_part(line) for line in lines[split_index+1:]]
    return (workflows, parts)

# part 1

def process(part, workflows):
    def evaluate(part, dest):
        if dest == accept: return True
        elif dest == reject: return False
        else: return consider(part, dest)
    def consider(part, wf_name):
        steps = workflows[wf_name]
        for step in steps[:-1]:
            category = step['category']
            operator = step['operator']
            comparand = step['comparand']
            destination = step['destination']
            actual = part[category]
            result = eval(' '.join([str(actual), operator, str(comparand)]))
            if result: return evaluate(part, destination)
        return evaluate(part, steps[-1])
    return consider(part, start)

def solve1(path):
    workflows, parts = parse(path)
    return sum(sum(part.values()) if process(part, workflows) else 0 for part in parts)

# part 2

def is_impossible(ranges):
    return any(map(lambda x: x[0] > x[1], ranges.values()))

def combinations(ranges):
    if is_impossible(ranges): return 0
    return reduce(lambda acc, x: acc * x, [b[1] - b[0] + 1 for b in ranges.values()], 1)

def update_range(ranges, category, op, comp):
    cur_lb, cur_ub = ranges[category]
    new_ranges = deepcopy(ranges)
    new_ranges[category] = (cur_lb, comp - 1) if op == lt else (comp + 1, cur_ub)
    return new_ranges

def dfs(workflows, workflow_name, ranges):
    if workflow_name == accept: return combinations(ranges)
    if workflow_name == reject: return 0
    def process_step(step, cur_ranges):
        category = step['category']
        operator = step['operator']
        comparand = step['comparand']
        destination = step['destination']
        result = 0
        cond_holds_ranges = update_range(cur_ranges, category, operator, comparand)
        result = 0 if is_impossible(cond_holds_ranges) else dfs(workflows, destination, cond_holds_ranges)
        other_operator = gt if operator == lt else lt
        other_comparand = comparand + 1 if other_operator == lt else comparand - 1
        cond_fails_ranges = update_range(cur_ranges, category, other_operator, other_comparand)
        return (result, cond_fails_ranges)
    total = 0
    cur_ranges = deepcopy(ranges)
    steps = workflows[workflow_name]
    for step in steps[:-1]:
        options, new_ranges = process_step(step, cur_ranges)
        total += options
        cur_ranges = new_ranges
    total += dfs(workflows, steps[-1], cur_ranges)
    return total

def solve2(path):
    workflows, _ = parse(path)
    all = {category: (lb, ub) for category in categories}
    return dfs(workflows, start, all)

parts = [1, 2]
solve_map = {1: solve1, 2: solve2}

path = 'input'
for part in parts:
    result = solve_map[part](path)
    print(f'part {part}: {result}')
