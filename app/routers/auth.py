from fastapi import APIRouter, Depends, status, HTTPException, Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from .. import database, schemas, models, utils, oauth2


router = APIRouter(
    tags=['Authentication']
)

#voy a crear el incio de sesión
@router.post("/login")
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    
    #hago la consulta
    user = db.query(models.User).filter(
        models.User.email == user_credentials.username).first()
    
    #si no es el correo, devuelvo un error
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Credenciales Inválidas")
    
    #ejecuto la funcion de verificacion y comparo si son iguales
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Credenciales Inválidas")
    
    #creo un token y lo retorno
    access_token = oauth2.create_access_token(data={"user_id": user.id})
    
    return {"access_token": access_token, "token_type": "bearer"}
    