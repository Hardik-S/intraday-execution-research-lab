import unittest
from pathlib import Path

from src.execution_lab import estimate_execution_price, load_bars, summarize_execution, twap, vwap


FIXTURE = Path(__file__).resolve().parents[1] / "data" / "synthetic_spy_minutes.csv"


class ExecutionLabTests(unittest.TestCase):
    def setUp(self) -> None:
        self.bars = load_bars(FIXTURE)

    def test_twap_uses_equal_time_weighting(self) -> None:
        self.assertAlmostEqual(twap(self.bars), 512.3566666667)

    def test_vwap_uses_volume_weighting(self) -> None:
        self.assertAlmostEqual(vwap(self.bars), 512.3673529412)

    def test_execution_summary_reports_shortfall(self) -> None:
        summary = summarize_execution(self.bars, order_size=1200, side="buy")
        self.assertEqual(summary["symbol"], "SPY")
        self.assertEqual(summary["order_size"], 1200)
        self.assertGreater(summary["implementation_shortfall_bps"], 0)

    def test_order_size_must_be_positive(self) -> None:
        with self.assertRaises(ValueError):
            estimate_execution_price(self.bars, 0)


if __name__ == "__main__":
    unittest.main()
