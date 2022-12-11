import json
import uvicorn
from datetime import datetime, timedelta
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel
# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = "fb1dfaeddc49947fa6381468b60964e758b1c33495c8ae2cf35fdff7f3ee79a4"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


fake_users_db = {
    "juan": {
        "username": "juan",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": '$2b$12$91tN.ua6NatSL6csjPVq6epAQoYQYRCfHi4dh95pbB9530e5jkHF.', #password: 123
        "disabled": False,
    }
}

tags_metadata = [
    {
        "name": "login",
        "description": "Login to use endpoint password/code, (user: juan, password:123)."
    },
    {
        "name": "code",
        "description": "Get information about a postal code (México), doesn't requiere authentication"
    },
    {
        "name": "code_password",
        "description": "Get information about a postal code (México), requieres authentication."
    }
]

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class User(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None


class UserInDB(User):
    hashed_password: str


with open("codigos_postales_reduced.json", encoding='utf-8') as f:
    data = f.read()
postal_code_database = json.loads(data)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
app = FastAPI(openapi_tags=tags_metadata)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)


def authenticate_user(fake_db, username: str, password: str):
    user = get_user(fake_db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(fake_users_db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


@app.post("/token", response_model=Token, tags=["login"])
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/code/{postal_code}", tags=["code"])
async def get_info(postal_code):
    global postal_code_database
    if postal_code in postal_code_database["codigos_postales"]:
        return postal_code_database["codigos_postales"][postal_code]
    else:
        return {"message:": f"El código postal {postal_code} no existe"}

@app.get("/password/code/{postal_code}", tags=["code_password"])
async def get_info(postal_code, current_user: User = Depends(get_current_active_user)):
    global postal_code_database
    if postal_code in postal_code_database["codigos_postales"]:
        return postal_code_database["codigos_postales"][postal_code]
    else:
        return {"message:": f"El código postal {postal_code} no existe"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)