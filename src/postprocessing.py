import numpy as np

from src.bitstream import validate_bitstream

#Su dung Von Neumann debiasing algorithm
"""
00 -> Loai
11 -> Loai
01 -> 0
10 -> 1
"""
def von_neumann_extract(bits) -> np.ndarray:
    array = validate_bitstream(bits)

    # Dung doi mot khong chong lap
    n_pairs = len(array) // 2
    pairs = array[: 2 * n_pairs].reshape(-1, 2)

    #Chi giu cac cap 2 bit khac nhau
    different_pairs = pairs[pairs[:, 0] != pairs[:, 1]]

    # 01 -> 0, 10 -> 1
    output_bits = different_pairs[:, 0]

    return output_bits.astype(np.uint8)