import argparse
import csv
import json
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class MinuteBar:
    timestamp: str
    symbol: str
    price: float
    volume: int


def load_bars(path: Path) -> list[MinuteBar]:
    with path.open(newline="", encoding="utf-8") as handle:
        rows = csv.DictReader(handle)
        bars = [
            MinuteBar(
                timestamp=row["timestamp"],
                symbol=row["symbol"],
                price=float(row["price"]),
                volume=int(row["volume"]),
            )
            for row in rows
        ]

    if not bars:
        raise ValueError("At least one minute bar is required.")
    return bars


def twap(bars: list[MinuteBar]) -> float:
    return sum(bar.price for bar in bars) / len(bars)


def vwap(bars: list[MinuteBar]) -> float:
    total_volume = sum(bar.volume for bar in bars)
    if total_volume <= 0:
        raise ValueError("Total volume must be positive.")
    return sum(bar.price * bar.volume for bar in bars) / total_volume


def estimate_execution_price(bars: list[MinuteBar], order_size: int) -> float:
    if order_size <= 0:
        raise ValueError("Order size must be positive.")

    # This intentionally simple schedule makes the first proof deterministic:
    # participate equally across bars until the synthetic order is filled.
    remaining = order_size
    filled_value = 0.0
    filled_size = 0
    per_bar_target = max(1, order_size // len(bars))

    for bar in bars:
        if remaining <= 0:
            break
        fill = min(remaining, per_bar_target, bar.volume)
        filled_value += fill * bar.price
        filled_size += fill
        remaining -= fill

    if remaining > 0:
        last_bar = bars[-1]
        filled_value += remaining * last_bar.price
        filled_size += remaining

    return filled_value / filled_size


def summarize_execution(bars: list[MinuteBar], order_size: int, side: str) -> dict[str, float | int | str]:
    arrival_price = bars[0].price
    execution_price = estimate_execution_price(bars, order_size)
    direction = 1 if side == "buy" else -1
    shortfall_bps = direction * ((execution_price - arrival_price) / arrival_price) * 10_000

    return {
        "symbol": bars[0].symbol,
        "bars": len(bars),
        "order_size": order_size,
        "side": side,
        "arrival_price": round(arrival_price, 4),
        "twap": round(twap(bars), 4),
        "vwap": round(vwap(bars), 4),
        "estimated_execution_price": round(execution_price, 4),
        "implementation_shortfall_bps": round(shortfall_bps, 4),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Summarize synthetic intraday execution quality.")
    parser.add_argument("csv_path", type=Path)
    parser.add_argument("--order-size", type=int, default=1000)
    parser.add_argument("--side", choices=("buy", "sell"), default="buy")
    args = parser.parse_args()

    bars = load_bars(args.csv_path)
    print(json.dumps(summarize_execution(bars, args.order_size, args.side), indent=2))


if __name__ == "__main__":
    main()

