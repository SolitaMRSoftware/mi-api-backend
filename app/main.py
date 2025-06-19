from typing import Optional, List
from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel

from random import randrange # para crear num aleatorios
import psycopg2
from psycopg2.extras import RealDictCursor #para que me incluya el nombre de las columnas
import time
from sqlalchemy.orm import Session
#from sqlalchemy.sql.functions import mode #QUE HACE ESTA LIBRERIA?
from . import models, schemas, utils
from .database import engine, get_db
from .routers import post, user, auth

#este comando crea el motor y todos los modelos
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

    
#creo mi conexion
#puedo hacer un while para que lo reintente si la conexion ha fallado hasta que lo logre
while True:
    try:
        conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres', password='contrasenasuperusuario', cursor_factory=RealDictCursor)
        
        #llamo al metodo cursor y lo guardo en una variable para ejecutar las sentencias sql
        cursor = conn.cursor()
        print("Database connection was succesfully!")
        break
    
        #sino obtengo una excepcion y la almaceno en una variable error
    except Exception as error:
        print("Connecting to database failed")
        print("Error: ", error)
        time.sleep(3)

#creo una variable global para simular un BBDD
my_posts = [
    {"title": "Título del post 1 ", "content": "Content del post 1","id": 1}, {"title": "Título del post 2 ", "content": "Content del post 2", "id": 2}
    ]
#creo una funcion para encontrar mi post iterando
def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p
        
#funcion para hallar el indice y luego eliminarlo

def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p['id']== id:
            return i
    
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)

@app.get("/")
async def root():
    return {"message": "Hello world"}

#documentación interactiva http://127.0.0.1:8000/docs