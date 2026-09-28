import os
from jose import JWTError, jwt 
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv
from . import schemas 
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer

load_dotenv()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')


#secret_key
#algorithm
#expriation time 

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

if not SECRET_KEY:
    raise RuntimeError(
        "Variavel SECRET_KEY nao encontrada.\n"
        "Crie o arquivo .env na raiz do projeto a partir do .env.example:\n"
        "    cp .env.example .env"
    )

def create_acess_token(data: dict):
    to_encode = data.copy()


    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    #Cria o TOKEN JWT
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


def verify_access_token(token: str, crendentials_exception):

    try:

        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        id: int = payload.get("user_id")

        if id is None:
            raise crendentials_exception
        token_data = schemas.TokenData(id=id)
    except JWTError:
        raise crendentials_exception


    return token_data

def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Couldnot validate credentials", headers={"WWW-Authenticate": "Bearer"})

    return verify_access_token(token, credentials_exception)