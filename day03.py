import argparse
import re
import sys
from collections.abc import Sequence
from typing import Optional


def instruction_stream_simple(stream: str) -> int:
    """
    Read all mul(X,Y) where X and Y are 1 to 3 digit numbers, and return the
    sum of the all functions.
    """
    sum_result = 0
    pattern = r'\w{3}\(\d{1,3},\d{1,3}\)'
    matches = re.findall(pattern, stream)
    for mem_instr in matches:
        if mem_instr.startswith('mul'):
            num1, num2 = map(int, mem_instr[4:-1].split(','))
            sum_result += num1 * num2
    return sum_result


def instruction_stream(stream: str) -> int:
    """
    Read all mul(X,Y), do(), and don't() functions where X and Y are 1 to 3
    digit numbers, and return the sum of the all functions that are enabled.
    Do enables the following functions. Don't() disables the following
    functions.
    """
    sum_result = 0
    pattern = r"\w{3}\(\d{1,3},\d{1,3}\)|do\(\)|don't\(\)"
    matches = re.findall(pattern, stream)
    evaluate_instruction = True
    for mem_instr in matches:
        if mem_instr == "do()":
            evaluate_instruction = True
        elif mem_instr == "don't()":
            evaluate_instruction = False
        elif evaluate_instruction and mem_instr.startswith('mul'):
            num1, num2 = map(int, mem_instr[4:-1].split(','))
            sum_result += num1 * num2
    return sum_result


def read_mem_rows(file_path: str) -> str:
    with open(file_path, 'r') as file:
        return file.read()


def parse_args(argv: Optional[Sequence[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", "-f", help="input file", required=True, type=str)
    return parser.parse_args(argv)


def main(argv: Optional[Sequence[str]] = None) -> None:
    """
    https://adventofcode.com/2024/day/3
    """
    args = parse_args(argv)
    instructions = read_mem_rows(args.file)
    sum_result = instruction_stream_simple(instructions)
    print(f"Part 1 -> {sum_result}")
    sum_result = instruction_stream(instructions)
    print(f"Part 2 -> {sum_result}")


if __name__ == "__main__":
    main(sys.argv[1:])
