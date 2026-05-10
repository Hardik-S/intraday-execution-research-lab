# Intraday Execution Research Lab

Synthetic intraday execution research package for demonstrating TWAP/VWAP analysis without publishing broker exports, paid market data, or investment recommendations.

## Recruiter Proof Point

This repository turns a resume claim about SPY/QQQ intraday execution research into a reproducible artifact:

- Synthetic minute bars live in `data/synthetic_spy_minutes.csv`.
- The model in `src/execution_lab.py` computes TWAP, VWAP, and implementation shortfall.
- Unit tests in `tests/test_execution_lab.py` validate the calculations against known values.
- `docs/runbook.md` explains assumptions, rejected approaches, and verification commands.

## Boundary Decisions

The repository intentionally uses synthetic data. Real broker fills, paid data, account balances, strategy parameters, and personal trade history are excluded because they would distract from the engineering proof and create unnecessary disclosure risk.

The calculations are educational. They are not financial advice, a live trading strategy, or a claim that the sample data represents real liquidity.

## Quick Start

```powershell
python -m unittest discover -s tests
python src\execution_lab.py data\synthetic_spy_minutes.csv --order-size 1200 --side buy
```

Expected output is a JSON summary with TWAP, VWAP, arrival price, execution price, and shortfall in basis points.

## File Structure

- `data/`: small synthetic fixtures that make the repository reviewable without credentials.
- `src/`: dependency-free Python code so the verifier runs on a clean machine.
- `tests/`: deterministic tests for the calculation surface.
- `docs/`: rationale and operating notes for future expansion.

