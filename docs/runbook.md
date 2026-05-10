# Research Runbook

## Scope

The first automation pass creates a minimal, reviewable execution-research artifact. The goal is not to optimize a trading strategy. The goal is to make the resume-backed claim inspectable through code, tests, and clear caveats.

## Approaches Considered

- Pulling current SPY/QQQ market data was rejected for this proof pass because live data introduces provider credentials, license constraints, and unstable test fixtures.
- Publishing real trade exports was rejected because account-level information is private and unnecessary for recruiter review.
- Adding a notebook was deferred because a dependency-free script and tests provide a smaller, more reliable verification surface.

## Model Notes

`twap` is the arithmetic mean of minute prices. `vwap` weights each minute price by displayed synthetic volume. The execution-price approximation applies a simple participation schedule across the observed bars. Implementation shortfall compares the estimated execution price with the arrival price and reports basis points.

## Verification

Run from the repository root:

```powershell
python -m unittest discover -s tests
python src\execution_lab.py data\synthetic_spy_minutes.csv --order-size 1200 --side buy
```

The test command is the authoritative regression check for this first proof point.

