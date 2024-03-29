from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
import pytest

from app.main import app
from app.config import settings
from app.database import get_db, Base
from app.oauth2 import create_access_token
from app import models


SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.db_username}:{settings.db_passwd}@{settings.db_hostname}:{settings.db_port}/{settings.db_name}_test"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)



@pytest.fixture
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close() 

@pytest.fixture
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close() 
    # run code before test
    # create all tables
    # dependancy override
    app.dependency_overrides[get_db] = override_get_db  
    yield TestClient(app)
    
    
    
@pytest.fixture
def test_user(client):
    user_data = {
        "email": "ti5a2@example.com",
        "password": "123456"
    }
    
    res = client.post("/users/", json=user_data)
    
    assert res.status_code == 201
    
    # print(res.json())
    new_user = res.json()
    new_user["password"] = user_data["password"]
    return new_user

@pytest.fixture
def test_user2(client):
    user_data = {
        "email": "ti5a@example.com",
        "password": "123456"
    }
    
    res = client.post("/users/", json=user_data)
    
    assert res.status_code == 201
    
    # print(res.json())
    new_user = res.json()
    new_user["password"] = user_data["password"]
    return new_user
    
    
@pytest.fixture
def token(test_user):
    return create_access_token({"user_id": test_user["id"]})
    
@pytest.fixture
def auth_client(client, token):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }
    
    return client

@pytest.fixture
def test_posts(test_user, session, test_user2):
    posts_data = [{
        "title": "first title",
        "content": "first content",
        "user_id": test_user["id"] 
    },{
        "title": "second title",
        "content": "second content",
        "user_id": test_user["id"] 
    },{
        "title": "third title",
        "content": "third content",
        "user_id": test_user["id"] 
    },{
        "title": "4th title",
        "content": "4th content",
        "user_id": test_user2["id"] 
    }
    ]
    
    def create_post_model(post):
        return models.Post(**post)
    
    posts_map = map(create_post_model, posts_data)
    posts = list(posts_map)
    session.add_all(posts)
    session.commit()
    posts = session.query(models.Post).all()
    return posts