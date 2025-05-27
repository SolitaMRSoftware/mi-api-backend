from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.orm import Session

from .. import database, schemas, models, utils 


router = APIRouter(
    tags=['Authentication']
)

#voy a crear el incio de sesión
@router.post("/login")
def login(user_credentials: schemas.UserLogin, db: Session = Depends(database.get_db)):
    
    #hago la consulta
    user = db.query(models.User).filter(models.User.email == user_credentials.email).first()
    
    #si no es el correo, devuelvo un error
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Credenciales Inválidas")
    
    #ejecuto la funcion de verificacion y comparo si son iguales
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Credenciales Inválidas")
    
    #creo un token y lo retorno
    return {"token": "Token Ejemplo"}
    