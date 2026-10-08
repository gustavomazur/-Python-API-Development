from fastapi.testclient import TestClient
from app.main import app

from app.config import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base 
from app.database import get_db
from app.database import Base
import pytest
from alembic import command
from app import models
from app.oauth2 import create_acess_token


SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{
    settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine)

@pytest.fixture()
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture()
def cliente(session):
    def overrid_get_db():

        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db] = overrid_get_db
    yield TestClient(app)

@pytest.fixture
def test_user2(cliente):
    user_data = {"email": "mazur001@gmail.com",
                 "password": "senha123"}
    res = cliente.post("/users/", json=user_data)

    assert res.status_code == 201
    new_user = res.json()
    new_user["password"] = user_data["password"]
    return new_user


@pytest.fixture
def test_user(cliente):
    user_data = {"email": "mazur@gmail.com",
                 "password": "senha123"}
    res = cliente.post("/users/", json=user_data)

    assert res.status_code == 201
    new_user = res.json()
    new_user["password"] = user_data["password"]
    return new_user



@pytest.fixture
def token(test_user):
    return create_acess_token({"user_id": test_user['id']})

@pytest.fixture
def authorized_client(cliente, token):
    cliente.headers = {
        **cliente.headers,
        "Authorization": f"Bearer {token}"
    }
    return cliente

@pytest.fixture
def test_posts(test_user, session, test_user2):
    posts_data = [
        {
            "title": "first title",
            "content": "first content",
            "user_id": test_user['id']
        },
        {
            "title": "2nd title",
            "content": "2nd content",
            "user_id": test_user['id']
        },
        {
            "title": "3rd title",
            "content": "3rd content",
            "user_id": test_user['id']
        },
        {
        "title": "3rd title",
        "content": "3rd content",
        "user_id": test_user2['id']            
        }]

    def creat_post_model(post):
        return models.Post(**post)
    
    post_map = map(creat_post_model, posts_data)
    posts = list(post_map)

    session.add_all(posts)

    # session.add_all([models.Post(title='first title', content='first content', user_id = test_user['id']),
    #                  models.Post(title='2nd title', content='2nd content', user_id = test_user['id']),
    #                  models.Post(title='3rd title', content='3rd content', user_id = test_user['id'])])
    session.commit()

    posts = session.query(models.Post).all()
    return posts
