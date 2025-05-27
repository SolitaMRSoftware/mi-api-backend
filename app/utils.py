#este archivo solo contendrá funciones de utilidad

from passlib.context import CryptContext #encripta la contraseña

pwd_context= CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash(password:str):
    return pwd_context.hash(password)

#hago la funcion para comparar y codificarla
def verify(plain_password, hashed_password):
    
    #hasheo la contraseña
    return pwd_context.verify(plain_password, hashed_password)


    