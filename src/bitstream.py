from pathlib import Path

import numpy as np

# 1. Ktra dau vao
    # Dau vao nen la 1 chieu, co phan tu, chi chua 1 bit 1 va 0
def validate_bitstream(bits) -> np.ndarray:
    array = np.asarray(bits) # Chuyen input data -> NumPy array

    if array.ndim != 1:
        raise ValueError("Bitstream must be one-dimensional.")
    if array.size == 0:
        raise ValueError("Bitstream must not be empty.")
    # np.isin(array, [0, 1]) : Ktra tung phan tu thuoc {0, 1} khong
    # np.all(): Ktra tat ca cac phan tu co thoa man khong
    if not np.all(np.isin(array, [0, 1])):
        raise ValueError("Bitstream can contain only 0 and 1.") # raise ValueError(..): Bao loi neu data khong hop le

    return array.astype(np.uint8)

# 2. Chuyen doi bit array -. str chi co 0 va 1
def bits_to_string(bits) -> str:
    array = validate_bitstream(bits)

    # array.astype(str) : convert bit -> string
    # "".join(..): ghep chung lai ma khong dau phan cach
    return "".join(array.astype(str)) 

# 3. Luu luong bits thanh text file
def save_bitstream(bits, file_path: str) -> None:
    bit_string = bits_to_string(bits)
    path = Path(file_path)# dai dien cho path cua file

    path.parent.mkdir(parents=True,exist_ok=True) # Tao thu muc cha neu chua ton tai
    path.write_text(bit_string + "\n", encoding="utf-8") # ghi chuoi bit vao tep

# 4. Tai 1 luong bits tu text file
def load_bitstream(file_path: str) ->np.ndarray:
    path = Path(file_path)
    bit_string = path.read_text(encoding="utf-8").strip()

    if not bit_string:
        raise ValueError("Bitstream file is empty!")

    if any(char not in "01" for char in bit_string):
        raise ValueError("File contains characters other than 0 and 1.")

    return np.fromiter(
        (int(char) for char in bit_string),
        dtype=np.uint8
    )