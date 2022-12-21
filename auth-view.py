from datetime import datetime, timedelta
from typing import Optional

import uvicorn
from fastapi import Depends, HTTPException, status, Form
from jose import jwt
from pydantic import BaseModel

from common.VerifyCode import VerifyCode
from entity.Entity import User, UserV
from entity.EntityHome import UserEntityHome
from views import app, SECRET_KEY, ALGORITHM, get_user, get_current_active_user

# openssl rand -hex 32
# SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

test_data = {
    "admin": {
        "id": 1,
        "name": "admin",
        "dname": "John Doe",
        "password": "$2y$12$9X/Ts9dpj/TGuDAOl75KKeSdW1AFg6YcEyisGQuz.37q3gv9h1vdS",  # 123
        "disabled": False,
    }
}


class Token(BaseModel):
    access_token: str
    token_type: str


def authenticate_user(name: str, password: str):
    user = get_user(name)
    if not user:
        return False
    if not user.verify_password(password):
        return False
    return user


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


@app.post("/noteapi/token", response_model=Token)
async def login_for_access_token(username: str = Form(...),
                                 password: str = Form(...), vcode: str = Form(...), rcode: str = Form(...)):
    payload = jwt.decode(rcode, SECRET_KEY, algorithms=[ALGORITHM])
    code: str = payload.get("sub")
    if code != vcode:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect verify code",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = authenticate_user(username, password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.name}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.put('/noteapi/v1/password')
def method(user: UserV,
           current_user: User = Depends(get_current_active_user)):
    h = UserEntityHome()
    current_user.hash_password(user.password)
    u = h.update(current_user)
    return u


@app.post('/noteapi/v1/user')
def method(user: UserV):
    h = UserEntityHome()
    m = User()
    m.name = user.name
    m.hash_password(user.password)
    u = h.add(m)
    return u


@app.get('/noteapi/v1/verifycode')
async def method():
    v = VerifyCode()
    c, img = v.get()
    e_time = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    v_token = create_access_token(
        data={"sub": c}, expires_delta=e_time
    )
    return {"code": v_token, "img": img}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8008, log_level="info")
