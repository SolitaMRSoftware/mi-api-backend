from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List
from .. import models, schemas
from ..database import engine, get_db  # type: ignore

router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)

@router.get("/", response_model=List[schemas.PostResponse])
async def get_posts(db:Session = Depends(get_db)):

    posts = db.query(models.Post).all()
    return posts


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
async def create_posts(post: schemas.PostCreate, db:Session = Depends(get_db)):
    #para crear un post nuevo debo hacer refernecia al modelo que es Post
    new_post =models.Post(**post.model_dump())
    db.add(new_post) #agrego el nuevo post a la BD
    db.commit() #lo confirmo
    db.refresh(new_post) #recupero ese nuevo post
    
    return new_post


#trabajo de a una publicación
@router.get("/{id}", response_model=schemas.PostResponse)
def get_post(id: int, db:Session = Depends(get_db)):
    
    # cursor.execute("""SELECT * FROM posts WHERE id = %s """,(str(id),))
    # post = cursor.fetchone()
    
    #voy a filtrar por id y q retorne el q solicitó el usuario
    post = db.query(models.Post).filter(models.Post.id == id).first()
    
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"El post con id {id} no existe")    
    return post
    

#eliminar el post hallado
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
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



@router.put("/{id}", response_model=schemas.PostResponse)
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