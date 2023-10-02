from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str):
    """
    Hashes a plaintext password using a secure cryptographic hash.

    Args:
        password (str): The plaintext password to be hashed.

    Returns:
        str: The hashed password as a string.

    Note:
        This function uses the bcrypt hashing scheme for password hashing.
    """
    return pwd_context.hash(password)


def verify_password(password: str, hashed_password: str):
    """
    Verifies a plaintext password against a hashed password.

    Args:
        password (str): The plaintext password to be verified.
        hashed_password (str): The previously hashed password to compare against.

    Returns:
        bool: True if the plaintext password matches the hashed password, False otherwise.

    Note:
        This function uses the bcrypt hashing scheme for password verification.
    """
    return pwd_context.verify(password, hashed_password)
