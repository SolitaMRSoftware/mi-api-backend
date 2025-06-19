from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models, schemas, utils
from ..database import engine, get_db  # type: ignore

router = APIRouter(
    prefix="/users",
    tags=['Users']
)


#RUTAS PARA CREAR USUARIOS

@router.post("/", status_code= status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user:schemas.UserCreate, db:Session = Depends(get_db)):
    
    #antes de crear el usuario voy a crear el hash de la password
    hash_password = utils.hash(user.password)
    user.password = hash_password
    
    new_user =models.User(**user.model_dump())
    db.add(new_user) #agrego el nuevo post a la BD
    db.commit() #lo confirmo
    db.refresh(new_user) #recupero ese nuevo post
    
    return new_user
    
#recuperar usuario a partir del ID

@router.get("/{id}", response_model=schemas.UserOut)
def get_user(id: int, db:Session = Depends(get_db)):
    #hago la consulta
    user = db.query(models.User).filter(models.User.id == id).first()
    
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"el usuario con id: {id} no existe")
    
    return user
