from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
import jwt
import datetime
from fastapi.security import OAuth2PasswordBearer

# Конфигурация для JWT
SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"

app = FastAPI()

class User(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str


def create_access_token(data: dict, expires_delta: datetime.timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.datetime.utcnow() + expires_delta
    else:
        expire = datetime.datetime.utcnow() + datetime.timedelta(minutes=30)  # Токен истекает через 30 минут
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Проверка токена
def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Could not validate token")

# Эндпоинт для логина и получения токена
@app.post("/token", response_model=Token)
async def login_for_access_token(user: User):
    if user.username == "test" and user.password == "password":  # Пример проверки
        access_token = create_access_token(data={"sub": user.username})
        return {"access_token": access_token, "token_type": "bearer"}
    raise HTTPException(status_code=401, detail="Invalid credentials")


@app.get("/protected")
async def protected_route(token: str = Depends(OAuth2PasswordBearer(tokenUrl="token"))):
    payload = verify_token(token)
    return {"message": "You have access", "user": payload["sub"]}
