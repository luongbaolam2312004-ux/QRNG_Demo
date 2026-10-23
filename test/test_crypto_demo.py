
import unittest

from cryptography.exceptions import InvalidTag

from src.crypto_demo import encrypt_message, decrypt_message


class TestCryptoDemo(unittest.TestCase):

    def test_encrypt_decrypt_roundtrip(self):
        key = bytes(range(16))
        message = "QRNG project - AES-GCM test"

        nonce, ciphertext = encrypt_message(key, message)
        decrypted = decrypt_message(key, nonce, ciphertext)

        self.assertEqual(decrypted, message)

    def test_modified_ciphertext_is_rejected(self):
        key = bytes(range(16))
        nonce, ciphertext = encrypt_message(key, "Test message")

        modified = bytearray(ciphertext)
        modified[0] ^= 1

        with self.assertRaises(InvalidTag):
            decrypt_message(key, nonce, bytes(modified))

    def test_wrong_key_is_rejected(self):
        key1 = bytes(range(16))
        key2 = bytes(range(1, 17))

        nonce, ciphertext = encrypt_message(key1, "Test message")

        with self.assertRaises(InvalidTag):
            decrypt_message(key2, nonce, ciphertext)

    def test_invalid_key_length_is_rejected(self):
        with self.assertRaises(ValueError):
            encrypt_message(b"short", "Test message")


if __name__ == "__main__":
    unittest.main()
