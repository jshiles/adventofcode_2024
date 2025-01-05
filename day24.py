from __future__ import annotations
import argparse
import sys
from dataclasses import dataclass, field
from collections.abc import Sequence
from enum import Enum
from functools import cache
from typing import Optional, FrozenSet, Tuple, TypeAlias


class GateType(Enum):
    AND = "AND"
    OR = "OR"
    XOR = "XOR"


@dataclass(frozen=True)
class _GateBase:
    name: str

    @cache
    def evaluate(self, gates: GateStorage) -> bool:
        raise NotImplemented


GateStorage: TypeAlias = FrozenSet[Tuple[str, _GateBase]]


@dataclass(frozen=True)
class FixedGate(_GateBase):
    output: bool

    @cache
    def evaluate(self, gates: GateStorage) -> bool:
        return self.output


@dataclass(frozen=True)
class LogicGate(_GateBase):
    gate_type: GateType
    inputs: frozenset[str] = field(default_factory=frozenset)

    @cache
    def evaluate(self, gates: GateStorage) -> bool:
        input_values = [
            gate.evaluate(gates) for name, gate in gates if name in self.inputs
        ]

        if self.gate_type == GateType.AND:
            return all(input_values)
        elif self.gate_type == GateType.OR:
            return any(input_values)
        elif self.gate_type == GateType.XOR:
            return sum(input_values) % 2 == 1
        else:
            raise ValueError(f"Unknown gate type: {self.gate_type}")


def parse_gates_from_file(filename: str) -> frozenset[tuple[str, _GateBase]]:
    gates = []

    with open(filename, "r") as file:
        lines = file.readlines()

    # Process FixedGates
    for line in lines:
        line = line.strip()
        if not line or "->" in line:
            break
        name, value = line.split(":")
        gates.append((name.strip(), FixedGate(name.strip(), bool(int(value.strip())))))

    # Process LogicGates
    for line in lines:
        line = line.strip()
        if "->" not in line:
            continue
        parts = line.split("->")
        inputs, output = parts[0].strip(), parts[1].strip()
        input1, gate_type, input2 = inputs.split(" ")
        gate_enum = GateType[gate_type.strip()]
        gates.append((output, LogicGate(output, gate_enum, frozenset({input1, input2}))))

    return frozenset(gates)


def parse_args(argv: Optional[Sequence[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", "-f", help="input file", required=True, type=str)
    return parser.parse_args(argv)


def main(argv: Optional[Sequence[str]] = None) -> None:
    """https://adventofcode.com/2024/day/23"""

    args = parse_args(argv)
    gates = parse_gates_from_file(args.file)

    binary = [
        str(int(gate.evaluate(gates)))
        for name, gate in sorted(gates, key=lambda x: x[0], reverse=True)
        if name.startswith("z")
    ]
    print(f"Part 1: {int(''.join(binary), 2)} <- {binary}")


if __name__ == "__main__":
    main(sys.argv[1:])


# gates: dict[str, _GateBase] = {}
# gates["x00"] = FixedGate("x00", True)
# gates["x01"] = FixedGate("x01", True)
# gates["x02"] = FixedGate("x02", True)
# gates["y00"] = FixedGate("y00", False)
# gates["y01"] = FixedGate("y01", True)
# gates["y02"] = FixedGate("y02", False)

# gates["z00"] = LogicGate("z00", GateType.AND, [gates["x00"], gates["y00"]])
# gates["z01"] = LogicGate("z01", GateType.XOR, [gates["x01"], gates["y01"]])
# gates["z02"] = LogicGate("z02", GateType.OR, [gates["x02"], gates["y02"]])
# assert gates["z00"].evaluate() == False
# assert gates["z01"].evaluate() == False
# assert gates["z02"].evaluate() == True
