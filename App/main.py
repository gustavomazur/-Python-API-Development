from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time

app = FastAPI()

class Post(BaseModel):
    title:str
    content:str
    published:bool = True
    rating: Optional[int] = None

while True:

    try:
        conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres', 
                                password='postgres123', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print('Database connection was successful')
        break
    except Exception as error:
        print('Connecting to database failed')
        print('Error: ', error)
        time.sleep(2)



my_posts = [{"title": "title of post 1", "content": "content of post 1", "id": 1},
             {"title": "Favorite foods", "content": "I like pizza", "id": 2} ]

def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p

def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p ['id'] == id:
            return i

@app.get("/")
def root():
    return {"message": "Hello, World!"}

#GET 
@app.get("/posts")
def get_posts():
    cursor.execute("""SELECT * FROM pots """)
    posts = cursor.fetchall()
    return {"data": posts}

#POST 
@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    cursor.execute("""INSERT INTO pots (title, content, published) VALUES (%s, %s, %s) 
    RETURNING *""",
                    (post.title, post.content, post.published))
    new_post = cursor.fetchone()
    conn.commit()

    return {"data": new_post}
 
#GET ID
@app.get("/posts/{id}")
def get_post(id: int):
    cursor.execute("""SELECT * FROM pots WHERE id = %s """, ((id,)))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")
    return {"post_detail": post}

#DELETET ID
@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):

    cursor.execute("""DELETE FROM pots WHERE id = %s returning *""", ((id,)))
    delete_post = cursor.fetchone()
    conn.commit()

    if delete_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)

#PUT ID
@app.put("/posts/{id}")
def upadate_post(id: int, post: Post):
    cursor.execute("""UPDATE pots SET title = %s, content = %s, published = %s WHERE id = %s
    RETURNING *""",
                    (post.title, post.content, post. published, (id,)))
    
    upadate_post = cursor.fetchone()
    conn.commit

    if upadate_post == None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"post with id: {id} does not exist")


    return {"data": upadate_post}