#este archivo solo contendrá un montón de funciones de utilidad

from passlib.context import CryptContext #encripta la contraseña

pwd_context= CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash(password:str):
    return pwd_context.hash(password)
    