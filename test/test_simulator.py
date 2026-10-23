import numpy as np
from quantum_simulator import simulate_measurements

# Test 1: Tao 1000 bits
bits = simulate_measurements(n_bits = 1000, seed = 42)

print("Test 1: Generate 1,000 bits")
print("="*20)
print("Number of bits:", len(bits))
print("First 20 bits:", bits[:20])
print("Unique values:", np.unique(bits))
print("="*20)
print("")

assert len(bits) == 1000
assert set(np.unique(bits)).issubset({0, 1})

# Test 2: Do tai lap
bits_a = simulate_measurements(n_bits=100, seed=123)
bits_b = simulate_measurements(n_bits=100, seed=123)

assert np.array_equal(bits_a, bits_b) # So sanh 2 day bit

print("Test 2: Reproducibility")
print("="*20)
print("Reproducibility test passed!\n")

# Test 3: Do do can bang
balanced_bits = simulate_measurements(
    n_bits=100_000,
    p_one=0.5,
    seed=42
)

ratio_one= np.mean(balanced_bits)

print("Test 3: Balanced source")
print("="*20)
print("Balanced source - ratio of 1:", ratio_one)
print("")

# Test 4: Do do thien vi
biased_bits = simulate_measurements(
    n_bits=100_000,
    p_one=0.5,
    seed=42
)

ratio_one_biased= np.mean(biased_bits)

print("Test 4: Biased source")
print("="*20)
print("Biased source - ratio of 1:", ratio_one_biased)
print("\n")


