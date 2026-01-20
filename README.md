# pyO3 FFI array benchmark

This micro-benchmark mirrors ValuationEngine's `future_into_py` array return.

## Build and run

```sh
maturin develop
python bench.py --rounds 5 --count 10000
```
