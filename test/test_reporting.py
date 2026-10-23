
import json
import math
import tempfile
import unittest
from pathlib import Path

from src.reporting import create_experiment_report, save_report


class TestReporting(unittest.TestCase):

    def setUp(self):
        self.config = {
            "n_bits": 1000,
            "p_one": 0.5,
            "seed": 42,
            "key_size_bits": 128,
        }

        self.raw_stats = {
            "n_bits": 1000,
            "n_zeros": 510,
            "n_ones": 490,
            "p_zero": 0.51,
            "p_one": 0.49,
            "shannon_entropy": 0.9997,
            "estimated_min_entropy": 0.9714,
            "adjacent_correlation": 0.01,
        }

        self.processed_stats = {
            "n_bits": 240,
            "n_zeros": 120,
            "n_ones": 120,
            "p_zero": 0.5,
            "p_one": 0.5,
            "shannon_entropy": 1.0,
            "estimated_min_entropy": 1.0,
            "adjacent_correlation": 0.0,
        }

        self.report = create_experiment_report(
            config=self.config,
            raw_stats=self.raw_stats,
            processed_stats=self.processed_stats,
            processed_bits_count=240,
            demo_key_bits=128,
            demo_aes_passed=True,
            reference_aes_passed=True,
        )

    def test_create_experiment_report(self):
        self.assertEqual(
            self.report["experiment"]["name"],
            "QRNG Simulation for Cryptographic Key Generation",
        )
        self.assertEqual(
            self.report["postprocessing"]["output_bits"],
            240,
        )
        self.assertAlmostEqual(
            self.report["postprocessing"]["retention_ratio"],
            0.24,
        )
        self.assertTrue(
            self.report["cryptography"]["demo_encryption_roundtrip"]
        )
        self.assertTrue(
            self.report["cryptography"]["reference_encryption_roundtrip"]
        )

    def test_save_and_load_json_report(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            report_path = Path(temp_dir) / "experiment_report.json"

            save_report(self.report, str(report_path))

            self.assertTrue(report_path.exists())

            with report_path.open("r", encoding="utf-8") as file:
                loaded_report = json.load(file)

            self.assertEqual(
                loaded_report["postprocessing"]["output_bits"],
                240,
            )
            self.assertEqual(
                loaded_report["cryptography"]["algorithm"],
                "AES-GCM",
            )

    def test_reject_non_dictionary_report(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            report_path = Path(temp_dir) / "report.json"

            with self.assertRaises(TypeError):
                save_report([], str(report_path))

    def test_reject_nan_in_report(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            report_path = Path(temp_dir) / "report.json"

            with self.assertRaises(ValueError):
                save_report({"invalid_value": math.nan}, str(report_path))

    def test_reject_zero_raw_bits(self):
        with self.assertRaises(ValueError):
            create_experiment_report(
                config=self.config,
                raw_stats={"n_bits": 0},
                processed_stats=self.processed_stats,
                processed_bits_count=0,
                demo_key_bits=128,
                demo_aes_passed=True,
                reference_aes_passed=True,
            )


if __name__ == "__main__":
    unittest.main()
