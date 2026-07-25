"""
HANDS-ON 9 - Task 1 & 2: registration, JWT login, protected routes.

OAuth2 Authorization Code flow (concept) vs. this simple JWT login:
The Authorization Code flow is the standard OAuth2 flow for third-party
login (e.g. "Sign in with Google"). The user is redirected to the
provider's login page, the provider redirects back with a short-lived
`code`, and the backend exchanges that code (server-to-server, with a
client secret) for an access token - the app never sees the user's
password. Our `/auth/login/` endpoint is a simpler "Resource Owner
Password" style flow: the client sends email+password directly to our
own API and we issue a JWT ourselves. That's fine for a first-party app
we control, but unsuitable for letting users log in via a third party.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from database import get_db
from models import User
from auth_schemas import UserRegister, UserLogin, Token, UserOut
from security import get_password_hash, verify_password, create_access_token

router = APIRouter(prefix='/api/v1/auth', tags=['Auth'])


@router.post('/register/', response_model=UserOut, status_code=status.HTTP_201_CREATED)
async def register(payload: UserRegister, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.email == payload.email))
    if result.scalar_one_or_none() is not None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Email already registered')

    user = User(email=payload.email, hashed_password=get_password_hash(payload.password))
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


@router.post('/login/', response_model=Token)
async def login(payload: UserLogin, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.email == payload.email))
    user = result.scalar_one_or_none()
    if user is None or not verify_password(payload.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid email or password')

    token = create_access_token(data={'sub': user.email})
    return Token(access_token=token)
