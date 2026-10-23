from src.quantum_simulator import simulate_measurements
from src.postprocessing import von_neumann_extract
import numpy as np

raw_bits = simulate_measurements(
    n_bits=100_000,
    p_one=0.5,
    seed=42,
)

processed_bits = von_neumann_extract(raw_bits)


def check_correlation(bits):
    left = bits[:-1].astype(float)
    right = bits[1:].astype(float)

    return np.corrcoef(left, right)[0, 1]


print("Raw correlation:", check_correlation(raw_bits))
print("Processed correlation:", check_correlation(processed_bits))