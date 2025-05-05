from typing import Optional, List
from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel

from random import randrange # para crear num aleatorios
import psycopg2
from psycopg2.extras import RealDictCursor #para que me incluya el nombre de las columnas
import time
from sqlalchemy.orm import Session
from sqlalchemy.sql.functions import mode #QUE HACE ESTA LIBRERIA?
from . import models, schemas, utils
#from app.models import Post
from .schemas import PostResponse, UserCreate, UserOut
from .database import engine, get_db


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
    

@app.get("/")
async def root():
    return {"message": "Hello world"}


@app.get("/posts", response_model=List[PostResponse])
async def get_posts(db:Session = Depends(get_db)):

    posts = db.query(models.Post).all()
    return posts


@app.post("/posts", status_code=status.HTTP_201_CREATED, response_model=PostResponse)
async def create_posts(post: schemas.PostCreate, db:Session = Depends(get_db)):
    #para crear un post nuevo debo hacer refernecia al modelo que es Post
    new_post =models.Post(**post.model_dump())
    db.add(new_post) #agrego el nuevo post a la BD
    db.commit() #lo confirmo
    db.refresh(new_post) #recupero ese nuevo post
    
    return new_post


#trabajo de a una publicación
@app.get("/posts/{id}", response_model=PostResponse)
def get_post(id: int, db:Session = Depends(get_db)):
    
    # cursor.execute("""SELECT * FROM posts WHERE id = %s """,(str(id),))
    # post = cursor.fetchone()
    
    #voy a filtrar por id y q retorne el q solicitó el usuario
    post = db.query(models.Post).filter(models.Post.id == id).first()
    
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"El post con id {id} no existe")    
    return post
    

#eliminar el post hallado
@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db:Session = Depends(get_db)):
    # cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (str(id),))
    # deleted_post =  cursor.fetchone()
    # conn.commit()
    
    post = db.query(models.Post).filter(models.Post.id == id)

    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"La publicación con id {id} no existe")
    
    post.delete(synchronize_session=False)
    db.commit()
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)



@app.put("/posts/{id}", response_model=PostResponse)
def update_post(id: int, updated_post:schemas.PostCreate, db:Session = Depends(get_db)):
    
    # cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""", (post.title, post.content, post.published, str(id)))
    # updated_post = cursor.fetchone()
    # conn.commit()
    
    post_query = db.query(models.Post).filter(models.Post.id == id)
    
    post = post_query.first()
    
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"La publicación con id {id} no existe")
    
    # post_dict = post.model_dump()
    # post_dict['id'] = id
    # my_posts[index] = post_dict
    post_query.update(updated_post.model_dump() , synchronize_session=False)
    db.commit()
    
    return post_query.first()
    
    
#RUTAS PARA CREAR USUARIOS

@app.post("/users", status_code= status.HTTP_201_CREATED, response_model=UserOut)
def create_user(user:UserCreate, db:Session = Depends(get_db)):
    
    #antes de crear el usuario voy a crear el hash de la password
    
    hash_password = utils.hash(user.password)
    user.password = hash_password
    
    new_user =models.User(**user.model_dump())
    db.add(new_user) #agrego el nuevo post a la BD
    db.commit() #lo confirmo
    db.refresh(new_user) #recupero ese nuevo post
    
    return new_user
    
#recuperar usuario a partir del ID

@app.get("/users/{id}")
def get_user(id: int, db:Session = Depends(get_db)):
    
    #hago la consulta
    db.query(models.User)