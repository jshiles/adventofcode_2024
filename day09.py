import argparse
import sys
from collections.abc import Sequence
from typing import Optional, Union, NewType
from dataclasses import dataclass


@dataclass(frozen=True)
class File:
    fileno: int
    blocks: int


@dataclass(frozen=True)
class FreeSpace:
    blocks: int


Disk = NewType("Disk", list[Union[File, FreeSpace]])


def disk_to_checksum(disk: Disk) -> int:
    """Return the checksum, which is the sum of fileno * block position"""
    checksum = 0
    block_cnt = 0
    for x in disk:
        if isinstance(x, FreeSpace):
            block_cnt += x.blocks
        else:
            for _ in range(x.blocks):
                checksum += x.fileno * block_cnt
                block_cnt += 1

    return checksum


def disk_to_string(disk: Disk) -> str:
    """Returns a string representation of the disk, like in the example."""
    string = ""
    for x in disk:
        if isinstance(x, File):
            string += str(x.fileno) * x.blocks
        else:
            string += "." * x.blocks
    return string


def swap(disk: Disk, fs_idx: int, file_idx: int) -> Disk:
    """
    Takes a disk and two positions to swap, one file and one freespace. If the
    file is smaller than the freespace, only part of the freespace will be taken.
    Return modified Diskspace.
    """
    if disk[fs_idx].blocks == disk[file_idx].blocks:
        disk[fs_idx] = disk[file_idx]
        disk[file_idx] = FreeSpace(disk[fs_idx].blocks)
    elif disk[fs_idx].blocks > disk[file_idx].blocks:
        file = disk[file_idx]
        new_freespace = FreeSpace(disk[fs_idx].blocks - file.blocks)
        disk[file_idx] = FreeSpace(file.blocks)
        disk = disk[:fs_idx] + [file, new_freespace] + disk[fs_idx + 1 :]
    else:
        raise ValueError("Cannot swap File larger than freespace.")

    return disk


def defragment_whole_files(checksum: list[int]) -> Disk:
    """
    Builds disk from checksum. Returns defragmented disk.
    """
    # Build disk object
    disk: Disk = []
    fileno = 0
    for idx, val in enumerate(checksum):
        if idx % 2 == 0:
            disk.append(File(fileno, val))
            fileno += 1
        else:
            disk.append(FreeSpace(val))

    # Defragment disk object.
    defragged_disk: Disk = disk
    for i in range(len(defragged_disk) - 1, -1, -1):
        if isinstance(defragged_disk[i], File):
            file = defragged_disk[i]
            for j in range(len(defragged_disk)):
                if (
                    isinstance(defragged_disk[j], FreeSpace)
                    and defragged_disk[j].blocks >= file.blocks
                    and i > j
                ):
                    defragged_disk = swap(defragged_disk, j, i)
                    break

    return defragged_disk


def parse_input(path: str) -> list[int]:
    with open(path, "r") as file:
        numbers = list(map(int, file.read().strip()))
    return numbers


def parse_args(argv: Optional[Sequence[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", "-f", help="input file", required=True, type=str)
    return parser.parse_args(argv)


def main(argv: Optional[Sequence[str]] = None) -> None:
    """
    https://adventofcode.com/2024/day/9
    """
    args = parse_args(argv)
    nums = parse_input(args.file)

    defragged_disk = defragment_whole_files(nums)
    checksum = disk_to_checksum(defragged_disk)
    print(f"Part 2: {checksum}")


if __name__ == "__main__":
    main(sys.argv[1:])
