from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm  import Session
from typing import List
from .. import models, schemas, oauth2
from ..database import get_db 

router = APIRouter(
     prefix="/posts",
     tags=['Posts']
)


#GET 
@router.get("/", response_model=List[schemas.Post])
def get_posts(db: Session = Depends(get_db)):
    #cursor.execute("""SELECT * FROM Post """)
    #posts = cursor.fetchall()
    posts = db.query(models.Post).all()
    return posts

#POST 
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_post(post: schemas.PostCreat, db: Session = Depends(get_db), get_current_user: 
schemas.TokenData = Depends(oauth2.get_current_user)):
    
    # cursor.execute("""INSERT INTO pots (title, content, published) VALUES (%s, %s, %s) 
    # RETURNING *""",
    #                 (post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    # conn.commit()
    #-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    # new_post = models.Post(
    #     title=post.title, content=post.content, published=post.published)
    
    new_post = models.Post(
        **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post
 
#GET ID
@router.get("/{id}", response_model=schemas.Post)
def get_post(id: int, db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM pots WHERE id = %s """, ((id,)))
    # post = cursor.fetchone()

    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")
    
    return post

#DELETET ID
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):

    # cursor.execute("""DELETE FROM pots WHERE id = %s returning *""", ((id,)))
    # delete_post = cursor.fetchone()
    # conn.commit()
    post = db.query(models.Post).filter(models.Post.id == id)

    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")
    
    post.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


#PUT ID
@router.put("/{id}", response_model=schemas.Post)
def upadate_post(id: int, update_post: schemas.PostCreat, db: Session = Depends(get_db)):

    # cursor.execute("""UPDATE pots SET title = %s, content = %s, published = %s WHERE id = %s
    # RETURNING *""",
    #                 (post.title, post.content, post. published, (id,)))
    
    # upadate_post = cursor.fetchone()
    # conn.commit

    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()

    if post == None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"post with id: {id} does not exist")

    post_query.update(update_post.dict(), synchronize_session=False)

    db.commit()

    return  post_query.first()
