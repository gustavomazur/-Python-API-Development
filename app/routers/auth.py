from fastapi import APIRouter, Depends, status, HTTPException, Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from .. import database, schemas, models, utils, oauth2

router = APIRouter(tags=['Authentication'])

@router.post('/login')
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):

    #consulta ao nosso banco de dados
    user = db.query(models.User).filter(
        models.User.email == user_credentials.username).first()


    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")

    # a senha em texto puro, que é a senha que o usuário está tentando utilizar;
    # a senha com hash, que vem do banco de dados.
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")


    #Create a token 
    #return token 

    access_token = oauth2.create_acess_token(data = {"user_id": user.id})


    return {"acess_token": access_token, "token_type": "bearer"}