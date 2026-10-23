import numpy as np

from src.bitstream import (
    validate_bitstream,
    bits_to_string,
    save_bitstream,
    load_bitstream
)

# Test 1: Convert bits -> string
bits = np.array([1, 0, 1, 1, 0, 0, 1, 0])

bit_string = bits_to_string(bits)

assert bit_string == "10110010"
print("Test 1 bits conversion: Passed!\n")

#Test 2: Reject invalid bits
try:
    validate_bitstream([0, 1, 2, 0])
except ValueError:
    print("Test 2 Reject invalid bit: Passed!\n")
else:
    raise AssertionError("Invalid bistream was not rejected\n")

#Test 3: Save and load bitstream
file_path = "results/data/test_bits.txt"

save_bitstream(bits, file_path)
loaded_bits = load_bitstream(file_path)

assert np.array_equal(bits, loaded_bits)
print("Test 3 Save and load bitstream: Passed!\n")

# Test 4: Reject empty bitstream
try:
    bits_to_string([])
except ValueError:
    print("Test 4 Reject empty bitstream: Passed!\n")
else:
    raise AssertionError("Empty bitstream was not rejected.\n")
