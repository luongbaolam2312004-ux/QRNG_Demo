import numpy as np

from src.bitstream import validate_bitstream


def evaluate_bitstream(bits) -> dict:
    array = validate_bitstream(bits)
    n_bits = len(array)

    n_zeros = int(np.count_nonzero(array == 0))
    n_ones = int(np.count_nonzero(array == 1))

    p_zero = n_zeros / n_bits
    p_one = n_ones / n_bits

    # Shannon entropy của phân phối bit 0/1
    shannon_entropy = 0.0

    for probability in (p_zero, p_one):
        if probability > 0:
            shannon_entropy -= (
                probability * np.log2(probability)
            )

    # Min-entropy ước lượng từ tần suất biên
    max_probability = max(p_zero, p_one)
    estimated_min_entropy = -np.log2(max_probability)

    # Tương quan Pearson giữa các bit liền kề
    if n_bits < 2:
        adjacent_correlation = None
    else:
        left = array[:-1].astype(float)
        right = array[1:].astype(float)

        if np.std(left) == 0 or np.std(right) == 0:
            adjacent_correlation = None
        else:
            adjacent_correlation = float(
                np.corrcoef(left, right)[0, 1]
            )

    return {
        "n_bits": n_bits,
        "n_zeros": n_zeros,
        "n_ones": n_ones,
        "p_zero": p_zero,
        "p_one": p_one,
        "shannon_entropy": float(shannon_entropy),
        "estimated_min_entropy": float(
            estimated_min_entropy
        ),
        "adjacent_correlation": adjacent_correlation,
    }
