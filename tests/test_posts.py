
import pytest
from app import schemas

def test_get_all_posts(authorized_client, test_posts):
    res = authorized_client.get("/posts/")

    def validate(post):
        return schemas.PostOut(**post)
    posts_map = map(validate, res.json())
    posts_list = list(posts_map)

    assert len(res.json()) == len(test_posts)
    assert res.status_code == 200

def test_unauthorized_user_get_one_posts(cliente, test_posts):
    res = cliente.get(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401

def test_get_one_post_not_exist(authorized_client, test_posts):
    res = authorized_client.get(f"/posts/88888")
    assert res.status_code == 404

def test_get_one_post(authorized_client, test_posts):
    res = authorized_client.get(f"/posts/{test_posts[0].id}")
    post = schemas.PostOut(**res.json())
    assert post.post.id == test_posts[0].id
    assert post.post.content == test_posts[0].content
    assert post.post.title == test_posts[0].title
@pytest.mark.parametrize('title, content, published', [
    ('test_1', 'asdf', True),
    ('test_2', 'çlkj', False),
    ('test_3','gh', True)
])
def test_create_post(authorized_client, test_user, test_posts, title, content, published):
    res = authorized_client.post("/posts/", json={"title": title,
                                                  "content": content,
                                                  "published": published})

    created_post = schemas.Post(**res.json())
    assert res.status_code == 201
    assert created_post.title == title
    assert created_post.content == content
    assert created_post.published == published
    assert created_post.user_id == test_user['id']

def test_creat_post_default_published_true(authorized_client, test_posts, test_user):
    res = authorized_client.post("/posts/", json={"title": "arbitray title",
                                                  "content": "asdfg",})

    created_post = schemas.Post(**res.json())
    assert res.status_code == 201
    assert created_post.title == "arbitray title"
    assert created_post.content == "asdfg"
    assert created_post.published == True
    assert created_post.user_id == test_user['id']


def test_unauthorized_user_create_posts(cliente, test_user, test_posts):
    res = cliente.post("/posts/", json={"title": "arbitray title",
                                        "content": "asdfg",})

    assert res.status_code == 401


def test_unauthorized_user_delete_Post(cliente, test_user, test_posts):
    res = cliente.delete(
        f"/posts/{test_posts[0].id}")
    
    assert res.status_code == 401

def test_delete_post_sucess(authorized_client, test_user, test_posts):
    res = authorized_client.delete(
        f"/posts/{test_posts[0].id}")
    
    assert res.status_code == 204



def test_delete_post_non_exist(authorized_client, test_user, test_posts):
    res = authorized_client.delete(
        f"/posts/800000")
    
    assert res.status_code == 404


def test_delete_other_user_post(authorized_client, test_user, test_posts):
    res = authorized_client.delete(
        f"/posts/{test_posts[3].id}")
    
    assert res.status_code == 403


def test_update_post(authorized_client, test_user, test_posts):
    data = {
        "title": "updated title",
        "content": "updatd content",
        "id": test_posts[0].id
    }
    res = authorized_client.put(f"/posts/{test_posts[0].id}", json=data)
    update_post = schemas.Post(**res.json())
    assert res.status_code == 200
    assert update_post.title == data['title']
    assert update_post.content == data['content']

def test_update_other_user_post(authorized_client, test_user, test_user2, test_posts):
    data = {
        "title": "updated title",
        "content": "updatd content",
        "id": test_posts[3].id
        }
    res = authorized_client.put(f"/posts/{test_posts[3].id}", json=data)
    assert res.status_code == 403

def test_authorized_user_update_post(cliente, test_user, test_posts):
    res = cliente.put(
        f"/posts/{test_posts[0].id}")
    assert res.status_code == 401

def test_update_post_non_exist(authorized_client, test_user, test_posts):
    data = {
        "title": "updated title",
        "content": "updatd content",
        "id": test_posts[3].id
    }
    res = authorized_client.put(
        f"/posts/800000", json=data)
    
    assert res.status_code == 404