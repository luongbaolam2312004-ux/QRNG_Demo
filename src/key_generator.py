import secrets

import numpy as np

from src.bitstream import validate_bitstream


def generate_demo_key(bits, key_bits = 128) -> bytes:
    # 1. Ktra dau vao
    if key_bits not in (128, 192, 256):
        raise ValueError("key_bits must be 128, 192 or 256")

    array = validate_bitstream(bits)

    # 2. Convert 128 bits -> 16 bytes
    if len(array) < key_bits:
        raise ValueError(
            f"Not enough bits: need {key_bits}, got {len(array)}"
        )

    #Select required number of bits
    selected_bits = array[:key_bits]

    # Pack every 8 bits into 1 bytes
    key_array = np.packbits(selected_bits, bitorder="big")

    # Convert the NumPy array to Python bytes
    key = key_array.tobytes()

    expected_bytes = key_bits //8

    if len(key) != expected_bytes:
        raise RuntimeError("Unexpected key length.")

    return key

def generate_reference_key(key_bits: int = 128) -> bytes:
    """
    Generate a reference key using Python's cryptographic RNG.
    """

    if key_bits not in (128, 192, 256):
        raise ValueError("key_bits must be 128, 192, or 256.")

    return secrets.token_bytes(key_bits // 8)
