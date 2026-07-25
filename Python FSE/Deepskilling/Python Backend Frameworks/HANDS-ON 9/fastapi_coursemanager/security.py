"""
HANDS-ON 9 - password hashing & JWT helpers.

Why bcrypt over MD5/SHA-256 for passwords:
MD5 and SHA-256 are designed to be FAST, which is exactly what makes them
weak for passwords - an attacker with a stolen hash database can try
billions of guesses per second on commodity GPUs. bcrypt has a tunable
"work factor" that deliberately makes each hash slow (and salts
automatically), so brute-forcing becomes computationally expensive even
at scale.
"""
from datetime import datetime, timedelta, timezone
from passlib.context import CryptContext
from jose import jwt, JWTError

SECRET_KEY = 'dev-secret-change-me-in-production'  # move to env var in real deployments
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({'exp': expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def decode_access_token(token: str) -> dict:
    """Raises jose.JWTError if the token is invalid or expired."""
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
