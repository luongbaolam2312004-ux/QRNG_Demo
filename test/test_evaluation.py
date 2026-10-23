
import numpy as np

from src.evaluation import evaluate_bitstream
from src.quantum_simulator import simulate_measurements


# Test 1: A perfectly balanced bitstream
result = evaluate_bitstream([0, 1, 0, 1])

assert result["n_bits"] == 4
assert result["n_zeros"] == 2
assert result["n_ones"] == 2
assert np.isclose(result["shannon_entropy"], 1.0)
assert np.isclose(result["estimated_min_entropy"], 1.0)

print("Test 1 passed: balanced bitstream\n")


# Test 2: A completely biased bitstream
result = evaluate_bitstream([1, 1, 1, 1])

assert result["p_one"] == 1.0
assert result["p_zero"] == 0.0
assert np.isclose(result["shannon_entropy"], 0.0)
assert np.isclose(result["estimated_min_entropy"], 0.0)
assert result["adjacent_correlation"] is None

print("Test 2 passed: constant bitstream\n")


# Test 3: Simulated balanced source
bits = simulate_measurements(
    n_bits=100_000,
    p_one=0.5,
    seed=42
)

result = evaluate_bitstream(bits)

print("\nBalanced source:")
for name, value in result.items():
    print(f"{name}: {value}")
print("\n")

# Test 4: Simulated biased source
bits = simulate_measurements(
    n_bits=100_000,
    p_one=0.6,
    seed=42
)

result = evaluate_bitstream(bits)

print("\nBiased source:")
for name, value in result.items():
    print(f"{name}: {value}")

assert abs(result["p_one"] - 0.6) < 0.01

print("\nAll evaluation tests passed!\n")
