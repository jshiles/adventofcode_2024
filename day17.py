import argparse
import sys
from collections.abc import Sequence
from typing import Optional
from dataclasses import dataclass, field


@dataclass
class Computer:
    reg_a: int
    reg_b: int
    reg_c: int
    instr_ptr: int = field(default=0)

    def reset_registers(self, a: int = 0, b: int = 0, c: int = 0) -> None:
        self.reg_a = a
        self.reg_b = b
        self.reg_c = c


def evaluate_operand(c: Computer, operand: int) -> int:
    """
    Return the evaluation of the operand according to the rules.
    :param c: Computer
    :param operand: int
    :returns: int
    """
    match operand:
        case 0 | 1 | 2 | 3:
            # Combo operands 0 through 3 represent literal values 0 through 3.
            return operand
        case 4:
            # Combo operand 4 represents the value of register A.
            return c.reg_a
        case 5:
            # Combo operand 5 represents the value of register B.
            return c.reg_b
        case 6:
            # Combo operand 6 represents the value of register C.
            return c.reg_c
        case _:
            # Combo operand 7 is reserved and will not appear in valid programs.
            raise ValueError(f"{operand} not valid.")


def evaluate_step(c: Computer, opcode: int, operand: int) -> Optional[int]:
    """
    Given a computer and a opcode / operand pair, update the computer and
    optionally return a value.
    :param c: Computer
    :param opcode: int
    :param operand: int
    :returns: Optional[int] a return value if there is one
    """

    match opcode:
        # The adv instruction (opcode 0) performs division. The numerator is the
        # value in the A register. The denominator is found by raising 2 to the
        # power of the instruction's combo operand. (So, an operand of 2 would
        # divide A by 4 (2^2); an operand of 5 would divide A by 2^B.) The result
        # of the division operation is truncated to an integer and then written
        # to the A register.
        case 0:
            c.reg_a = c.reg_a // 2 ** evaluate_operand(c, operand)
            return

        # The bxl instruction (opcode 1) calculates the bitwise XOR of register B
        # and the instruction's literal operand, then stores the result in
        # register B.
        case 1:
            c.reg_b = c.reg_b ^ operand
            return

        # The bst instruction (opcode 2) calculates the value of its combo operand
        # modulo 8 (thereby keeping only its lowest 3 bits), then writes that value
        # to the B register.
        case 2:
            c.reg_b = evaluate_operand(c, operand) % 8
            return

        # The jnz instruction (opcode 3) does nothing if the A register is 0.
        # However, if the A register is not zero, it jumps by setting the instruction
        # pointer to the value of its literal operand; if this instruction jumps, the
        # instruction pointer is not increased by 2 after this instruction.
        case 3:
            if c.reg_a != 0:
                c.instr_ptr = evaluate_operand(c, operand) - 2
            return

        # The bxc instruction (opcode 4) calculates the bitwise XOR of register B and
        # register C, then stores the result in register B. (For legacy reasons, this
        # instruction reads an operand but ignores it.)
        case 4:
            c.reg_b = c.reg_b ^ c.reg_c
            return

        # The out instruction (opcode 5) calculates the value of its combo operand
        # modulo 8, then outputs that value. (If a program outputs multiple values,
        # they are separated by commas.)
        case 5:
            return evaluate_operand(c, operand) % 8

        # The bdv instruction (opcode 6) works exactly like the adv instruction except
        # that the result is stored in the B register. (The numerator is still read
        # from the A register.)
        case 6:
            c.reg_b = c.reg_a // 2 ** evaluate_operand(c, operand)
            return

        # The cdv instruction (opcode 7) works exactly like the adv instruction except
        # that the result is stored in the C register. (The numerator is still read
        # from the A register.)
        case 7:
            c.reg_c = c.reg_a // 2 ** evaluate_operand(c, operand)
            return


def run_program(computer: Computer, program: list[int]) -> list[int]:
    """
    Given a computer, and it's preset registers, return the output values of
    the program.
    :param computer: Computer.
    :param program: list[int] list of operands and opcodes.
    :returns: list[int]
    """
    output_vals = []
    while computer.instr_ptr < len(program):
        val = evaluate_step(
            computer, program[computer.instr_ptr], program[computer.instr_ptr + 1]
        )
        if val is not None:
            output_vals.append(val)
        computer.instr_ptr += 2

    return output_vals


def find_a(program: list[int]) -> int:
    """
    Finds an register_a value that will produce the same output as input.
    :param program: list[int] which is our program
    :returns: int
    """

    def _recurse(a: int = 0, depth: int = 0) -> Optional[int]:
        if depth == len(target):
            return a

        for i in range(8):
            output = run_program(Computer(a * 8 + i, 0, 0), program)
            if len(output) and output[0] == target[depth]:
                if result := _recurse((a * 8 + i), depth + 1):
                    return result

    target = program[::-1]
    reg_a = _recurse()
    return reg_a if reg_a is not None else 0


def parse_input(file_path: str) -> tuple[Computer, list[int]]:
    register_a = register_b = register_c = 0
    program = []

    with open(file_path, "r") as file:
        for line in file:
            line = line.strip()
            if line.startswith("Register A:"):
                register_a = int(line.split(":")[1].strip())
            elif line.startswith("Register B:"):
                register_b = int(line.split(":")[1].strip())
            elif line.startswith("Register C:"):
                register_c = int(line.split(":")[1].strip())
            elif line.startswith("Program:"):
                program = [int(x) for x in line.split(":")[1].strip().split(",")]

    return Computer(register_a, register_b, register_c), program


def parse_args(argv: Optional[Sequence[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", "-f", help="input file", required=True, type=str)
    return parser.parse_args(argv)


def main(argv: Optional[Sequence[str]] = None) -> None:
    """
    https://adventofcode.com/2024/day/17
    """

    args = parse_args(argv)

    # If register C contains 9, the program 2,6 would set register B to 1.
    comp = Computer(0, 0, 9)
    _ = run_program(comp, [2, 6])
    assert comp.reg_b == 1

    # If register A contains 10, the program 5,0,5,1,5,4 would output 0,1,2.
    comp = Computer(10, 0, 0)
    assert run_program(comp, [5, 0, 5, 1, 5, 4]) == [0, 1, 2]

    # If register A contains 2024, the program 0,1,5,4,3,0 would output 4,2,5,6,7,7,7,7,3,1,0 and leave 0 in register A.
    comp = Computer(2024, 0, 0)
    assert run_program(comp, [0, 1, 5, 4, 3, 0]) == [4, 2, 5, 6, 7, 7, 7, 7, 3, 1, 0]
    assert comp.reg_a == 0

    # If register B contains 29, the program 1,7 would set register B to 26.
    comp = Computer(0, 29, 0)
    _ = run_program(comp, [1, 7])
    assert comp.reg_b == 26

    # If register B contains 2024 and register C contains 43690, the program 4,0 would set register B to 44354.
    comp = Computer(0, 2024, 43690)
    _ = run_program(comp, [4, 0])
    assert comp.reg_b == 44354

    # Example from the website's text
    comp = Computer(729, 0, 0)
    assert run_program(comp, [0, 1, 5, 4, 3, 0]) == [4, 6, 3, 5, 6, 3, 5, 2, 1, 0]

    computer, program = parse_input(args.file)
    result = run_program(computer, program)
    print("Part 1: " + ",".join([str(x) for x in result]))

    computer, program = parse_input(args.file)
    reg_a = find_a(program)
    assert run_program(Computer(reg_a, 0, 0), program) == program
    print(f"Part 2: {reg_a}")


if __name__ == "__main__":
    main(sys.argv[1:])
