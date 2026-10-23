from pathlib import Path
from pprint import pprint

from src.quantum_simulator import simulate_measurements
from src.bitstream import save_bitstream, load_bitstream
from src.evaluation import evaluate_bitstream
from src.postprocessing import von_neumann_extract
from src.key_generator import generate_demo_key, generate_reference_key
from src.crypto_demo import encrypt_message, decrypt_message
from src.reporting import create_experiment_report, save_report


# ============================================================
# CONFIGURATION
# ============================================================

N_BITS = 100_000
P_ONE = 0.5
SEED = 42
KEY_BITS = 128

MESSAGE = "QRNG simulation and AES-GCM demonstration"

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"

RAW_BITS_PATH = DATA_DIR / "raw_bits.txt"
PROCESSED_BITS_PATH = DATA_DIR / "processed_bits.txt"
REPORT_PATH = DATA_DIR / "experiment_report.json"


def main():
    print("=" * 60)
    print("QRNG SIMULATION AND CRYPTOGRAPHY DEMO")
    print("=" * 60)

    DATA_DIR.mkdir(parents=True, exist_ok=True)

    # --------------------------------------------------------
    # 1. SIMULATE RAW BITSTREAM
    # --------------------------------------------------------
    print("\n[1] Simulating raw bitstream...")

    raw_bits = simulate_measurements(
        n_bits=N_BITS,
        p_one=P_ONE,
        seed=SEED,
    )

    print(f"Raw bits generated: {len(raw_bits)}")

    save_bitstream(raw_bits, str(RAW_BITS_PATH))
    loaded_raw_bits = load_bitstream(str(RAW_BITS_PATH))

    if not (raw_bits == loaded_raw_bits).all():
        raise RuntimeError("Raw bitstream verification failed.")

    print(f"Raw bitstream saved and verified: {RAW_BITS_PATH}")

    # --------------------------------------------------------
    # 2. EVALUATE RAW BITSTREAM
    # --------------------------------------------------------
    print("\n[2] Evaluating raw bitstream...")

    raw_stats = evaluate_bitstream(loaded_raw_bits)
    pprint(raw_stats)

    # --------------------------------------------------------
    # 3. VON NEUMANN POST-PROCESSING
    # --------------------------------------------------------
    print("\n[3] Applying Von Neumann post-processing...")

    processed_bits = von_neumann_extract(loaded_raw_bits)

    print(f"Processed bits: {len(processed_bits)}")

    save_bitstream(processed_bits, str(PROCESSED_BITS_PATH))
    loaded_processed_bits = load_bitstream(str(PROCESSED_BITS_PATH))

    if not (processed_bits == loaded_processed_bits).all():
        raise RuntimeError("Processed bitstream verification failed.")

    print(f"Processed bitstream saved and verified: {PROCESSED_BITS_PATH}")

    # --------------------------------------------------------
    # 4. EVALUATE PROCESSED BITSTREAM
    # --------------------------------------------------------
    print("\n[4] Evaluating processed bitstream...")

    processed_stats = evaluate_bitstream(loaded_processed_bits)
    pprint(processed_stats)

    # --------------------------------------------------------
    # 5. GENERATE DEMONSTRATION AND REFERENCE KEYS
    # --------------------------------------------------------
    print("\n[5] Generating demonstration and reference keys...")

    demo_key = generate_demo_key(
        loaded_processed_bits,
        key_bits=KEY_BITS,
    )

    reference_key = generate_reference_key(
        key_bits=KEY_BITS,
    )

    print(f"Demo key length: {len(demo_key)} bytes")
    print(f"Reference key length: {len(reference_key)} bytes")

    # --------------------------------------------------------
    # 6. TEST AES-GCM WITH DEMONSTRATION KEY
    # --------------------------------------------------------
    print("\n[6] Testing AES-GCM with the demo key...")

    nonce, ciphertext = encrypt_message(demo_key, MESSAGE)
    decrypted = decrypt_message(demo_key, nonce, ciphertext)

    demo_aes_passed = decrypted == MESSAGE

    print(f"Ciphertext length: {len(ciphertext)} bytes")
    print(f"Decryption successful: {demo_aes_passed}")

    if not demo_aes_passed:
        raise RuntimeError("Demo-key AES-GCM roundtrip failed.")

    # --------------------------------------------------------
    # 7. TEST AES-GCM WITH REFERENCE KEY
    # --------------------------------------------------------
    print("\n[7] Testing AES-GCM with the reference key...")

    ref_nonce, ref_ciphertext = encrypt_message(
        reference_key,
        MESSAGE,
    )

    ref_decrypted = decrypt_message(
        reference_key,
        ref_nonce,
        ref_ciphertext,
    )

    reference_aes_passed = ref_decrypted == MESSAGE

    print(f"Decryption successful: {reference_aes_passed}")

    if not reference_aes_passed:
        raise RuntimeError("Reference-key AES-GCM roundtrip failed.")

    # --------------------------------------------------------
    # 8. CREATE AND SAVE EXPERIMENT REPORT
    # --------------------------------------------------------
    print("\n[8] Creating experiment report...")

    report = create_experiment_report(
        config={
            "n_bits": N_BITS,
            "p_one": P_ONE,
            "seed": SEED,
            "key_size_bits": KEY_BITS,
        },
        raw_stats=raw_stats,
        processed_stats=processed_stats,
        processed_bits_count=len(processed_bits),
        demo_key_bits=KEY_BITS,
        demo_aes_passed=demo_aes_passed,
        reference_aes_passed=reference_aes_passed,
    )

    save_report(report, str(REPORT_PATH))

    print(f"Experiment report saved: {REPORT_PATH}")

    # --------------------------------------------------------
    # 9. FINAL SUMMARY
    # --------------------------------------------------------
    print("\n" + "=" * 60)
    print("PIPELINE COMPLETED")
    print("=" * 60)

    print(f"Raw bits: {len(raw_bits)}")
    print(f"Processed bits: {len(processed_bits)}")
    print(f"Key size: {KEY_BITS} bits")
    print(f"AES-GCM demo: {'PASS' if demo_aes_passed else 'FAIL'}")
    print(
        "AES-GCM reference: "
        f"{'PASS' if reference_aes_passed else 'FAIL'}"
    )
    print(f"Report: {REPORT_PATH}")

    print("\nIMPORTANT:")
    print(
        "The bitstream is generated by NumPy pseudorandom simulation, "
        "not by a physical quantum random source."
    )
    print(
        "Successful AES-GCM encryption does not prove that the "
        "demonstration key is cryptographically secure."
    )


if __name__ == "__main__":
    main()
