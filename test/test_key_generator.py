
import numpy as np

from src.key_generator import (
    generate_demo_key,
    generate_reference_key,
)


# Test 1: Generate an AES-128 demonstration key
bits = np.tile([0, 1], 64)

key = generate_demo_key(bits, key_bits=128)

assert isinstance(key, bytes)
assert len(key) == 16

print("Test 1 passed: AES-128 key length =", len(key), "bytes")


# Test 2: Generate AES-256 demonstration key
bits_256 = np.tile([0, 1], 128)

key_256 = generate_demo_key(bits_256, key_bits=256)

assert len(key_256) == 32

print("Test 2 passed: AES-256 key length =", len(key_256), "bytes")


# Test 3: Reject insufficient input
try:
    generate_demo_key([0, 1, 0, 1], key_bits=128)
except ValueError:
    print("Test 3 passed: insufficient bits rejected")
else:
    raise AssertionError("Insufficient input was not rejected")


# Test 4: Generate a reference key
reference_key = generate_reference_key(128)

assert isinstance(reference_key, bytes)
assert len(reference_key) == 16

print("Test 4 passed: reference key length =", len(reference_key), "bytes")


print("All key generator tests passed!")
