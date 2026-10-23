
import numpy as np

def simulate_measurements(
    n_bits: int, # So bit can tao
    p_one: float = 0.5, # Xsuat xhien bit 1, default = 0.5
    seed: int | None = None # Cho phep dat seed de lap lai ket qua
) -> np.ndarray: # Du kien tra ra np.ndarray
    # 1. Ktra so bit
    if isinstance(n_bits, bool) or not isinstance(n_bits, (int, np.integer)):
        raise TypeError("n_bits must be an integer.")

    if n_bits <= 0:
        raise ValueError("n_bits must be greater than 0.")

    # 2. Ktra xsuat
    if not isinstance(p_one, (int, float, np.integer, np.floating)):
        raise TypeError("p_one must be a number.")

    if not np.isfinite(p_one) or not 0 <= p_one <= 1:
        raise ValueError("p_one must be between 0 and 1.")

    # 3. Tao 1 trinh so ngau nhien
    rng = np.random.default_rng(seed) # Tao seed ngau nhien

    # 4. Mo phong dau ra cua phep do luong
    # Neu p_one = 0.5 --> val => 0.5 -> val = 0, val < 0.5 -> val = 1 
    random_values = rng.random(n_bits) # Tao day so ngau nhien
    bits = (random_values < p_one).astype(np.uint8)

    # 5. Tra ra ket qua bit da bien doi
    return bits
