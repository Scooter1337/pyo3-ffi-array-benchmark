import argparse
import asyncio
import statistics
import time
from array import array
import sys

import pyo3_ffi_array_benchmark as bench


def _fmt_ns(value_ns: int) -> str:
    return f"{value_ns / 1_000:.2f}us"


def _percentile(sorted_values, pct: float) -> int:
    if not sorted_values:
        return 0
    idx = int((len(sorted_values) - 1) * pct)
    return sorted_values[idx]


async def run_async(rounds: int, count: int, fmt: str) -> None:
    for i in range(rounds):
        start_ns = time.time_ns()
        if fmt == "bytes":
            payload = await bench.await_timestamps_bytes(count)
            timestamps = array("Q")
            timestamps.frombytes(payload)
            if sys.byteorder != "little":
                timestamps.byteswap()
        else:
            timestamps = await bench.await_timestamps(count)
        recv_ns = time.time_ns()
        latencies = [recv_ns - ts for ts in timestamps]
        latencies.sort()
        mean_ns = int(statistics.mean(latencies)) if latencies else 0
        p50 = _percentile(latencies, 0.50)
        p95 = _percentile(latencies, 0.95)
        p99 = _percentile(latencies, 0.99)
        total_ns = recv_ns - start_ns
        print(
            f"round={i + 1} count={count} total={_fmt_ns(total_ns)} "
            f"min={_fmt_ns(latencies[0]) if latencies else '0.00us'} "
            f"p50={_fmt_ns(p50)} p95={_fmt_ns(p95)} p99={_fmt_ns(p99)} "
            f"max={_fmt_ns(latencies[-1]) if latencies else '0.00us'} "
            f"mean={_fmt_ns(mean_ns)}"
        )

def run_sync(rounds: int, count: int, fmt: str) -> None:
    for i in range(rounds):
        start_ns = time.time_ns()
        if fmt == "bytes":
            payload = bench.timestamps_bytes(count)
            timestamps = array("Q")
            timestamps.frombytes(payload)
            if sys.byteorder != "little":
                timestamps.byteswap()
        else:
            timestamps = bench.timestamps(count)
        recv_ns = time.time_ns()
        latencies = [recv_ns - ts for ts in timestamps]
        latencies.sort()
        mean_ns = int(statistics.mean(latencies)) if latencies else 0
        p50 = _percentile(latencies, 0.50)
        p95 = _percentile(latencies, 0.95)
        p99 = _percentile(latencies, 0.99)
        total_ns = recv_ns - start_ns
        print(
            f"round={i + 1} count={count} total={_fmt_ns(total_ns)} "
            f"min={_fmt_ns(latencies[0]) if latencies else '0.00us'} "
            f"p50={_fmt_ns(p50)} p95={_fmt_ns(p95)} p99={_fmt_ns(p99)} "
            f"max={_fmt_ns(latencies[-1]) if latencies else '0.00us'} "
            f"mean={_fmt_ns(mean_ns)}"
        )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--rounds", type=int, default=5)
    parser.add_argument("--count", type=int, default=10_000)
    parser.add_argument("--format", choices=("list", "bytes"), default="bytes")
    parser.add_argument("--mode", choices=("async", "sync"), default="async")
    args = parser.parse_args()
    if args.mode == "sync":
        run_sync(args.rounds, args.count, args.format)
    else:
        asyncio.run(run_async(args.rounds, args.count, args.format))


if __name__ == "__main__":
    main()
