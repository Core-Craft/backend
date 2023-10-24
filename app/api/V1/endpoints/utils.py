from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str):
    """
    Hashes a plaintext password using a secure cryptographic hash (bcrypt).

    Args:
        password (str): The plaintext password to be hashed.

    Returns:
        str: The hashed password as a string.

    Note:
    This function securely hashes the input password using the bcrypt hashing scheme.
    The recommended number of rounds for bcrypt is set to 12, which provides a good balance
    between security and computational cost. You can adjust the number of rounds to meet
    your specific security requirements.

    Example:
    >>> hashed = hash_password("my_secure_password")

    """
    return pwd_context.hash(password, rounds=12)


def verify_password(password: str):
    """
    Verifies a plaintext password against a previously hashed password using bcrypt.

    Args:
        password (str): The plaintext password to be verified.
        hashed_password (str): The previously hashed password to compare against.

    Returns:
        bool: True if the plaintext password matches the hashed password, False otherwise.

    Note:
    This function securely verifies a plaintext password against a previously hashed password using the bcrypt hashing scheme.


    Example:
    >>> hashed = hash_password("my_secure_password")
    >>> is_valid = verify_password("my_secure_password", hashed)

    """
    hashed_password = hash_password(password)
    return pwd_context.verify(password, hashed_password)
