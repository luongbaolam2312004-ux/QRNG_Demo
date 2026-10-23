
import unittest

from src.quantum_simulator import simulate_measurements
from src.postprocessing import von_neumann_extract
from src.key_generator import generate_demo_key, generate_reference_key
from src.crypto_demo import encrypt_message, decrypt_message


class TestCryptoPipeline(unittest.TestCase):

    def setUp(self):
        self.message = "QRNG cryptography pipeline test"

    def test_demo_key_encryption_pipeline(self):
        # 1. Simulate raw bits
        raw_bits = simulate_measurements(
            n_bits=100_000,
            p_one=0.5,
            seed=42
        )

        # 2. Apply Von Neumann post-processing
        processed_bits = von_neumann_extract(raw_bits)

        # 3. Generate a 128-bit demonstration key
        key = generate_demo_key(
            processed_bits,
            key_bits=128
        )

        # 4. Encrypt the message
        nonce, ciphertext = encrypt_message(
            key,
            self.message
        )

        # 5. Decrypt the message
        decrypted = decrypt_message(
            key,
            nonce,
            ciphertext
        )

        # 6. Verify the result
        self.assertEqual(decrypted, self.message)

    def test_reference_key_encryption_pipeline(self):
        # 1. Generate a reference key using secrets
        key = generate_reference_key(key_bits=128)

        # 2. Encrypt the message
        nonce, ciphertext = encrypt_message(
            key,
            self.message
        )

        # 3. Decrypt the message
        decrypted = decrypt_message(
            key,
            nonce,
            ciphertext
        )

        # 4. Verify the result
        self.assertEqual(decrypted, self.message)


if __name__ == "__main__":
    unittest.main()
