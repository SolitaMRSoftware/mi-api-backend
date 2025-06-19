from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone
from . import schemas
from fastapi import Depends,status, HTTPException
from fastapi.security import OAuth2PasswordBearer


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


#clave secreta
#Algoritmo
#Tiempo de expiración
#el comando openssl rand -hex 32 Genera 32 bytes de datos aleatorios y los imprime en formato hexadecimal
SECRET_KEY = "miclavesecreta"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1

def create_access_token(data: dict):
    to_encode = data.copy() #diccionario q voy a codificar
    
    #tiempo de exp
    expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    #actualizo el tiempo
    to_encode.update({"exp": expire})
    #to_encode.update({"exp": int(expire.timestamp())})  # ✅ CORRECCIÓN AQUÍ
    #llamo a la libreria y el metodo para crear el token. Lo guardo en una variable
    
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    
    return encoded_jwt
    
#funcion para verificar token de acceso
def verify_access_token(token: str, credentials_exception):
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id: str = payload.get("user_id") #user_id viene del access_token
        
        if id is None:
            raise credentials_exception
        token_data = schemas.TokenData(id=id) #valida que coincida con mi schema
        
    except JWTError:
        raise credentials_exception
    
    return token_data
    
    
#toma el token de la solicitud y extrae el ID
#verifica que el token sea correcto llamando al token de acc de verificación

def get_current_user(token:str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"No se pudieron validar las credenciales", headers={"WWW-Authenticate":"Bearer"})
    
    return verify_access_token(token, credentials_exception)