import os
from datetime import datetime, timedelta
from typing import Any, Union

from dotenv import load_dotenv
from jose import jwt
from passlib.context import CryptContext

load_dotenv()
ACCESS_TOKEN_EXPIRE_MINUTES = 30  # 30 minutes
REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # 7 days
ALGORITHM = "HS256"
JWT_SECRET_KEY = os.environ["JWT_SECRET_KEY"]  # should be kept secret
JWT_REFRESH_SECRET_KEY = os.environ["JWT_REFRESH_SECRET_KEY"]  # should be kept secret

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


def verify_password(password: str, hashed_password: str):
    """
    Verifies a plaintext password against a previously hashed password using bcrypt.

    Args:
        password (str): The plaintext password to be verified.

    Returns:
        bool: True if the plaintext password matches the hashed password, False otherwise.

    Note:
    This function securely verifies a plaintext password against a previously hashed password using the bcrypt hashing scheme.


    Example:
    >>> is_valid = verify_password("my_secure_password", hashed_password)

    """
    return pwd_context.verify(password, hashed_password)


def create_access_token(subject: Union[str, Any], expires_delta: int = None) -> str:
    """
    Create an access token for the specified subject.

    This function generates a JSON Web Token (JWT) access token for the given subject, typically representing a user or client. The token is signed with the secret key and includes an expiration time.

    Args:
        subject (Union[str, Any]): The subject for which the access token is created. This can be a user ID, username, or any relevant subject identifier.

        expires_delta (int, optional): The expiration time of the token in seconds. If not provided, it defaults to the value defined by ACCESS_TOKEN_EXPIRE_MINUTES (in minutes).

    Returns:
        str: The generated JWT access token as a string.

    Note:
        The function uses the JWT_SECRET_KEY and ALGORITHM constants for signing the token and configuring the algorithm. The expiration time of the token can be specified directly or calculated based on the number of minutes defined by ACCESS_TOKEN_EXPIRE_MINUTES.
    """
    if expires_delta is not None:
        expires_delta = datetime.utcnow() + expires_delta
    else:
        expires_delta = datetime.utcnow() + timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES
        )

    to_encode = {"exp": expires_delta, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, ALGORITHM)
    return encoded_jwt


def create_refresh_token(subject: Union[str, Any], expires_delta: int = None) -> str:
    """
    Create a refresh token for the specified subject.

    This function generates a JSON Web Token (JWT) refresh token for the given subject, typically representing a user or client. The token is signed with the refresh token secret key and includes an expiration time.

    Args:
        subject (Union[str, Any]): The subject for which the refresh token is created. This can be a user ID, username, or any relevant subject identifier.

        expires_delta (int, optional): The expiration time of the token in seconds. If not provided, it defaults to the value defined by REFRESH_TOKEN_EXPIRE_MINUTES (in minutes).

    Returns:
        str: The generated JWT refresh token as a string.

    Note:
        The function uses the JWT_REFRESH_SECRET_KEY and ALGORITHM constants for signing the token and configuring the algorithm. The expiration time of the token can be specified directly or calculated based on the number of minutes defined by REFRESH_TOKEN_EXPIRE_MINUTES.
    """
    if expires_delta is not None:
        expires_delta = datetime.utcnow() + expires_delta
    else:
        expires_delta = datetime.utcnow() + timedelta(
            minutes=REFRESH_TOKEN_EXPIRE_MINUTES
        )

    to_encode = {"exp": expires_delta, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, JWT_REFRESH_SECRET_KEY, ALGORITHM)
    return encoded_jwt
