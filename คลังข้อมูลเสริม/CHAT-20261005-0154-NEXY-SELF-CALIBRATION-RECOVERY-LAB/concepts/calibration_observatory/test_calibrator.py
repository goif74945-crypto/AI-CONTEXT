from __future__ import annotations

import unittest

from concepts.calibration_observatory.calibrator import PredictionRecord, calibration_report


class CalibrationObservatoryTests(unittest.TestCase):
    def test_overconfidence_detected(self) -> None:
        rows = [PredictionRecord(f"r{i:02d}", 0.9, i < 10, "E2") for i in range(20)]
        r = calibration_report(rows, min_records=20, gap_threshold=0.1)
        self.assertEqual(r["status"], "SYSTEMATIC_OVERCONFIDENCE")
        self.assertGreater(r["signed_calibration_bias"], 0.1)

    def test_underconfidence_detected(self) -> None:
        rows = [PredictionRecord(f"r{i:02d}", 0.2, i < 18, "E3") for i in range(20)]
        r = calibration_report(rows, min_records=20, gap_threshold=0.1)
        self.assertEqual(r["status"], "SYSTEMATIC_UNDERCONFIDENCE")

    def test_small_sample_not_promoted(self) -> None:
        rows = [PredictionRecord("a", 0.9, True, "E2")]
        self.assertEqual(calibration_report(rows, min_records=5)["status"], "NOT_ENOUGH_DATA")

    def test_no_data_explicit(self) -> None:
        self.assertEqual(calibration_report([])["status"], "NO_DATA")

    def test_order_independent(self) -> None:
        rows = [
            PredictionRecord("a", 0.8, True, "E2"),
            PredictionRecord("b", 0.2, False, "E2"),
        ]
        self.assertEqual(calibration_report(rows), calibration_report(reversed(rows)))

    def test_invalid_probability_rejected(self) -> None:
        with self.assertRaises(ValueError):
            PredictionRecord("x", 1.1, True, "E2")


if __name__ == "__main__":
    unittest.main()
