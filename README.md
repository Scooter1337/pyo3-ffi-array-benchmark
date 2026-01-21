# pyO3 FFI array benchmark

This micro-benchmark mirrors ValuationEngine's `future_into_py` array return.

## Build and run

```sh
maturin develop
python bench.py --rounds 5 --count 10000 --format bytes
```

`--format bytes` uses a packed `u64` byte buffer (faster) while `--format list`
returns a Python list of integers (baseline).

`--mode sync` benchmarks a synchronous Rust call; `--mode async` (default)
benchmarks the `future_into_py` path.
