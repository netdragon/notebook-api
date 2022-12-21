from fastapi import FastAPI, status, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

from entity.Entity import Memo, User, MemoV
from entity.EntityHome import EntityHome, UserEntityHome

SECRET_KEY = "$2y$12$U82dA.9ObxyrmjtHOJMGWefcggEl2zHA3mS9nOUM1DVUwHvmAZqxq"
ALGORITHM = "HS256"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app = FastAPI()

origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_user(name: str):
    h = UserEntityHome()
    e = h.get_by_name(name)
    return e


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        name: str = payload.get("sub")
        if name is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = get_user(name=name)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=399, detail="Inactive user")
    return current_user


@app.get('/noteapi/v1/memos')
async def method(current_user: User = Depends(get_current_active_user)):
    h = EntityHome(Memo)
    list = h.query_by_cond(Memo.uid == current_user.id)
    return list


@app.get('/noteapi/v1/memo/{id}')
def method(id: int, current_user: User = Depends(get_current_active_user)):
    h = EntityHome(Memo)
    e = h.get(id)
    if e.uid != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Private data could not be accessed!",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return e


@app.post('/noteapi/v1/memo')
def method(memo: MemoV,
           current_user: User = Depends(get_current_active_user)):
    h = EntityHome(Memo)
    m = Memo()
    m.title = memo.title
    m.content = memo.content
    m.label = memo.label
    m.uid = current_user.id
    u = h.add(m)
    return u


@app.put('/noteapi/v1/memo/{id}')
def method(id: int, memo: MemoV,
           current_user: User = Depends(get_current_active_user)):
    h = EntityHome(Memo)
    e = h.get(id)
    if e.uid != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Private data could not be accessed!",
            headers={"WWW-Authenticate": "Bearer"},
        )
    e.title = memo.title
    e.content = memo.content
    e.label = memo.label
    h = EntityHome(Memo)
    u = h.update(e)
    return u


@app.put('/noteapi/v1/memo_color/{id}')
def method(id: int, memo: MemoV,
           current_user: User = Depends(get_current_active_user)):
    h = EntityHome(Memo)
    e = h.get(id)
    if e.uid != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Private data could not be accessed!",
            headers={"WWW-Authenticate": "Bearer"},
        )
    e.color = memo.color
    h = EntityHome(Memo)
    u = h.update(e)
    return u


@app.delete('/noteapi/v1/memo/{id}')
def method(id: int, current_user: User = Depends(get_current_active_user)):
    h = EntityHome(Memo)
    e = h.get(id)
    if e.uid != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Private data could not be accessed!",
            headers={"WWW-Authenticate": "Bearer"},
        )
    h = EntityHome(Memo)
    u = h.delete(id)
    return u

# 记录访问请求时间
# @app.middleware("http")
# async def add_process_time_header(request: Request, call_next):
#     start_time = time.time()
#     response = await call_next(request)
#     process_time = time.time() - start_time
#     response.headers["X-Process-Time"] = str(process_time)
#     # print(response.headers)
#     return response
