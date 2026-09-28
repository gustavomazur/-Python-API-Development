from typing import Optional, List
from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time 
from sqlalchemy.orm  import Session
from .import models, schemas, utils
from .database import engine, get_db
from .routers import post, user, auth


#código de inicialização do banco
models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p

def find_index_post(id):
     for i, p in enumerate(my_posts):
         if p ['id'] == id:
             return i

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)


@app.get("/")
def root():
    return {"message": "Hello, World!"}
