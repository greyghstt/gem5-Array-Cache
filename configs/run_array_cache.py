import argparse
from pathlib import Path

from gem5.components.boards.simple_board import SimpleBoard
from gem5.components.cachehierarchies.classic.no_cache import NoCache
from gem5.components.cachehierarchies.classic.private_l1_cache_hierarchy import (
    PrivateL1CacheHierarchy,
)
from gem5.components.cachehierarchies.classic.private_l1_private_l2_cache_hierarchy import (
    PrivateL1PrivateL2CacheHierarchy,
)
from gem5.components.memory.single_channel import SingleChannelDDR3_1600
from gem5.components.processors.cpu_types import CPUTypes
from gem5.components.processors.simple_processor import SimpleProcessor
from gem5.isas import ISA
from gem5.resources.resource import BinaryResource
from gem5.simulate.simulator import Simulator


def build_cache_hierarchy(cache_name: str):
    if cache_name == "nocache":
        return NoCache()

    if cache_name == "l1_16k":
        return PrivateL1CacheHierarchy(
            l1d_size="16KiB",
            l1i_size="16KiB",
        )

    if cache_name == "l1_32k":
        return PrivateL1CacheHierarchy(
            l1d_size="32KiB",
            l1i_size="32KiB",
        )

    if cache_name == "l1_l2":
        return PrivateL1PrivateL2CacheHierarchy(
            l1d_size="32KiB",
            l1i_size="32KiB",
            l2_size="256KiB",
        )

    raise ValueError(f"Unknown cache configuration: {cache_name}")


parser = argparse.ArgumentParser()

parser.add_argument("--binary", required=True)
parser.add_argument("--mode", required=True, choices=["seq", "stride", "random"])
parser.add_argument("--cache", required=True, choices=["nocache", "l1_16k", "l1_32k", "l1_l2"])
parser.add_argument("--size", default="131072")
parser.add_argument("--repeats", default="8")
parser.add_argument("--stride", default="16")
parser.add_argument("--clk", default="3GHz")
parser.add_argument("--mem-size", default="256MiB")

args = parser.parse_args()

binary_path = Path(args.binary).resolve()

if not binary_path.exists():
    raise FileNotFoundError(f"Binary not found: {binary_path}")

cache_hierarchy = build_cache_hierarchy(args.cache)

memory = SingleChannelDDR3_1600(args.mem_size)

processor = SimpleProcessor(
    cpu_type=CPUTypes.TIMING,
    isa=ISA.X86,
    num_cores=1,
)

board = SimpleBoard(
    clk_freq=args.clk,
    processor=processor,
    memory=memory,
    cache_hierarchy=cache_hierarchy,
)

binary = BinaryResource(local_path=str(binary_path), architecture=ISA.X86)

board.set_se_binary_workload(
    binary,
    arguments=[
        args.mode,
        str(args.size),
        str(args.repeats),
        str(args.stride),
    ],
)

print("Experiment configuration:")
print(f"  binary : {binary_path}")
print(f"  mode   : {args.mode}")
print(f"  cache  : {args.cache}")
print(f"  size   : {args.size}")
print(f"  repeats: {args.repeats}")
print(f"  stride : {args.stride}")
print(f"  clk    : {args.clk}")
print(f"  memory : {args.mem_size}")

simulator = Simulator(board=board)
simulator.run()
