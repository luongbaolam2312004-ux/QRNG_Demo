
import json
from datetime import datetime, timezone
from pathlib import Path


def save_report(report: dict, file_path: str) -> None:
    """Save an experiment report as a JSON file."""
    if not isinstance(report, dict):
        raise TypeError("report must be a dictionary.")

    path = Path(file_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("w", encoding="utf-8") as file:
        json.dump(
            report,
            file,
            indent=4,
            ensure_ascii=False,
            allow_nan=False,
        )


def create_experiment_report(
    config: dict,
    raw_stats: dict,
    processed_stats: dict,
    processed_bits_count: int,
    demo_key_bits: int,
    demo_aes_passed: bool,
    reference_aes_passed: bool,
) -> dict:
    """Create a structured report for a QRNG simulation experiment."""
    raw_count = raw_stats["n_bits"]

    if raw_count <= 0:
        raise ValueError("raw_stats['n_bits'] must be greater than zero.")

    if not 0 <= processed_bits_count <= raw_count:
        raise ValueError(
            "processed_bits_count must be between 0 and raw bit count."
        )

    return {
        "experiment": {
            "name": "QRNG Simulation for Cryptographic Key Generation",
            "timestamp_utc": datetime.now(timezone.utc).isoformat(),
            "source_type": (
                "NumPy pseudorandom simulation; "
                "not a physical quantum random source"
            ),
        },
        "configuration": config,
        "raw_bitstream": raw_stats,
        "postprocessing": {
            "method": "Von Neumann extractor",
            "input_bits": raw_count,
            "output_bits": processed_bits_count,
            "retention_ratio": processed_bits_count / raw_count,
            "output_statistics": processed_stats,
        },
        "cryptography": {
            "algorithm": "AES-GCM",
            "demo_key_size_bits": demo_key_bits,
            "demo_encryption_roundtrip": demo_aes_passed,
            "reference_encryption_roundtrip": reference_aes_passed,
            "security_note": (
                "Successful encryption does not establish that the "
                "simulated demo key has sufficient cryptographic entropy."
            ),
        },
    }
