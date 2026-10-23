import numpy as np

from src.postprocessing import von_neumann_extract

#Test 1: Ktra tat ca 4 cap
input_bits = np.array([
    0, 0,
    0, 1,
    1, 1,
    1, 0
])

output_bits = von_neumann_extract(input_bits)

assert np.array_equal(output_bits, [0, 1])
print("Test 1 Passed!")

#Test 2: Tat ca cap duoc ktra
input_bits = np.array([0, 0, 1, 1, 0, 0])

output_bits = von_neumann_extract(input_bits)

assert len(output_bits) == 0
print("Test 2 passed")

#Test 3: Slg bit dau vao le
input_bits = np.array([0, 1, 1, 0, 1])

output_bits = von_neumann_extract(input_bits)

assert np.array_equal(output_bits, [0, 1])
print("Test 3 passed")

# Test 4: Loai dau vao khong hop le
try:
    von_neumann_extract([0, 1, 2, 0])
except ValueError:
    print("Test 4 passed")
else:
    raise print("Invalid input was not rejected")