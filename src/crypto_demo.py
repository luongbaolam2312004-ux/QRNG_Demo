
import secrets

from cryptography.hazmat.primitives.ciphers.aead import AESGCM


def _validate_key(key: bytes) -> None:
    """Kiểm tra độ dài khóa AES."""
    if not isinstance(key, bytes):
        raise TypeError("Key must be bytes.")

    if len(key) not in (16, 24, 32):
        raise ValueError("AES key must be 16, 24, or 32 bytes.")


def encrypt_message(
    key: bytes,
    plaintext: str,
    associated_data: bytes | None = None,
) -> tuple[bytes, bytes]:
    """
    Mã hóa thông điệp bằng AES-GCM.

    Returns:
        nonce, ciphertext (ciphertext có kèm authentication tag).
    """
    _validate_key(key)

    if not isinstance(plaintext, str):
        raise TypeError("Plaintext must be a string.")

    if associated_data is not None and not isinstance(associated_data, bytes):
        raise TypeError("Associated data must be bytes or None.")

    # Nonce 12 bytes: không cần bí mật nhưng phải duy nhất
    # cho mỗi lần mã hóa bằng cùng một khóa.
    nonce = secrets.token_bytes(12)

    aesgcm = AESGCM(key)
    ciphertext = aesgcm.encrypt(
        nonce,
        plaintext.encode("utf-8"),
        associated_data,
    )

    return nonce, ciphertext


def decrypt_message(
    key: bytes,
    nonce: bytes,
    ciphertext: bytes,
    associated_data: bytes | None = None,
) -> str:
    """Giải mã và xác thực thông điệp bằng AES-GCM."""
    _validate_key(key)

    if not isinstance(nonce, bytes) or len(nonce) != 12:
        raise ValueError("Nonce must be exactly 12 bytes.")

    if not isinstance(ciphertext, bytes):
        raise TypeError("Ciphertext must be bytes.")

    if associated_data is not None and not isinstance(associated_data, bytes):
        raise TypeError("Associated data must be bytes or None.")

    aesgcm = AESGCM(key)
    plaintext = aesgcm.decrypt(nonce, ciphertext, associated_data)

    return plaintext.decode("utf-8")
